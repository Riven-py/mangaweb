import requests
from bs4 import BeautifulSoup


class Series:
    def __init__(self):
        self.TITLES = []
        self.COVERS = []
        self.URLS = []

    def get_data_latest(self, start_page, end_page):
        for page_number in range(start_page, end_page + 1):
            url = f"https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page={page_number}"
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            divs = soup.find_all("div", class_='list-truyen-item-wrap')

            for div in divs:
                anchor_tags = div.find_all("a", class_=False)
                for anchor in anchor_tags:
                    if anchor.get_text() == anchor.get('title'):
                        anchor_text = anchor.get_text().strip()
                        self.TITLES.append(anchor_text)

                img_tags = div.find_all("img")
                for img in img_tags:
                    img_src = img.get("src")
                    self.COVERS.append(img_src)

                for anchor in anchor_tags:
                    if anchor.get_text() == anchor.get('title'):
                        anchor_href = anchor.get('href')
                        self.URLS.append(anchor_href)
    
    def print_data(self):
        for title, cover, url in zip(self.TITLES, self.COVERS, self.URLS):
            print(f"Title: {title}\nCover: {cover}\nURL: {url}\n")
            
    def get_title_cover(self):
        title_cover = {}
        for title, cover in zip(self.TITLES, self.COVERS):
            title_cover[title] = cover
        return title_cover


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
        
        find_chapter_div = soup.find('div', class_='chapter-list')
        if find_chapter_div:
            chapter_divs = find_chapter_div.find_all('div', class_='row')
            chapter_list = []

            for chapter_div in chapter_divs:
                chapter_link = chapter_div.find('a')['href']
                chapter_name = chapter_div.find('a').get_text(strip=True)
                chapter_views = chapter_div.find_all('span')[1].get_text(strip=True)
                chapter_date = chapter_div.find_all('span', title=True)[-1]['title']

                chapter_info = {
                    'link': chapter_link,
                    'name': chapter_name,
                    'views': chapter_views,
                    'date': chapter_date,
                }
                chapter_list.append(chapter_info)

            self.CHAPTER = {chapter['name']: {'date': chapter['date'], 'link': chapter['link']} for chapter in chapter_list}
        else:
            print("Chapter div not found.")




#start_page = 1
#end_page = 1

#series = Series() # Initializes the LISTS
#series.get_data_latest(start_page, end_page) # Get Data First

#print(series.get_title_cover())
