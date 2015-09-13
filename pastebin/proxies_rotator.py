__author__ = 'guido'
from bs4 import BeautifulSoup
import requests
import random
import time


class DoYourOwnProxyRotator():
    def __init__(self, logger):
        self.logger = logger

    @property
    def proxies(self):
        self.logger.error('wtf I said do your own')
        raise NotImplementedError()

    @property
    def random_proxy(self):
        self.logger.error('hard to learn')
        raise NotImplementedError()

    def ban(self, proxy):
        self.logger.error('...')
        raise NotImplementedError()

    def is_valid(self, proxy):
        raise NotImplementedError()


class SingleProxy(DoYourOwnProxyRotator):
    def __init__(self, logger, hostname='127.0.0.1', port='8888'):
        self.proxy = '{}:{}'.format(hostname, port)
        super(SingleProxy, self).__init__(logger)

    @property
    def proxies(self):
        return [self.proxy]

    @property
    def random_proxy(self):
        return self.proxy

    def ban(self, proxy):
        self.logger('trying to ban single proxy {}, weird'.format(self.proxy))


class USProxyOrg_Fetcher(DoYourOwnProxyRotator):
    def __init__(self, logger, expire=1800):
        self._proxies = []
        self._blacklist = []
        self.expire = expire
        self.lastupdate = 0
        super(USProxyOrg_Fetcher, self).__init__(logger)

    def _download_proxies(self):
        self.logger.info('Downloading proxies...')
        list = BeautifulSoup(requests.get('http://www.us-proxy.org/').text, "lxml")
        rows = list.find('table').find_all('tr')
        pr = []
        for row in rows:
            proxy = ''
            proxy_found = False
            for td in row.find_all('td'):
                if td.text.count('.') == 3:
                    proxy += td.text
                    proxy_found = True
                elif proxy_found:
                    proxy += ':' + td.text
                    break
            if proxy not in self._proxies + self._blacklist:
                pr.append(proxy)
        self._proxies.extend([proxy for proxy in pr if proxy not in self._proxies])
        self.lastupdate = int(time.time())
        self.logger.info('New {} proxies saved from www.us-proxy.org, total of {} proxies listed'.format(len(pr),
                                                                                   len(self._proxies)))

    @property
    def proxies(self):
        p = [proxy for proxy in self._proxies if proxy not in self._blacklist]
        if not p or not self.lastupdate or int(time.time()) - self.lastupdate > self.expire:
            self._download_proxies()
            return [proxy for proxy in self._proxies if proxy not in self._blacklist and proxy != '']
        return p

    @property
    def random_proxy(self):
        proxies = self.proxies
        # take from the firsts, usually more reliable
        return proxies[random.randint(0, 2)]

    def ban(self, proxy):
        self._blacklist.append(proxy)
        if proxy in self._proxies:
            self._proxies.remove(proxy)

    def is_valid(self, proxy):
        return proxy not in self._blacklist