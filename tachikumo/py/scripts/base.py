import requests
from bs4 import BeautifulSoup

start_page = 1
end_page = 1  
url_template = f"https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page={start_page}"
div_class = "list-truyen-item-wrap"
output_file = "output.txt"

with open(output_file, "w", encoding='UTF-8') as file:
    for page_number in range(start_page, end_page + 1):
        url = url_template.format(page_number)
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all("div", class_=div_class)

        for div in divs:
            anchor_tags = div.find_all("a", class_=False)
            for anchor in anchor_tags:
                if anchor.get_text() == anchor.get('title'):
                    anchor_text = anchor.get_text().strip()
                    if anchor_text:
                        file.write(anchor_text + "\n")

            img_tags = div.find_all("img")
            for img in img_tags:
                img_src = img.get("src")
                if img_src:
                    file.write(img_src + "\n")

            for anchor in anchor_tags:
                if anchor.get_text() == anchor.get('title'):
                    anchor_href = anchor.get('href')
                    file.write(anchor_href + "\n")
            
            file.write('\n')

class SeriesInfo():
    def __init__(self) -> None:
        self.LABEL = []
        self.VALUE = []
        self.CHAPTER = {}
        pass
    
    def meta(self, passurl):
        response = requests.get(passurl) # Get URL by setting the parameter as the url of the title
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        #Variation 1 - td with class=table-label and table-value
        class_label = soup.find_all('td', class_='table-label')
        class_value = soup.find_all('td', class_="table-value")
        
        #Variation 1 Append
        for labels in class_label:
            self.LABEL.append(labels.get_text())
        
        for values in class_value:
            self.VALUE.append(values.get_text())

        
        #Variation 2 - li under div class=manga-info-text, try function to avoid breaking of site
        try:
            li_ul = soup.find('ul', class_="manga-info-text")
            # Find all the li elements within the ul
            li_elements = li_ul.find_all('li')
            
            # Extract the text content of each li element and append to self.VALUE
            for li_element in li_elements:
                self.VALUE.append(li_element.get_text())
                
        except AttributeError:
            pass
        
        
        #Variation 1
        chapters_name = soup.find_all('a', class_="chapter-name text-nowrap")
        chapters_date = soup.find_all('span', class_="chapter-time text-nowrap")
        chapter_links = [chapter['href'] for chapter in chapters_name]

        #List comprehension that makes the name as the key and the links and date as the value
        self.CHAPTER = {name.get_text(): {'date': date.get_text(), 'link': link} for name, date, link in zip(chapters_name, chapters_date, chapter_links)}

        #Variation 2
        
        print(self.CHAPTER)
        
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get the entire HTML content and print it
        entire_html = soup.prettify()
        print(entire_html)

test = SeriesInfo()
test.meta('https://mangakakalot.com/manga/jg934614')