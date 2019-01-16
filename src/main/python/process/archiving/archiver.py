import sys
import logging

from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.archiving.pdf_archiving_spider import LocalGovernmentPdfArchivingSpider
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.commons.configuration import Configuration
from src.main.python.persistence.redis_access import RedisAccess


def log_configuration():
    print('Starting with the following configuration :')
    for attribute_key in configuration.__dict__.keys():
        attribute_value = configuration.__dict__[attribute_key]
        print(attribute_key + '=' + attribute_value)


if __name__ == '__main__':
    print('Welcome in the local government_archiver process.')
    configuration = Configuration(sys.argv[1:])
    log_configuration()
    redis_access = RedisAccess()
    random_local_governments = redis_access.get_random_aggregate(the_class=LocalGovernment)
    crawling_process = LocalGovernmentCrawlingProcess(
        local_governments=[random_local_governments],
        spider_class=LocalGovernmentPdfArchivingSpider)
    #crawling_process.crawl()
