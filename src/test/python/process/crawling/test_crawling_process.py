import unittest

from unittest.mock import MagicMock

from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.pdf_converter.pdf_converter import PdfConverter
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.process.crawling.crawling_process import LocalGovernmentPdfSpider
from src.main.python.persistence.redis_access import RedisAccess
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response



class TestLocalGovernmentCrawlingProcess(unittest.TestCase):
    def test_crawl_should_raise_error_if_domain_name_absent(self):
        # given
        local_governments = [LocalGovernment(ident='1', name='Agen'), LocalGovernment(ident='2', name='Caen')]
        crawling_process = LocalGovernmentCrawlingProcess(local_governments=local_governments)
        crawler_process = CrawlerProcess()
        crawler_process.crawl = MagicMock()
        crawler_process.start = MagicMock()

        # when
        with self.assertRaises(Exception) as cm:
            crawling_process.crawl()

        # then
        exception = cm.exception
        self.assertEqual(exception.args[0], 'Impossible to crawl local government "Agen" with id \'1\' because it has no domain name')

class TestGovernmentPdfSpider(unittest.TestCase):
    def test_convert_and_save(self):
        # given
        spider = LocalGovernmentPdfSpider([LocalGovernment(name='Metz')])

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
