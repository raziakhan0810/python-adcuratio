import threading
import Queue
import requests
import csv

from bs4 import BeautifulSoup


def worker(url, queue):
    try:
        # print 'Started url: ', url
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, 'html.parser')
        jquery_found = False
        for script in soup.find_all('script', src=True):
            if 'jquery' in script['src']:
                jquery_found = True
                break
        if jquery_found:
            with open('accepted.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([url])
        else:
            with open('rejected.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([url])
        # print 'Completed url: ', url
    except Exception as exc:
        print exc
        print 'Error scraping url: ', url

    queue.put('STOP')


def scrap(filename):
    result = Queue.Queue()
    threads = [threading.Thread(target=worker, args=(url.strip(), result)) for url in open(filename)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print 'Starting scrapper...'
    scrap('url_list.txt')
    print 'Scrapping completed.'
