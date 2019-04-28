import os
import unittest
from unittest.mock import Mock, MagicMock

import src.test.python.process.training.text_dataset_producer.db_test_text_dataset_loader as test_text_dataset_loader
from src.main.python.commons.boolean_enum import Boolean
from src.main.python.commons.configuration import Configuration
from src.main.python.model.web_resource import WebDocument
from src.main.python.process.training.classification_model.mlp_model_builder import MlpModelBuilder
from src.main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader


class TestMlpModelBuilder(unittest.TestCase):
    def test_build_model_should_run_without_error_with_few_small_texts(self):

        # given
        model_builder = MlpModelBuilder()
        model_builder._train_model = Mock(side_effect=print('MlpModelBuilder._train_model mocked'))
        text_and_label_loader = TextAndLabelLoader()
        text_and_label_loader.load_texts_and_labels = self.mock_load_texts_and_labels
        texts_and_labels = text_and_label_loader.load_texts_and_labels()
        data = (texts_and_labels[0], texts_and_labels[1]), (texts_and_labels[2], texts_and_labels[3])

        # when
        model_builder.build_model(data)

        # then
        vectorizer_path = os.path.join(os.path.dirname(__file__), '../../../../../main/resources/', Configuration().get_vectorizer_file())
        feature_selector_path = os.path.join(os.path.dirname(__file__), '../../../../../main/resources/', Configuration().get_feature_selector_file())
        model_path = os.path.join(os.path.dirname(__file__), '../../../../../main/resources/', Configuration().get_model_file())
        self.assertTrue(os.path.isfile(vectorizer_path))
        self.assertTrue(os.path.isfile(feature_selector_path))
        self.assertTrue(os.path.isfile(model_path))
        os.remove(vectorizer_path)
        os.remove(feature_selector_path)
        os.remove(model_path)

    def mock_load_texts_and_labels(self):
        doc1 = WebDocument(ident='1', text_content='This is the highway to hell')
        doc1.classified_as_official_report = Boolean.TRUE
        doc2 = WebDocument(ident='2', text_content='Baby you can drive this car to hell')
        doc2.classified_as_official_report = Boolean.FALSE
        doc3 = WebDocument(ident='3', text_content='Hey Mr Tambourine man, let''s get away')
        doc3.classified_as_official_report = Boolean.FALSE
        doc4 = WebDocument(ident='4', text_content='Ticking away the moment that make up a dull day')
        doc4.classified_as_official_report = Boolean.TRUE
        return [doc1.text_content, doc2.text_content],\
                [doc1.classified_as_official_report.to_int(), doc2.classified_as_official_report.to_int()], \
                [doc3.text_content, doc4.text_content], \
                [doc3.classified_as_official_report.to_int(), doc4.classified_as_official_report.to_int()]


if __name__ == '__main__':
    unittest.main()