import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def get_paragraphs_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = [p.get_text(separator=' ', strip=True) for p in soup.find_all('p')]
    return paragraphs

def crawl_website(start_url, max_pages=50):
    to_crawl = [start_url]
    crawled = set()
    all_paragraphs = []

    while to_crawl and len(crawled) < max_pages:
        url = to_crawl.pop(0)
        if url in crawled:
            continue

        print(f"Crawling: {url}")
        paragraphs = get_paragraphs_from_url(url)
        if paragraphs:
            all_paragraphs.extend(paragraphs)

        crawled.add(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            absolute_link = urljoin(url, link['href'])
            if urlparse(absolute_link).netloc == urlparse(start_url).netloc:
                to_crawl.append(absolute_link)

        time.sleep(1)

    return all_paragraphs

start_url = 'https://www.saglik.gov.tr/'
paragraphs = crawl_website(start_url, max_pages=10)

for i, paragraph in enumerate(paragraphs):
    print(f"Paragraph {i+1}:")
    print(paragraph)  # İlk 500 karakteri göster
    print("-" * 80)
