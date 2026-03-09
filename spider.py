import threading
from urllib import request
from urllib.request import urlopen
from link_finder import LinkFinder
from crawl_functions import *
from domain import *

class Spider:
    project_name=''
    domain_name=''
    crawled_file=''
    queue_file=''
    base_url=''
    queue=set()
    crawled=set()

    lock = threading.Lock()


    def __init__(self, project_name, domain_name, base_url):
        Spider.project_name=project_name
        Spider.domain_name=domain_name
        Spider.base_url=base_url
        Spider.queue_file=Spider.project_name + '/queue.txt'
        Spider.crawled_file=Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawled_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue=file_to_set(Spider.queue_file)
        Spider.crawled=file_to_set(Spider.crawled_file)

    @staticmethod
    def crawled_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(f"{thread_name} now crawling {page_url}")
            print('Queue' + str(len(Spider.queue)) + '|Crawled ' + str(len(Spider.crawled)))
            links=Spider.gather_links(page_url)
            for l in links:
                Spider.add_link_to_queue(l)
            #Spider.queue.remove(page_url)
            Spider.queue.discard(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # @staticmethod
    # def gather_Links(page_url):
    #     html_str=''
    #     try:
    #         response=urlopen(page_url)
    #
    #         if 'text/html' in response.getheader('Content-Type'):
    #             html_bytes=response.read()
    #             html_str=html_bytes.decode("utf-8")
    #         finder=LinkFinder(Spider.base_url, page_url)
    #         finder.feed(html_str)
    #     except Exception as e:
    #         print(str(e))
    #         return set()
    #
    #     return finder.page_links()

    # @staticmethod
    # def add_link_to_queue(links):
    #     for url in links:
    #         if(url in Spider.queue) or (url in Spider.crawled):
    #             continue
    #         if Spider.domain_name != get_domain_name(url):
    #             continue
    #         Spider.queue.add(url)
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)


    @staticmethod
    def gather_links(page_url):
        html_str = ''
        try:
            response = urlopen(page_url)

            content_type = response.getheader('Content-Type') or ''
            if 'text/html' not in content_type:
                return set()

            html_bytes = response.read()

            # Probeer UTF-8, val terug op latin-1
            try:
                html_str = html_bytes.decode("utf-8")
            except UnicodeDecodeError:
                html_str = html_bytes.decode("latin-1")

            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_str)

        except Exception as e:
            print(f"Error while gathering links from {page_url}: {e}")
            return set()

        return finder.page_links()


    @staticmethod
    def add_link_to_queue(links):
        # Zorg dat links altijd een iterable is
        if not isinstance(links, (list, set, tuple)):
            links = [links]

        for url in links:
            # Skip lege of None URLs
            if not url:
                continue

            # Domeinfilter
            if Spider.domain_name != get_domain_name(url):
                continue

            # Thread-safe check & add
            with Spider.lock:
                if (url not in Spider.queue) and (url not in Spider.crawled):
                    Spider.queue.add(url)







