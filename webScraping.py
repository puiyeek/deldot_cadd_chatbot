import requests
from bs4 import BeautifulSoup
import json
import time
import re


def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_linked_pages(base_url, main_url):
    soup = scrape_page(main_url)
    links = soup.find_all('a', href=True)
    page_urls = set()

    for link in links:
        href = link['href']
        if href.startswith('/index.php') and ':' not in href:
            page_urls.add(base_url + href)

    return list(page_urls)


def scrape_all_pages(page_urls):
    content = []
    for url in page_urls:
        soup = scrape_page(url)
        paragraphs = soup.find_all('p')
        page_content = ' '.join([para.get_text() for para in paragraphs])
        content.append({"url": url, "content": page_content})
        time.sleep(1)  # To avoid overwhelming the server

    return content


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.strip()
    return text


base_url = 'https://caddwiki.deldot.gov'
main_url = 'https://caddwiki.deldot.gov/index.php/Main_Page'

page_urls = get_linked_pages(base_url, main_url)
content = scrape_all_pages(page_urls)

with open('caddwiki_content.json', 'w', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=4)

with open('caddwiki_content.json', 'r', encoding='utf-8') as f:
    raw_content = json.load(f)

for page in raw_content:
    page['content'] = clean_text(page['content'])

with open('cleaned_caddwiki_content.json', 'w', encoding='utf-8') as f:
    json.dump(raw_content, f, ensure_ascii=False, indent=4)

print("Scraping and cleaning completed. Files are ready for use.")
