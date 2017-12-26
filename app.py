#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import string
import time

BASE_URL = 'http://www.dictionary.com/list/'
SLEEP_TIME = 0.5
# Generates URLs [ 'http://www.dictionary.com/list/a', 'http://www.dictionary.com/list/b' ]
BASE_URLS = [ BASE_URL + letter + '/' + str(1) for letter in string.ascii_lowercase ]
pages_to_visit = BASE_URLS
visited = []
words = set()

while len(pages_to_visit) != 0:
    print(f'Pages to visit: {len(pages_to_visit)} Scraping: {pages_to_visit[0]}')
    # Visit first page
    r = requests.get(pages_to_visit[0])
    # Parse html
    soup = BeautifulSoup(r.content, 'html.parser')
    # Add url to visited pages
    visited.append(pages_to_visit[0])
    # Remove url from pages_to_visit
    pages_to_visit.pop(0)
    print(f'Pages visited: {len(visited)}')

    # Scrape links to other other pages with the same letter
    # Adds them to the pages_to_visit stack
    for div in soup.find_all(class_='pagination'):
        for a in div.find_all('a'):
            if a.get('href') not in visited and a.get('href') not in pages_to_visit:
                pages_to_visit.append(a.get('href'))

    # Scrape words out of page
    for div in soup.find_all(class_='words-list'):
        for a in div.find_all('a'):
            words.add(a.text)

    time.sleep(SLEEP_TIME)

with open('words.txt', 'w') as f:
    for word in sorted(words):
        f.write(word + '\n')
f.close()

