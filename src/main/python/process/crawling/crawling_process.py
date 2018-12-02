from scrapy.crawler import CrawlerProcess
from src.main.python.commons.loggable import Loggable
from src.main.python.model.local_government import LocalGovernment
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Response


class PdfSpider(CrawlSpider):
    """
    A Scrapy spider that collects all pdf files found on a given domain
    """
    def __init__(self, *args, **kwargs):
        super(PdfSpider, self).__init__(self)
        self.start_urls = [kwargs.get('start_url')]
        self.allowed_domains = [kwargs.get('allowed_domain')]
        self.name = 'pdf_spider'

    rules = (
        Rule(LinkExtractor(allow=r'.*\.pdf$', deny_extensions=[]), callback='convert_and_save'),
        Rule(LinkExtractor())
    )

    def convert_and_save(self, response: Response):
        print('PDF found : ' + response.url)


class LocalGovernmentCrawlingProcess(Loggable):
    """
    A process that crawls local government's domain, and collects all data that could be an official council meeting report
    """
    def __init__(self, local_government: LocalGovernment):
        super().__init__()
        self.local_government = local_government

    def crawl(self):
        crawler_process = CrawlerProcess()
        domain = self.local_government.domain_name
        start_url = 'http://' + domain
        crawler_process.crawl(PdfSpider, allowed_domain=domain, start_url=start_url)
        self.log_info('Start crawling domain \"' + self.local_government.domain_name + '\"')
        crawler_process.start()
        self.log_info('Stop crawling domain \"' + self.local_government.domain_name + '\"')


if __name__ == '__main__':
    commune_bechy = LocalGovernment()
    commune_bechy.domain_name = 'bechy.fr'
    crawling_process = LocalGovernmentCrawlingProcess(commune_bechy)
    crawling_process.crawl()
