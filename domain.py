from urllib.parse import urlparse

def get_domain_name(url):
    try:
        domain = get_subdomain_name(url)
        parts = domain.split('.')
        if len(parts) >= 2:
            return parts[-2] + '.' + parts[-1]
        return domain
    except:
        return ''

def get_subdomain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


