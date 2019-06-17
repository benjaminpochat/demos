import unittest
from unittest.mock import MagicMock

from scrapy.http import Response

from main.python.model.local_government import LocalGovernment
from main.python.persistence.redis_access import RedisAccess
from main.python.process.pdf_converter.pdf_converter import PdfConverter
from main.python.process.training.training_data_producer.pdf_collector_spider import LocalGovernmentPdfCollectorSpider


class TestGovernmentPdfSpider(unittest.TestCase):
    def test_convert_and_save(self):
        # given
        spider = LocalGovernmentPdfCollectorSpider([LocalGovernment(name='Metz')])

        pdf_converter = PdfConverter()
        pdf_converter.convert = MagicMock(return_value='a text')
        spider.pdf_converter = pdf_converter

        redis_access = RedisAccess()
        redis_access.store_aggregate = MagicMock()
        spider.redis_access = redis_access

        response = Response(url='http://an.adresse.org')

        # when
        spider.convert_and_save(response=response)

        # then
        # Nothing to check

if __name__ == '__main__':
    unittest.main()
