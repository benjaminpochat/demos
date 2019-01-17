import sys

from src.main.python.process.local_government_selection.local_government_selector import LocalGovernmentSelector
from src.main.python.process.archiving.pdf_archiving_spider import LocalGovernmentPdfArchivingSpider
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess
from src.main.python.commons.configuration import Configuration
from src.main.python.commons.loggable import Loggable


class DelibArchiver(Loggable):

    def __init__(self, selector: LocalGovernmentSelector):
        super().__init__()
        self._selector = selector
        self._selected_local_governments = []

    def archive(self):
        self._selected_local_governments = self._selector.select_local_governments()
        self._crawl_local_governments_web_sites()

    def _crawl_local_governments_web_sites(self):
        crawling_process = LocalGovernmentCrawlingProcess(
            local_governments=self._selected_local_governments,
            spider_class=LocalGovernmentPdfArchivingSpider)
        crawling_process.crawl()


if __name__ == '__main__':
    print('Welcome in the local government archiver process.')
    if sys.argv.__contains__('-h'):
        print('Command line to store in tha database all the official council reports found in the local governments\' web sites')
        print('Preresites : start the database')
        print('Usage : sh archiver.sh [opt]')
        print('Options :')
        print('  -d <domain name> : a particular domain to crawl. Must match a local government.\n'
              '     By default, the process chooses the local governement randomly')
        print('  -n <number> : the number of local governments\' web sites to crawl (default is 1)\n'
              '     Ignored if the parameter -d is used\n'
              '     By default, the process never ends (value -1).')
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
        print('Start archiving data...')
        print('[ Ctrl + C ] to quit')
        selector = LocalGovernmentSelector(subset_size=subset_size, domains=domains)
        archiver = DelibArchiver(selector=selector)
        Configuration(sys.argv[1:])
        archiver.archive()
