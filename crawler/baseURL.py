
from urllib.parse import urlparse


def get_base_domain(url):
    # This causes an HTTP request; if your script is running more than,
    # say, once a day, you'd want to cache it yourself.  Make sure you
    # update frequently, though!

    hostname = urlparse(url).hostname

    return hostname
