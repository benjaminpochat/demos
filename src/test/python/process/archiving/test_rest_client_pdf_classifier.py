import unittest
from unittest.mock import Mock

from src.main.python.process.archiving.rest_client_pdf_classifier import RestClientPdfClassifier


class TestRestClientPdfClassifier(unittest.TestCase):

    def test_classify_official_city_council_report_should_be_classified_correctly(self):
        # given
        classifier = RestClientPdfClassifier()
        classifier.do_request_tensorflow_serving = Mock(return_value={'predictions': [[0.2]]})

        # when
        classification = classifier.classify(text_content='Il était une fois dans la ville de Foix...')

        # then
        self.assertFalse(classification.isOfficialCouncilReport())


if __name__ == '__main__':
    unittest.main()
