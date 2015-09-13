import logging
import logging.handlers

def get_onion_logger(loglevel):
    loglevels = {'debug': logging.DEBUG,
                 'error': logging.ERROR,
                 'info': logging.INFO}
    # create logger
    l = logging.getLogger("onion")
    l.setLevel(loglevels[loglevel])
    # create console handler and set level to debug
    ch = logging.FileHandler('onion.log')
    ch.setLevel(loglevels[loglevel])
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    l.addHandler(ch)
    return l
