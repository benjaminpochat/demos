import unittest
from unittest.mock import MagicMock

from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.web_resource import WebDocument
from src.main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader


def mock_get_random_web_documents_generator():
    doc1 = WebDocument(ident='1', text_content='This is the highway to hell')
    doc1.classified_as_official_report = Boolean.TRUE
    doc2 = WebDocument(ident='2', text_content='Baby you can drive my car')
    doc2.classified_as_official_report = Boolean.FALSE
    doc3 = WebDocument(ident='3', text_content='Hey Mr Tambourine man')
    doc3.classified_as_official_report = Boolean.FALSE
    doc4 = WebDocument(ident='4', text_content='Ticking away the moment that make up a dull day')
    doc4.classified_as_official_report = Boolean.TRUE
    documents = [doc1, doc2, doc3, doc4].__iter__()
    return MagicMock(return_value=documents)


class TestTextAndLabelLoader(unittest.TestCase):

    def test_load_text_and_labels_should_convert_list_web_documents_in_tuple_of_list(self):
        # given
        loader = TextAndLabelLoader()
        loader._get_random_web_documents_generator = mock_get_random_web_documents_generator()

        # when
        text_and_labels_loaded = loader.load_texts_and_labels(training_size=2, validation_size=2)

        # then
        training_texts, training_labels, validation_texts, validation_labels = text_and_labels_loaded
        self.assertEquals(training_texts, ['This is the highway to hell', 'Baby you can drive my car'])
        self.assertEquals(training_labels, [1, 0])
        self.assertEquals(validation_texts, ['Hey Mr Tambourine man', 'Ticking away the moment that make up a dull day'])
        self.assertEquals(validation_labels, [0, 1])

    def test_is_random_web_document_acceptable_should_return_true_for_document_classified_as_true(self):
        # given
        doc = WebDocument(ident='1', text_content='This is the highway to hell')
        doc.classified_as_official_report = Boolean.TRUE
        loader = TextAndLabelLoader()

        # when
        acceptable = loader.is_random_web_document_acceptable(doc, set())

        # then
        self.assertTrue(acceptable)

    def test_is_random_web_document_acceptable_should_return_true_for_document_classified_as_false(self):
        # given
        doc = WebDocument(ident='1', text_content='This is the highway to hell')
        doc.classified_as_official_report = Boolean.FALSE
        loader = TextAndLabelLoader()

        # when
        acceptable = loader.is_random_web_document_acceptable(doc, set())

        # then
        self.assertTrue(acceptable)

    def test_is_random_web_document_acceptable_should_return_false_for_document_classified_as_unknown(self):
        # given
        doc = WebDocument(ident='1', text_content='This is the highway to hell')
        doc.classified_as_official_report = Boolean.UNKNOWN
        loader = TextAndLabelLoader()

        # when
        acceptable = loader.is_random_web_document_acceptable(doc, set())

        # then
        self.assertFalse(acceptable)

    def test_is_random_web_document_acceptable_should_return_false_for_document_already_selected(self):
        # given
        doc = WebDocument(ident='1', text_content='This is the highway to hell')
        doc.classified_as_official_report = Boolean.TRUE
        loader = TextAndLabelLoader()
        selected_documents = set()
        selected_documents.add(doc)

        # when
        acceptable = loader.is_random_web_document_acceptable(doc, selected_documents)

        # then
        self.assertFalse(acceptable)
