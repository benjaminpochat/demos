from scrapy.crawler import CrawlerProcess

from src.main.python.commons.loggable import Loggable
from src.main.python.model.local_government import LocalGovernment


class LocalGovernmentCrawlingProcess(Loggable):
    """
    A process that crawls a local government's domain,
    and apply the process implemented in the spider class given as attribute
    """
    def __init__(self, local_governments: list, spider_class, classifier_class):
        super().__init__()
        self.local_governments = local_governments
        self.spider_class = spider_class
        self.classifier_class = classifier_class
        self.crawler_process = CrawlerProcess()

    def crawl(self):
        for local_government in self.local_governments:
            self._add_local_government_to_crawl(local_government)
        self.crawler_process.start()

    def _add_local_government_to_crawl(self, local_government: LocalGovernment):
        if local_government.domain_name.__len__() < 1:
            exception = Exception('Impossible to crawl local government \"'
                            + local_government.name
                            + '\" with id \''
                            + local_government.get_id()
                            + '\' because it has no domain name')
            self.log_error(exception)
            raise exception
        self.crawler_process.crawl(self.spider_class, [local_government, self.classifier_class])
