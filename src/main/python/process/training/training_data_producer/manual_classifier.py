import subprocess
import sys

from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.web_resource import WebDocument
from src.main.python.persistence.redis_access import RedisAccess


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
        while self._is_classification_defined():
            self._current_web_document = self._redis_access.get_random_aggregate(WebDocument)

    def _is_classification_defined(self):
        return self._current_web_document.classified_as_official_report == Boolean.TRUE \
               or self._current_web_document.classified_as_official_report == Boolean.FALSE

    def _display_random_web_document(self):
        echo_content = subprocess.Popen(('echo', self._current_web_document.text_content), stdout=subprocess.PIPE)
        subprocess.call('less', stdin=echo_content.stdout)

    def _ask_for_classification(self):
        response = input('Is this an official report ? [ y | n ]')
        while response.lower() not in ['y', 'n']:
            response = input('Is this an official report ? [ y | n ]')
        if response.lower() == 'y':
            self._current_web_document.classified_as_official_report = Boolean.TRUE
        else:
            self._current_web_document.classified_as_official_report = Boolean.FALSE

    def _store_classification(self):
        self._redis_access.store_aggregate(self._current_web_document)
        print('Classification for category \'official report\' stored \n'
              + ' - WebDocument\'s id  : ' + self._current_web_document.get_id () + '\n'
              + ' - WebDocument\'s url : ' + self._current_web_document.url + '\n'
              + ' - Classification for \'official report\' : ' + str(self._current_web_document.classified_as_official_report))

    def _clear_classification(self):
        confirmation = input('Are you sure to delete all classification data ? [ y | n ]')
        if confirmation.lower() == 'y':
            web_documents = self._redis_access.list_aggregates(WebDocument)
            cleared_documents_counter = 0
            for web_document in web_documents:
                if web_document.classified_as_official_report != Boolean.UNKNOWN:
                    web_document.classified_as_official_report = Boolean.UNKNOWN
                    self._redis_access.store_aggregate(web_document)
                    cleared_documents_counter += 1
            print(str(cleared_documents_counter) + ' classifications cleared on web documents.')
        else:
            print('Cleaning classification canceled.')

    def _show_classification_status(self):
        web_documents = self._redis_access.list_aggregates(WebDocument)
        classified_document_counter = 0
        document_counter = 0
        local_governments_documented = set()
        for web_document in web_documents:
            document_counter += 1
            if web_document.local_government is not None:
                local_governments_documented.add(web_document.local_government)
            if self._is_document_classified(web_document):
                classified_document_counter += 1
        print('Classification status :')
        print(str(document_counter) + ' documents in total found in ' + str(len(local_governments_documented)) + ' local governments')
        print(str(classified_document_counter) + ' classified documents')

    def _is_document_classified(self, web_document):
        return web_document.classified_as_official_report == Boolean.TRUE \
               or web_document.classified_as_official_report == Boolean.FALSE


if __name__ == '__main__':
    print('Welcome to the local government documents classifier program !')
    if sys.argv.__contains__('-h'):
        print('Command line to classify documents found on the local governments\' web sites.')
        print('Preresites : start the database')
        print('Usage : sh classify_training_data.sh [opt]')
        print('Options :')
        print('  -C clear the classification on all documents before starting')
        print('  -s get the status of the classification : number of documents classified, total of documents')
        print('')
    else:
        classifier = ManualWebDocumentClassifier()
        if sys.argv.__contains__('-C'):
            classifier._clear_classification()
        if sys.argv.__contains__('-s'):
            classifier._show_classification_status()
        while True:
            input('Start next classification ? [Ctrl+C : quit | Enter : continue]')
            classifier.classify()
