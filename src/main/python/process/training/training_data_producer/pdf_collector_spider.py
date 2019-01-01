from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from src.main.python.model.web_resource import WebDocument
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.process.pdf_converter.pdf_converter import PdfConverter


class LocalGovernmentPdfCollectorSpider(CrawlSpider):
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
        self.pdf_converter = PdfConverter(timeout=300)

    rules = (
        Rule(LinkExtractor(allow=r'.*\.pdf$', deny_extensions=[]), callback='convert_and_save'),
        Rule(LinkExtractor())
    )

    def convert_and_save(self, response: Response):
        print('PDF found : ' + response.url)
        text_content = self.pdf_converter.convert(response.body)
        web_document = WebDocument(url=response.url, local_government=self.local_government, text_content=text_content)
        web_document.generate_id()
        self.redis_access.store_aggregate(web_document)