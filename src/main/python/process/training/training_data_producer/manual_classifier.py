import subprocess

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.web_resource import WebDocument


class ManualWebDocumentClassifier:
    def __init__(self):
        self._redis_access = RedisAccess()
        self._current_web_document = None

    def classify(self):
        self._select_randomly_web_document()
        self._display_random_web_document()
        self._ask_for_classification()
        self._store_classification()

    def _select_randomly_web_document(self):
        self._current_web_document = self._redis_access.get_random_aggregate(WebDocument)
        while self._current_web_document.classified_as_official_report is not None:
            self._current_web_document = self._redis_access.get_random_aggregate(WebDocument)

    def _display_random_web_document(self):
        echo_content = subprocess.Popen(('echo', self._current_web_document.text_content), stdout=subprocess.PIPE)
        subprocess.call('less', stdin=echo_content.stdout)

    def _ask_for_classification(self):
        response = input('Is this an official report ? [Y | N]')
        self._current_web_document.classified_as_official_report = response.lower() == 'y'

    def _store_classification(self):
        self._redis_access.store_aggregate(self._current_web_document)
        print('Classification for category \'official report\' stored \n'
              + ' - WebDocument\'s id  : ' + self._current_web_document.get_id () + '\n'
              + ' - WebDocument\'s url : ' + self._current_web_document.url + '\n'
              + ' - Classified as \'official report\' : ' + str(self._current_web_document.classified_as_official_report))


if __name__ == '__main__':
    print('Welcome to the local government data classifier program !')
    classifier = ManualWebDocumentClassifier()
    while True:
        input('Start next classification ? [Ctrl+C : stop | Enter : start next]')
        classifier.classify()


