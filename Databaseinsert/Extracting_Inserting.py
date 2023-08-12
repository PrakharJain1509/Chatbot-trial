import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

conn = sqlite3.connect('website_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS website_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        text_content TEXT,
        hyperlink TEXT
    )
''')
conn.commit()

visited_urls = set()


def extract_and_store_data(url):
    if url in visited_urls:
        #print(f'{url} has already been visited. Skipping.')
        return

    visited_urls.add(url)

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        text_content = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])

        hyperlinks = [a['href'] for a in soup.find_all('a', href=True)]

        cursor.execute('SELECT id FROM website_content WHERE url = ?', (url,))
        existing_data = cursor.fetchone()
        if existing_data:
            #print(f'Data from {url} already exists in the database. Skipping insertion.')
            pass
        else:
            cursor.execute('INSERT INTO website_content (url, text_content, hyperlink) VALUES (?, ?, ?)',
                           (url, text_content, ', '.join(hyperlinks)))
            conn.commit()
            print(f'Data extracted and stored from {url}')

            base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
            for link in hyperlinks:
                full_link = urljoin(base_url, link)
                if full_link.startswith(base_url):
                    extract_and_store_data(full_link)
    else:
        print(f'Error fetching data from {url}')

website_url = 'https://www.educative.io/blog/pandas-cheat-sheet'

extract_and_store_data(website_url)

conn.close()
