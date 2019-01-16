import sys

from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.archiving.pdf_archiving_spider import LocalGovernmentPdfArchivingSpider
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.commons.configuration import Configuration
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.commons.loggable import Loggable


class DelibArchiver(Loggable):

    def __init__(self):
        super().__init__()

    def log_configuration(self):
        self.log_info('Starting with the following configuration :')
        for attribute_key in Configuration().__dict__.keys():
            attribute_value = Configuration().__dict__[attribute_key]
            self.log_info(attribute_key + '=' + attribute_value)


if __name__ == '__main__':
    print('Welcome in the local government_archiver process.')
    Configuration(sys.argv[1:])
    archiver = DelibArchiver()
    archiver.log_configuration()
    redis_access = RedisAccess()
    random_local_governments = redis_access.get_random_aggregate(the_class=LocalGovernment)
    crawling_process = LocalGovernmentCrawlingProcess(
        local_governments=[random_local_governments],
        spider_class=LocalGovernmentPdfArchivingSpider)
    #crawling_process.crawl()
