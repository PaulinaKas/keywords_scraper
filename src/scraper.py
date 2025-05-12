import os
import json
import pandas as pd
from bs4 import BeautifulSoup


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def extract_main_page_url(soup: BeautifulSoup, starts_with: str) -> str or None:
    hrefs = [link['href'] for link in soup.find_all('link', href=True)]

    for href in hrefs:
        if href.startswith(starts_with):
            return href
    return None


def extract_more_data(soup: BeautifulSoup, html_elements: {}, k: int, df: pd.DataFrame) -> pd.DataFrame:
    element_type = html_elements['page_elements']['type']
    element_id = html_elements['page_elements']['id']
    script_tag = soup.find('script', {'type': element_type, 'id': element_id})

    if script_tag:
        data = json.loads(script_tag.string)
        for key, value in data.items():
            if isinstance(value, str):
                key = key.replace('@', '')
                df.at[k, key] = value
            elif isinstance(value, dict):
                if value['@type'] == 'Place':
                    df.at[k, value['@type']] = value['name']

    main_page_starts_with = html_elements["main_page_starts_with"]
    df.at[k, 'Link'] = extract_main_page_url(soup, main_page_starts_with)

    return df



def scrape_from_file(html_dir: str, htmls) -> pd.DataFrame:
    df = pd.DataFrame()
    k = 0
    filenames = os.listdir(html_dir)
    html_output_file = htmls['html_output_file']


    for filename in filenames:
        if filename.endswith('.html'):
            path = os.path.join(html_dir, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    # pretty_html = soup.prettify()
                    df = extract_more_data(soup, htmls, k, df)
                    k += 1
                df += df
            except:
                pass
    df.to_csv(html_output_file, index=False)
    return df


def main():
    htmls = load_config('../config/htmls.json')
    html_dir = '../data/html_websites'

    scrape_from_file(html_dir, htmls)

if __name__ == '__main__':
    main()