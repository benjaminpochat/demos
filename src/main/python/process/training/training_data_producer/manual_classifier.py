import subprocess

from src.main.python.model.local_government import LocalGovernment
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

    def clear_classification(self):
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

    def show_classification_statistics(self):
        print('Classification statistics :')
        web_documents = self._redis_access.list_aggregates(WebDocument)
        print(web_documents.__len__().__str__() + ' documents available in the database.')
        web_documents_classified_as_official_reports = \
            self._redis_access.search_aggregate_keys_by_attribute_value(WebDocument, 'classified_as_official_report', Boolean.TRUE)
        print(web_documents_classified_as_official_reports.__len__().__str__() + ' documents classified as official reports.')
        web_documents_classified_as_non_official_reports = \
            self._redis_access.search_aggregate_keys_by_attribute_value(WebDocument, 'classified_as_official_report', Boolean.FALSE)
        print(web_documents_classified_as_non_official_reports.__len__().__str__() + ' documents classified as non official reports.')
        local_governments_with_classified_web_docs = \
            set([self._redis_access.get_aggregate(WebDocument, web_document_id).local_government.id for web_document_id in web_documents_classified_as_official_reports]) \
            .union(\
            set([self._redis_access.get_aggregate(WebDocument, web_document_id).local_government.id for web_document_id in web_documents_classified_as_non_official_reports]))
        local_gov_names = list()
        for local_gov_id in local_governments_with_classified_web_docs:
            local_gov_names.append(self._redis_access.get_aggregate(LocalGovernment, local_gov_id).name)
            local_gov_names.sort()
        print(local_gov_names.__len__().__str__() + ' local governments with classified documents :')
        for local_gov_name in local_gov_names:
            print('- ' + local_gov_name)