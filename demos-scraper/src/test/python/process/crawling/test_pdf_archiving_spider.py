import json
import unittest

import requests
from mock import Mock

from src.main.python.model.web_resource import WebDocument
from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.archiving.pdf_archiving_spider import LocalGovernmentPdfArchivingSpider


class TestPdfArchivingSpider(unittest.TestCase):
    def test_save_official_council_report(self):
        # Given
        local_government = LocalGovernment(name='Aix-en-Provence', domain_name='www.aix.fr', ident='123')
        pdf_archiving_spider = LocalGovernmentPdfArchivingSpider([local_government, None])
        pdf_archiving_spider._call_rest_service = Mock()

        # When
        pdf_archiving_spider.save_official_council_report(url='www.aix.fr/cm_20190709', text_content='Seance du 09/07/2019')

    def test_get_rest_service_json_content(self):
        # Given
        local_government = LocalGovernment(name='Aix-en-Provence', domain_name='www.aix.fr', ident='123')
        web_document = WebDocument(text_content='Seance du 09/07/2019', url='www.aix.fr/cm_20190709', ident='ABC')
        web_document.local_government = local_government
        pdf_archiving_spider = LocalGovernmentPdfArchivingSpider([local_government, None])

        # When
        json_content = pdf_archiving_spider._get_rest_service_content(web_document=web_document)

        # Then
        self.assertEquals(json.loads(json_content), {"url": "www.aix.fr/cm_20190709", "id": "ABC", "localGovernment": {"id": "123"}})

    def test_call_rest_service(self):
        local_government = LocalGovernment(name='Aix-en-Provence', domain_name='www.aix.fr', ident='123')
        web_document = WebDocument(text_content='Seance du 09/07/2019', url='www.aix.fr/cm_20190709', ident='ABC')
        web_document.local_government = local_government
        pdf_archiving_spider = LocalGovernmentPdfArchivingSpider([local_government, None])
        url = pdf_archiving_spider._get_rest_service_url()
        data = pdf_archiving_spider._get_rest_service_content(web_document=web_document)

        # When
        print('Sending POST request :')
        print('- url : ' + url)
        print('- content : ' + json.dumps(data))
        response = pdf_archiving_spider._call_rest_service(url=url, data=data)

        # Then
        self.assertEquals(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
