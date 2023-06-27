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
            
            
