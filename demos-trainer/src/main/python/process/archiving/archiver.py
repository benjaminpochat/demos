from src.main.python.process.local_government_selection.local_government_rest_selector import LocalGovernmentScrappingRestSelector
from src.main.python.process.archiving.pdf_archiving_spider import LocalGovernmentPdfArchivingSpider
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.commons.loggable import Loggable


class DelibArchiver(Loggable):

    def __init__(self, classifier_class, local_governments_selector: LocalGovernmentScrappingRestSelector):
        super().__init__()
        self._local_governments_selector = local_governments_selector
        self._classifier_class = classifier_class

    def archive(self):
        local_governments = self._local_governments_selector.select_local_governments()
        self._crawl_local_governments_web_site(local_governments)

    def _crawl_local_governments_web_site(self, local_governments):
        crawling_process = LocalGovernmentCrawlingProcess(
            local_governments=local_governments,
            spider_class=LocalGovernmentPdfArchivingSpider,
            classifier_class=self._classifier_class)
        crawling_process.crawl()
