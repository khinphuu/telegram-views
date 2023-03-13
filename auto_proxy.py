import requests
from threading import Thread
from time import sleep as swait
from utilitys import logger
from re import compile



TIME_OUT = 15
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
REGEX = compile(r"(?:^|\D)?(("+ r"(?:[1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"):" + (r"(?:\d|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}"
                + r"|65[0-4]\d{2}|655[0-2]\d|6553[0-5])")
                + r")(?:\D|$)")


class Proxy:
    def __init__(self, http_sources, socks4_sources, socks5_sources):
        self.http_sources = http_sources
        self.socks4_sources = socks4_sources
        self.socks5_sources = socks5_sources
        self.proxies, self.stats = [], 'Nothing'


    def scrap(self, sources, proxy_type):
        for source_url in [s for s in sources if s]:
            try: response = requests.get(
                source_url, 
                timeout=TIME_OUT, 
                headers={'user-agent': USER_AGENT})
            except Exception as e: logger(e)
            if tuple(REGEX.finditer(response.text)):
                for proxy in tuple(REGEX.finditer(response.text)):
                    self.proxies.append( (proxy_type, proxy.group(1)) )


    def init(self):
        threads, self.stats = [], 'Scraping'
        self.proxies.clear()
        for i in (
        (self.http_sources, 'http'), 
        (self.socks4_sources, 'socks4'), 
        (self.socks5_sources, 'socks5') ):
            thread = Thread(target=self.scrap, args=(*i, ))
            threads.append(thread)
            thread.start()
        self.stats = 'Sending'
        for t in threads:  t.join()


    def set_timer(self, seconds):
        def timer():
            while True: 
                self.init()
                self.stats = 'Waiting'
                swait(seconds)
                self.stats = 'Scraping'
        Thread(target=timer).start()


    def __str__(self) -> str: return f'[ Proxies ]: {len(self.proxies)}'
    def __len__(self): return len(self.proxies)
        
    