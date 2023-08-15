from bs4 import BeautifulSoup
import requests

# Fetch the webpage
response = requests.get('https://mangakakalot.com/manga/jg934614')
html_content = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find the chapter-list div
chapter_list_div = soup.find('div', class_='chapter-list')

# Initialize a list to store chapter information
chapters = []

# Find all row divs within the chapter-list div
row_divs = chapter_list_div.find_all('div', class_='row')

# Iterate through each row div and extract chapter information
for row in row_divs:
    chapter_link = row.find('a')['href']
    chapter_name = row.find('a').get_text(strip=True)
    chapter_views = row.find_all('span')[1].get_text(strip=True)
    chapter_date = row.find_all('span', title=True)[-1]['title']
    
    chapter_info = {
        'link': chapter_link,
        'name': chapter_name,
        'views': chapter_views,
        'date': chapter_date,
    }
    chapters.append(chapter_info)

# Print the extracted chapter information
for chapter in chapters:
    print("Chapter Name:", chapter['name'])
    print("Chapter Link:", chapter['link'])
    print("Chapter Views:", chapter['views'])
    print("Chapter Date:", chapter['date'])
    print("=" * 30)
