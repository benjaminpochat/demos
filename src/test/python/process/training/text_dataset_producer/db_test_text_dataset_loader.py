import unittest

from src.main.python.persistence.redis_index_manager import RedisIndexManager
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.commons.data_subset_type import DataSubsetType
from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.web_resource import WebDocument
from src.main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader


class TestTextAndLabelLoader(unittest.TestCase):

    def setUp(self):
        self._redis_access = RedisAccess()

        self.doc1 = WebDocument(ident='1', text_content='This is the highway to hell')
        self.doc1.classified_as_official_report = Boolean.TRUE
        self.doc1.subset_type = DataSubsetType.TRAINING
        self._redis_access.store_aggregate(self.doc1)

        self.doc2 = WebDocument(ident='2', text_content='Baby you can drive this car to hell')
        self.doc2.classified_as_official_report = Boolean.FALSE
        self.doc2.subset_type = DataSubsetType.TRAINING
        self._redis_access.store_aggregate(self.doc2)

        self.doc3 = WebDocument(ident='3', text_content='Hey Mr Tambourine man, let''s get away')
        self.doc3.classified_as_official_report = Boolean.FALSE
        self.doc3.subset_type = DataSubsetType.VALIDATION
        self._redis_access.store_aggregate(self.doc3)

        self.doc4 = WebDocument(ident='4', text_content='Ticking away the moment that make up a dull day')
        self.doc4.classified_as_official_report = Boolean.TRUE
        self.doc4.subset_type = DataSubsetType.VALIDATION
        self._redis_access.store_aggregate(self.doc4)

        redis_index_manager = RedisIndexManager()
        redis_index_manager.update_index(WebDocument, 'subset_type')

    def test_load_text_and_labels_should_convert_list_web_documents_in_tuple_of_list(self):
        # given
        loader = TextAndLabelLoader()

        # when
        text_and_labels_loaded = loader.load_texts_and_labels()

        # then
        training_texts, training_labels, validation_texts, validation_labels = text_and_labels_loaded
        self.assertTrue(training_texts.__contains__('This is the highway to hell'))
        self.assertEquals(training_labels[training_texts.index('This is the highway to hell')], 1)

        self.assertTrue(training_texts.__contains__('Baby you can drive this car to hell'))
        self.assertEquals(training_labels[training_texts.index('Baby you can drive this car to hell')], 0)

        self.assertTrue(validation_texts.__contains__('Hey Mr Tambourine man, let''s get away'))
        self.assertEquals(validation_labels[validation_texts.index('Hey Mr Tambourine man, let''s get away')], 0)

        self.assertTrue(validation_texts.__contains__('Ticking away the moment that make up a dull day'))
        self.assertEquals(validation_labels[validation_texts.index('Ticking away the moment that make up a dull day')], 1)

    def tearDown(self):
        self._redis_access.delete_aggregate(self.doc1)
        self._redis_access.delete_aggregate(self.doc2)
        self._redis_access.delete_aggregate(self.doc3)
        self._redis_access.delete_aggregate(self.doc4)

        redis_index_manager = RedisIndexManager()
        redis_index_manager.update_index(WebDocument, 'subset_type')
