from urllib.parse import urlparse

class URL:
    
    def __init__(self, url: str):
        self.__parse_url(url)


    def __parse_url(self, url: str) -> None:
        url = urlparse(url)
        # customized to make it more like javascript URL standard
        # see https://developer.mozilla.org/en-US/docs/Web/API/URL for reference
        self.hash     = url.fragment
        self.hostname = url.netloc
        self.host     = url.hostname
        self.href     = url.geturl()
        self.password = url.password
        self.pathname = url.path
        self.port     = url.port
        self.protocol = url.scheme
        self.username = url.username
        self.query    = url.query