import urllib2
import re
import multiprocessing,threading,time
import logging,sys
import Queue
import urlparse
from bs4 import BeautifulSoup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-4s %(levelname)s %(threadName)s %(message)s", 
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)


def get_text(url,soup):
    m=''
    for i in soup.stripped_strings:
        m=m+i.encode('utf-8')

    m = re.sub('[!@#$%^&*():;.<>,]','',m)
    m = m.split()
    m =" ".join(m)
    index = open("index.txt",'a')
    index.write(m)
    index.write("\n***\n")
    index.write(url)
    index.write("\n")
    index.close()
    return
def scan_page(url, soup):
    """return link URLs from HTML page"""
    get_text(url,soup)
    for tags in soup.findAll("a",href=True):
        yield urlparse.urljoin(url, tags["href"])

def get_all_links(url):
    """fetch page, return URLs, print timing"""
    start = time.time()
    page = urllib2.urlopen(url).read()
    links = list( scan_page(url, BeautifulSoup(page)) )
    logging.debug(
        '- %s: %.2f, %d links', 
        url, time.time()-start, len(links)
    )
    return links

def scrape(inqueue,visited):
    logging.info('start')
    while True:
        try:
            url=inqueue.get(timeout=5)
            if url in visited:
                logging.info("%s:ignoring visited URL",url)
                continue
            logging.info("url:%s",url)
            visited.add(url)
        except Queue.Empty:
            break
        links = get_all_links(url)
        for link in set(links)-visited:
            inqueue.put(link)
        logging.info("DONE")

def Root(seed):
    visited = set()
    url_queue = Queue.Queue()
    url_queue.put(seed)


    threads =[
        threading.Thread(
            target=scrape,args=[url_queue,visited,],)
        for _ in range(1,4)

        ]

    for th in threads:
        th.start()
    for th in threads:
        th.join()


Root("http://en.wikipedia.org/wiki/Main_Page")





