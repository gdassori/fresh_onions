__author__ = 'guido'

from pastebin.observers import OnionObserver, ErrorsObserver
from pastebin.scraper import PastebinScraper
import time
from pastebin.simple_logger import get_onion_logger
from pastebin.proxies_rotator import USProxyOrg_Fetcher, SingleProxy


def scrape_pastebin(sleep_time, logger):
    i = 0
    while True:
        scraper.scrape_archive()
        if not i or not i % 2:
            logger.info('Pastebin archive scraped {} time{}, total {} pastes parsed'.format(1 if not i else i,
                                                                                            '' if not i else 's',
                                                                                            scraper._pastes_counter))
        i += 1
        time.sleep(sleep_time)

def errors_handler(method, message, logger, proxy_rotator):
    if method in ('slow_down', 'proxy'):
        if message and proxy_rotator:
            proxy_rotator.ban(message)
    elif method in ('empty_archive'):
        logger.error('Banning proxy {}'.format(message  ))
        if message and proxy_rotator:
            proxy_rotator.ban(message)

if __name__ == '__main__':
    logger = get_onion_logger('info')
    onionObserver = OnionObserver(logger)
    errorsObserver = ErrorsObserver(logger)
    proxies_rotator = USProxyOrg_Fetcher(logger)
    # proxy_rotator = SingleProxy()
    errorsObserver.callbacks.append(lambda x, y: errors_handler(x, y, logger, proxies_rotator))
    scraper = PastebinScraper(logger, proxies_rotator=proxies_rotator)
    scraper.pastes_observers.append(onionObserver)
    scraper.errors_observers.append(errorsObserver)
    logger.info('Starting pastebin monitoring for onion links')
    scrape_pastebin(30, logger)