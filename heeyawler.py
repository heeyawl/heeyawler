
from bs4 import BeautifulSoup
import requests
import time
import hashlib

cache = {}
queue = []
## rooms for visited links

## a: anchor !!

def fetch(url):
    ## let's get the whole page
    return requests.get(url)


def get_links(soup):
    ## links always go with <a>
    ## Get me all the links on the page
    return soup.find_all('a')

def get_filename(url):
    # how to get a proper name for a file
    return hashlib.sha1(url.encode('utf-8')).hexdigest() + '.html'

def link_exists(url):
    ## save them
    return url in cache

## in the case we already have them?
def crawl(url):
    print(f'Fetching {url}...')
    resp = fetch(url)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        # make messy html pretty
        links = get_links(soup)

        with open(get_filename(url), 'wb') as fout:
            fout.write(resp.text.encode('euc-kr'))
            ## No more broken Korean...

        for link in links:
            href = link.get('href')
            if href.startswith('https://news.naver.com/main/read.nhn')\
            and href not in cache:
                queue.append(href)
                cache[href] = 0

    else:
        print(f'Failed to fetch {url}')

if __name__=='__main__':

    queue.append("https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=293&aid=0000025345&date=20191016&type=1&rankingSeq=9&rankingSectionId=105")

    while queue:
        url = queue.pop()
        crawl(url)
        time.sleep(1)
        # take a pause for just one second
        
