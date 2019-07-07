import unittest
import json
from mock import Mock
import requests as requests

from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.local_government_selection.local_government_rest_selector import LocalGovernmentScrappingRestSelector


class TestLocalGovernmentScrappingRestSelector(unittest.TestCase):
    def test_get_local_government_for_scraping(self):
        # Given
        selector = LocalGovernmentScrappingRestSelector()
        json_decoder = json.JSONDecoder()
        mocked_response = requests.Response()
        mocked_response.status_code = 200
        mocked_response.json = Mock(return_value=json_decoder.decode('{"id": 19852, "webSite": "lupcourt.com", "name": "Lupcourt", "type": "FRANCE_COMMUNE", "latitude": 6.20364, "longitude": 48.6255, "codification": "54330"}'))
        selector._call_rest_service = Mock(return_value=mocked_response)

        # When
        local_government = selector.get_local_governments_for_scraping()

        # Then
        self.assertIsInstance(local_government, LocalGovernment)
        self.assertEquals(local_government.id, '19852')
        self.assertEquals(local_government.name, 'Lupcourt')
        self.assertEquals(local_government.domain_name, 'lupcourt.com')


if __name__ == '__main__':
    unittest.main()
