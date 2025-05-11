import os
import json
import pandas as pd
from bs4 import BeautifulSoup


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def extract_main_page_url(starts_with: str, soup: BeautifulSoup) -> str or None:
    hrefs = [link['href'] for link in soup.find_all('link', href=True)]

    for href in hrefs:
        if href.startswith(starts_with):
            return href
    return None


def scrape_from_file(filepath, htmls) -> pd.DataFrame or None:
    main_page_starts_with = htmls["main_page_starts_with"]

    df = pd.DataFrame(data=None, columns=['Title', 'Link'])
    k = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            pretty_html = soup.prettify()
            title = soup.title.string
            link = extract_main_page_url(main_page_starts_with, soup)
            df.loc[k, 'Title'] = title
            df.loc[k, 'Link'] = link
            k += 1
        return df
    except:
        return None


def main():
    htmls = load_config('../config/htmls.json')
    html_dir = '../data/html_websites'

    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            path = os.path.join(html_dir, filename)
            data = scrape_from_file(path, htmls)


if __name__ == '__main__':
    main()