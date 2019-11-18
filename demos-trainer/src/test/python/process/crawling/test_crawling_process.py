import unittest

from unittest.mock import MagicMock

from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from main.python.process.training.training_data_producer.pdf_collector_spider import LocalGovernmentPdfCollectorSpider
from scrapy.crawler import CrawlerProcess


class TestLocalGovernmentCrawlingProcess(unittest.TestCase):
    def test_crawl_should_raise_error_if_domain_name_absent(self):
        # given
        local_governments = [LocalGovernment(ident='1', name='Agen'), LocalGovernment(ident='2', name='Caen')]
        crawling_process = LocalGovernmentCrawlingProcess(
            local_governments=local_governments,
            spider_class=LocalGovernmentPdfCollectorSpider)
        crawler_process = CrawlerProcess()
        crawler_process.crawl = MagicMock()
        crawler_process.start = MagicMock()

        # when
        with self.assertRaises(Exception) as cm:
            crawling_process.crawl()

        # then
        exception = cm.exception
        self.assertEqual(exception.args[0], 'Impossible to crawl local government "Agen" with id \'1\' because it has no domain name')


if __name__ == '__main__':
    unittest.main()
