from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from src.main.python.process.archiving.pdf_classifier import LocalGovernmentPdfClassifier
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.process.pdf_converter.pdf_converter import PdfConverter


class LocalGovernmentPdfArchivingSpider(CrawlSpider):
    """
    A Scrapy spider that stores the pdf content if it's classified as official council report by machine learning model
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
        Rule(LinkExtractor(allow=r'.*\.pdf$', deny_extensions=[]), callback='process_pdf'),
        Rule(LinkExtractor())
    )

    def process_pdf(self, response: Response):
        """
        The following process is applied to the response content (considered as pdf content) :
        - 1 : converting pdf content as text
        - 2 : applying machine learning classification model
        - 3 : if the content is considered as a document to archive (an official council report fo instance, containing deliberations), then saving the document into database, bound to the local government
        :param response: the http response obtained from the spider rule (pdf content)
        :return: nothing
        """
        print('PDF found : ' + response.url)
        classifier = LocalGovernmentPdfClassifier()
        classification = classifier.classify(response.body)
        if classification.isOfficialCouncilReport():
            self.saveOfficialCouncilReport(response.url)

    def saveOfficialCouncilReport(self, url):
        pass
