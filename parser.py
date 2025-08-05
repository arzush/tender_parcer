import time
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://rostender.info/extsearch?page={page}'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/115.0.0.0 Safari/537.36'
}


def get_tenders_page(page_num):
    url = BASE_URL.format(page=page_num)
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def parse_tenders(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.select('div.tender-info')
    tenders = []

    for card in cards:
        a_tag = card.select_one('a.tender-info__link')
        if not a_tag:
            continue

        title = a_tag.get_text(strip=True)
        href = a_tag.get('href')
        link = 'https://rostender.info' + href
        tender_id = href.split('/')[-1].split('-')[0] if '-' in href else ''

        region_slug = ''
        if href.startswith('/region/'):
            parts = href.split('/')
            if len(parts) > 2:
                region_slug = parts[2].replace('-', ' ').title()

        tenders.append({
            'id': tender_id,
            'title': title,
            'link': link,
            'region': region_slug,
        })

    return tenders


def get_tenders(max_count=100):
    all_tenders = []
    page = 1

    while len(all_tenders) < max_count:
        html = get_tenders_page(page)
        tenders = parse_tenders(html)

        if not tenders:
            break

        all_tenders.extend(tenders)
        page += 1
        time.sleep(1)

    return all_tenders[:max_count]