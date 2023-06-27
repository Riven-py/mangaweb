import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# USED FOR DEBUGGING PURPOSES ONLY

start_page = 1
end_page = 63 
url_template = "https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page={}"
div_class = "list-truyen-item-wrap"
output_file = "output.txt"
filter_text = ['HOT MANGA', 'NEW MANGA', 'COMPLETED MANGA', 'More.', 'Privacy Policy', 'Terms Conditions']

# EACH PAGE HAS 24 TITLES * 2 = 48 BECAUSE GETTING THE ANCHOR TAGS AND IMG TAGS
total_tags = 48 * (end_page - start_page + 1)

with open(output_file, "w", encoding='UTF-8') as file:
    with tqdm(desc="Scraping Progress: ",total=total_tags, unit=" tag", ncols=70, unit_scale=True) as pbar:
        for page_number in range(start_page, end_page + 1):
            url = url_template.format(page_number)
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            divs = soup.find_all("div", class_=div_class)

            for div in divs:
                anchor_tags = div.find_all("a", class_=False)
                for anchor in anchor_tags:
                    anchor_text = anchor.get_text().strip()
                    if anchor_text not in filter_text and anchor_text:
                        file.write(anchor_text + "\n")
                        pbar.update(1)

                img_tags = div.find_all("img")
                for img in img_tags:
                    img_src = img.get("src")
                    if img_src:
                        file.write(img_src + "\n")
                        pbar.update(1)

                
print("\nScraping completed.")
