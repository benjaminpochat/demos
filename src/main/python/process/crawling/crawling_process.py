from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Response
from src.main.python.commons.loggable import Loggable
from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.pdf_converter.pdf_converter import PdfConverter
from src.main.python.model.web_resource import WebDocument
from src.main.python.persistence.redis_access import RedisAccess


class LocalGovernmentPdfSpider(CrawlSpider):
    """
    A Scrapy spider that collects all pdf files found on a given domain
    """
    def __init__(self, args):
        super().__init__(self)
        self.local_government = args[0]
        self.start_urls = ['http://' + self.local_government.domain_name]
        self.allowed_domains = [self.local_government.domain_name]
        self.name = 'local_government_pdf_spider'
        self.redis_access = RedisAccess()

    rules = (
        Rule(LinkExtractor(allow=r'.*\.pdf$', deny_extensions=[]), callback='convert_and_save'),
        Rule(LinkExtractor())
    )

    def convert_and_save(self, response: Response):
        print('PDF found : ' + response.url)
        pdf_converter = PdfConverter()
        text_content = pdf_converter.convert(response.body)
        web_document = WebDocument(url=response.url, local_government=self.local_government, text_content=text_content)
        self.redis_access.store_aggregate(web_document)


class LocalGovernmentCrawlingProcess(Loggable):
    """
    A process that crawls a local government's domain, and collects all data that could be an official council meeting report
    """
    def __init__(self, local_government: LocalGovernment):
        super().__init__()
        self.local_government = local_government

    def crawl(self):
        crawler_process = CrawlerProcess()
        if(self.local_government.domain_name.__len__() < 1):
            raise Exception('Impossible to crawl local government \"'
                            + self.local_government.name
                            + '\" with id '
                            + self.local_government.name.get_id()
                            + 'because it has no domain name')
        crawler_process.crawl(LocalGovernmentPdfSpider, [self.local_government])
        self.log_info('Starts crawling domain \"' + self.local_government.domain_name + '\" for ' + self.local_government.name)
        crawler_process.start()
        self.log_info('Stops crawling domain \"' + self.local_government.domain_name + '\" for ' + self.local_government.name)
