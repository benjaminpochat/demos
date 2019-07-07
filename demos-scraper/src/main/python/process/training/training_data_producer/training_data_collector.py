import sys

from src.main.python.commons.configuration import Configuration
from src.main.python.process.local_government_selection.local_government_redis_selector import LocalGovernmentRedisSelector
from src.main.python.commons.loggable import Loggable
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.process.training.training_data_producer.pdf_collector_spider import LocalGovernmentPdfCollectorSpider


class TrainingDataCollector(Loggable):
    def __init__(self, selector: LocalGovernmentRedisSelector):
        super().__init__()
        self._selector = selector
        self._selected_local_governments = []

    def _crawl_local_governments_web_sites(self):
        crawling_process = LocalGovernmentCrawlingProcess(
            local_governments=self._selected_local_governments,
            spider_class=LocalGovernmentPdfCollectorSpider)
        crawling_process.crawl()

    def collect(self):
        self._selected_local_governments = self._selector.select_local_governments()
        self._crawl_local_governments_web_sites()
