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

start_page = 1
end_page = 3

series = Series() # Initializes the LISTS
series.get_data_latest(start_page, end_page) # Get Data First

print(series.get_title_cover())
