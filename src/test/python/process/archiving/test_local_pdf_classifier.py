import unittest
import os

from src.main.python.commons.configuration import Configuration
from src.main.python.process.archiving.local_pdf_classifier import LocalPdfClassifier
from src.main.python.commons.boolean_enum import Boolean


class TestLocalPdfClassifier(unittest.TestCase):

    def test_classify_official_city_council_report_should_be_classified_correctly(self):
        # given
        classifier = LocalPdfClassifier()
        texts = self._load_texts(text_folder='official_city_council_reports')

        # when
        classifications = list(classifier.classify(text_content=text) for text in texts)

        # then
        for classification in classifications:
            self.assertTrue(classification.isOfficialCouncilReport())

    def test_classify_non_official_city_council_report_should_be_classified_correctly(self):
        # given
        classifier = LocalPdfClassifier()
        texts = self._load_texts(text_folder='others')

        # when
        classifications = list(classifier.classify(text_content=text) for text in texts)

        # then
        for classification in classifications:
            self.assertFalse(classification.isOfficialCouncilReport())

    def _load_texts(self, text_folder: str):
        texts_file_path = os.path.join(Configuration().get_demos_home(), 'src', 'test', 'resources', 'process', 'archiving', text_folder)
        texts = []
        for text_file_name in os.listdir(texts_file_path):
            text = open(texts_file_path + '/' + text_file_name, 'r').read()
            texts.append(text)
        return texts


if __name__ == '__main__':
    unittest.main()
