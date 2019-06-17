from src.main.python.process.local_government_selection.local_government_selector import LocalGovernmentSelector
from src.main.python.process.archiving.pdf_archiving_spider import LocalGovernmentPdfArchivingSpider
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.commons.loggable import Loggable


class DelibArchiver(Loggable):

    def __init__(self, selector: LocalGovernmentSelector, classifier_class):
        super().__init__()
        self._selector = selector
        self.classifier_class = classifier_class
        self._selected_local_governments = []

    def archive(self):
        self._selected_local_governments = self._selector.select_local_governments()
        self._crawl_local_governments_web_sites()

    def _crawl_local_governments_web_sites(self):
        crawling_process = LocalGovernmentCrawlingProcess(
            local_governments=self._selected_local_governments,
            spider_class=LocalGovernmentPdfArchivingSpider,
            classifier_class=self.classifier_class)
        crawling_process.crawl()
