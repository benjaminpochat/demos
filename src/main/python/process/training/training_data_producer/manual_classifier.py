import random
import subprocess

from src.main.python.persistence.redis_index_manager import RedisIndexManager
from src.main.python.commons.configuration import Configuration
from src.main.python.model.local_government import LocalGovernment
from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.web_resource import WebDocument
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.commons.data_subset_type import DataSubsetType

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

    def distribute_classification(self):
        """
        Split the dataset into 3 subset : training, validation, test.
        """
        classified_document_keys = self._get_classified_document_keys()
        dataset_size = classified_document_keys.__len__()
        subset_type_array = [DataSubsetType.TRAINING] * self._get_subset_size(DataSubsetType.TRAINING, dataset_size) \
            + [DataSubsetType.VALIDATION] * self._get_subset_size(DataSubsetType.VALIDATION, dataset_size) \
            + [DataSubsetType.TEST] * self._get_subset_size(DataSubsetType.TEST, dataset_size) \
            + [DataSubsetType.UNKNOWN] * self._get_subset_size(DataSubsetType.UNKNOWN, dataset_size)
        random.shuffle(subset_type_array)
        for i in range(0, dataset_size ):
            document = self._redis_access.get_aggregate(WebDocument, classified_document_keys[i])
            subset_type = subset_type_array[i]
            document.subset_type = subset_type
            self._redis_access.store_aggregate(document)
        redis_index_manager = RedisIndexManager()
        redis_index_manager.update_index(WebDocument, 'subset_type')
        print('The classification dataset has been distributed over 3 subsets : ')
        print('* traning subset : ' + str(self._get_subset_size(DataSubsetType.TRAINING, dataset_size)) + ' items')
        print('* validation subset : ' + str(self._get_subset_size(DataSubsetType.VALIDATION, dataset_size)) + ' items')
        print('* test subset : ' + str(self._get_subset_size(DataSubsetType.TEST, dataset_size)) + ' items')

    def _get_classified_document_keys(self):
        document_keys = self._redis_access.search_aggregate_keys_by_attribute_value(
            the_class=WebDocument,
            attribute_name='classified_as_official_report',
            attribute_value='Boolean.TRUE')
        document_keys = document_keys + self._redis_access.search_aggregate_keys_by_attribute_value(
            the_class=WebDocument,
            attribute_name='classified_as_official_report',
            attribute_value='Boolean.FALSE')
        return document_keys

    def _get_subset_size(self, subset_type: DataSubsetType, dataset_size: int):
        return round(dataset_size * self._get_dataset_percent(subset_type) / 100)

    def _get_dataset_percent(self, subset_type: DataSubsetType):
        if DataSubsetType.TRAINING == subset_type:
            return Configuration().get_traning_dataset_percent()
        if DataSubsetType.VALIDATION == subset_type:
            return Configuration().get_validation_dataset_percent()
        if DataSubsetType.TEST == subset_type:
            return Configuration().get_test_dataset_percent()
        if DataSubsetType.UNKNOWN == subset_type:
            return 100 - Configuration().get_traning_dataset_percent() - Configuration().get_validation_dataset_percent() - Configuration().get_test_dataset_percent()



