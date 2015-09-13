__author__ = 'guido'


class OnionObserver():
    def __init__(self, logger):
        self.logger = logger

    def _search_onions(self, raw_paste):
        x = raw_paste.replace('\n', ' ')
        z = x.split(' ')
        onions = [x for x in z if len(x) > 22 and '.onion' in x]
        return onions

    def on_paste(self, paste_id, raw_paste):
        onions = self._search_onions(raw_paste)
        if onions:
            for onion in onions:
                self._on_onion(paste_id, onion)
            self._on_stringmatch(paste_id, raw_paste)

    def _on_onion(self, paste_id, onion):
        self.logger.info('Onion link found on paste {} | {}'.format(paste_id, onion))

    def _on_stringmatch(self, paste_id, raw_paste):
        self.logger.info('\'.onion pattern found in paste_id {}. Saving file'.format(paste_id))
        self._savefile(paste_id, raw_paste)

    def _savefile(self, paste_id, raw_paste):
        with open('pastes/paste_{}.raw'.format(paste_id), 'w') as f:
            f.write(raw_paste)
        self.logger.info('Saved file pastes/paste_{}.raw, worth a look'.format(paste_id))


class ErrorsObserver():
    def __init__(self, logger):
        self.logger = logger
        self.callbacks = []

    def on_error(self, method, message):
        self.logger.error('{} | {}'.format(method, message))
        for callback in self.callbacks:
            callback(method, message)