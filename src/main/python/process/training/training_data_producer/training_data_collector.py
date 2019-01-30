import sys

from src.main.python.commons.configuration import Configuration
from src.main.python.process.local_government_selection.local_government_selector import LocalGovernmentSelector
from src.main.python.commons.loggable import Loggable
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.process.training.training_data_producer.pdf_collector_spider import LocalGovernmentPdfCollectorSpider


class TrainingDataCollector(Loggable):
    def __init__(self, selector: LocalGovernmentSelector):
        super().__init__()
        self._selector = selector
        self._selected_local_governments = []

    def _crawl_local_governments_web_sites(self):
        crawling_process = LocalGovernmentCrawlingProcess(
            local_governments=self._selected_local_governments,
            spider_class=LocalGovernmentPdfCollectorSpider)
        crawling_process.crawl()

    def collect(self):
        self._selected_local_governments = self._selector.select_local_governments()
        self._crawl_local_governments_web_sites()


if __name__ == '__main__':
    if sys.argv.__contains__('-h'):
        print('Command line for collecting pdf content from french communes web sites, in order to be classified and to train machine learning model')
        print('Preresites : start the database, see start_sb.sh script')
        print('Usage : sh collect_local_government_pdf_content.sh [opt]')
        print('Options :')
        print('  -n <number> : the number of local governments\' web sites to crawl (default is 1)')
        print('  -d <domain name> : a particular domain to crawl. Must match a local government.')
        print('')
    else:
        subset_size = 1
        domains = []
        if sys.argv.__contains__('-d'):
            n_option_index = sys.argv.index('-d')
            domains.append(sys.argv[n_option_index + 1])
        elif sys.argv.__contains__('-n'):
            n_option_index = sys.argv.index('-n')
            subset_size = int(sys.argv[n_option_index + 1])
        print('Start collecting data...')
        print('[ Ctrl + C ] to quit')
        Configuration(sys.argv[1:])
        selector = LocalGovernmentSelector(subset_size=subset_size, domains=domains)
        collector = TrainingDataCollector(selector=selector)
        collector.collect()
