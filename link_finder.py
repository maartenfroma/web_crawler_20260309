from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'a':
            return

        for (attribute, value) in attrs:
            if attribute.lower() == "href":
                if not value:
                    continue

                # Skip anchors, mailto, javascript, tel, etc.
                if value.startswith('#'):
                    continue
                if value.startswith('mailto:'):
                    continue
                if value.startswith('javascript:'):
                    continue
                if value.startswith('tel:'):
                    continue

                url = parse.urljoin(self.page_url, value)

                url = url.rstrip('/')

                self.links.add(url)

    def page_links(self):
        return self.links


