import requests as requests
from bs4 import BeautifulSoup
import time
import logging

class PastebinScraper():
    def __init__(self, logger, delay=1, proxies_rotator=None):
        self._pastes = []
        self._pastes_counter = 0
        self._pastebin_urls = {'archive': 'http://pastebin.com/archive',
                               'pastes_raw_prefix': 'http://pastebin.com/raw.php?i='}
        self.pastes_observers = []
        self.errors_observers = []
        self.delay = delay
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.proxies_rotator = proxies_rotator
        self.logger = logger
        self.using_proxy = None

    def _handle_error(self, error, payload):
        for observer in self.errors_observers:
            observer.on_error(error, payload)

    def _get_archive(self, proxy):
        try:
            request = requests.get(self._pastebin_urls['archive'], proxies={'http': proxy} if proxy else None)
            if request.ok:
                return request.text
            else:
                self._handle_error('get_archive', proxy)
                return None
        except:
            self.proxies_rotator.ban(proxy)

    def _get_proxy(self):
        if not self.using_proxy or (self.proxies_rotator and not self.proxies_rotator.is_valid(self.using_proxy)):
            self.using_proxy = self.proxies_rotator.random_proxy if self.proxies_rotator else None

    def scrape_archive(self):
        self._get_proxy()
        if not self.using_proxy and self.proxies_rotator:
            self._handle_error('proxy', 'unavailable')
            return
        proxy = self.using_proxy
        try:
            message = 'Going to scrape pastebin with proxy {}'.format(proxy) if proxy else \
                'Going to scrape pastebin'
            self.logger.debug(message)
            archive = self._get_archive(proxy)
            if not archive:
                self._handle_error('empty_archive', proxy)
                return
            elif "You are scraping our site way too fast!" in archive:
                self._handle_error('slow_down', proxy)
                return
            if archive and self.pastes_observers:
                bs = BeautifulSoup(archive, 'lxml')
                try:
                    pastes = [x.get('href').replace('/', '') for x in bs.find('table').find_all('a')
                              if x.get('href') != '/archive/text']
                    for paste_id in pastes:
                        if paste_id not in self._pastes:
                            self._on_new_paste(paste_id, proxy)
                            if self.delay:
                                # avoid flooding pastebin and get banned
                                time.sleep(self.delay)
                except Exception as e:
                    self._handle_error('unexpected_content', proxy)
                    raise e

        except Exception as e:
            self._handle_error('scrape_archive', e)

    def _on_new_paste(self, paste_id, proxy):
        req = requests.get(self._pastebin_urls['pastes_raw_prefix'] + paste_id, proxies={'http': proxy} if proxy \
                           else None)
        if req.ok:
            self._notify_new_paste(paste_id, req.text)
            self._pastes.insert(0, paste_id)
            self._pastes = self._pastes[:1000] # track only last 1000s pastes
            self._pastes_counter += 1
        else:
            self._handle_error('on_new_paste', paste_id)

    def _notify_new_paste(self, paste_id, text):
        for observer in self.pastes_observers:
            observer.on_paste(paste_id, text)