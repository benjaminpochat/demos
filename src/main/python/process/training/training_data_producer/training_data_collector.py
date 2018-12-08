import sys

from src.main.python.commons.loggable import Loggable
from src.main.python.model.local_government import LocalGovernment
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess


class TrainingDataCollector(Loggable):
    def __init__(self, subset_size: int = 1, domains: list=[]):
        super().__init__()
        self._subset_size = subset_size
        self._domains = domains
        self._redis_access = RedisAccess()
        self._training_subset = []

    def _initilize_subset(self):
        for domain in self._domains:
            all_local_governments = self._redis_access.list_aggregates(the_class=LocalGovernment)
            local_government = None
            i = 0
            while local_government is None and i < all_local_governments.__len__():
                if all_local_governments[i].domain_name == domain:
                    local_government = all_local_governments[i]
                i += 1
            if local_government is None:
                raise Exception('No local government exist for the domain ' + domain)
            self._training_subset.append(local_government)

        for i in range(0, self._subset_size):
            random_local_government = self._redis_access.get_random_aggregate(the_class=LocalGovernment)
            while self._is_random_local_government_not_acceptable(random_local_government):
                random_local_government = self._redis_access.get_random_aggregate(the_class=LocalGovernment)
            self.log_info(random_local_government.name + ' added randomly to the subset')
            self._training_subset.append(random_local_government)
            print(random_local_government.name + ' added to the local government to crawl.')

    def _is_random_local_government_not_acceptable(self, random_local_government:LocalGovernment):
        return random_local_government.domain_name.__len__() < 1 or self._training_subset.__contains__(random_local_government)

    def _crawl_subset(self):
        crawling_process = LocalGovernmentCrawlingProcess(local_governments=self._training_subset)
        crawling_process.crawl()

    def collect(self):
        self._initilize_subset()
        self._crawl_subset()


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
        collector = TrainingDataCollector(subset_size=subset_size, domains=domains)
        collector.collect()
