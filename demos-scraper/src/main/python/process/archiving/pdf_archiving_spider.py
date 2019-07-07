import json

import requests
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from src.main.python.commons.configuration import Configuration
from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.web_resource import WebDocument
from src.main.python.commons.loggable import Loggable
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.process.pdf_converter.pdf_converter import PdfConverter


class LocalGovernmentPdfArchivingSpider(CrawlSpider, Loggable):
    """
    A Scrapy spider that stores the pdf content if it's classified as official council report by machine learning model
    """
    def __init__(self, args):
        CrawlSpider.__init__(self, args)
        Loggable.__init__(self)
        self.local_government = args[0]
        self.classifier_class = args[1]
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
        self.log_info('PDF found : ' + response.url)
        classifier = self.classifier_class()
        text_content = self.pdf_converter.convert(response.body)
        classification = classifier.classify(text_content)
        if classification.isOfficialCouncilReport():
            self.log_info('The PDF at ' + response.url + ' has been classified as an official city council report')
            self.save_official_council_report(response.url, text_content)
        else:
            self.log_info('The PDF at ' + response.url + ' has not been classified as an official city council report')
        self.log_info('gc.garbage = ')

    def save_official_council_report(self, url: str, text_content: str):
        self.log_info("Saving WebDocument with url " + url)
        official_council_report = self._generate_web_document(text_content, url)
        url = self._get_rest_service_url()
        content = self._get_rest_service_content(official_council_report)
        self.log_debug('Sending POST request :')
        self.log_debug('- url : ' + url)
        self.log_debug('- content : ' + json.dumps(content))
        self._call_rest_service(url=url, data=content)

    def _generate_web_document(self, text_content, url):
        official_council_report = WebDocument(
            text_content=text_content,
            url=url,
            local_government=self.local_government)
        official_council_report.classified_as_official_report = Boolean.TRUE
        official_council_report.id = official_council_report.generate_id()
        return official_council_report

    def _get_rest_service_url(self):
        demos_core_host = Configuration().get_demos_core_host()
        demos_core_port = Configuration().get_demos_core_port()
        url = 'http://' + demos_core_host + ':' + demos_core_port + '/webDocuments'
        return url

    def _get_rest_service_content(self, web_document: WebDocument):
        return {
            'url': web_document.url,
            'localGovernment':
                {'id': web_document.local_government.id},
            'id': web_document.id}

    def _call_rest_service(self, url: str, data: dict):
        response = requests.post(url=url,
                                 json=data,
                                 headers={
                                     'Accept': 'application/json, text/plain, */*',
                                     'Content-Type': 'application/json;charset=utf-8'
                                 })
        if response.status_code != 200:
            self.log_error('POST ' + url + ' status : {}'.format(response.status_code))
        else:
            self.log_debug('POST ' + url + ' status : {}'.format(response.status_code))
        return response

