import threading
from queue import Queue
from spider import Spider
from crawl_functions import *
from domain import *

#PROJECT VARIABLES

PROJECT_NAME="thesite"
HOMEPAGE="https://www.wikipedia.org/"
DOMAIN_NAME=get_domain_name(HOMEPAGE)
QUEUE_FILE=PROJECT_NAME + '/queue.txt'
CRAWLED_FILE=PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS=8
queue=Queue()
Spider(PROJECT_NAME, DOMAIN_NAME, HOMEPAGE)

def crawl():
    queued_links=file_to_set(QUEUE_FILE)
    if len(queued_links)>0:
        print(str(len(queued_links)) + " links in the queue")
        create_jobs()
        queue.join()  #wacht totdat alle jobs klaar zijn
        crawl()  #Check of er nieuwe links zijn toegevoegd


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
        # queue.join()
        # crawl()

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()

def work():
    while True:
        url=queue.get()
        Spider.crawled_page(threading.currentThread().name, url)
        queue.task_done()

create_workers()

crawl()
