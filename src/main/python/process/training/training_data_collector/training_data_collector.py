from main.python.commons.loggable import Loggable
from main.python.model.local_government import LocalGovernment
from main.python.persistence.redis_access import RedisAccess
from main.python.process.crawling.crawling_process import LocalGovernmentCrawlingProcess


class TrainingDataCollector(Loggable):
    def __init__(self, subset_size: int = 1):
        super().__init__()
        self.subset_size = subset_size
        self._redis_access = RedisAccess()
        self._training_subset = []

    def _initilize_subset(self):
        for i in range(0, self.subset_size):
            random_local_government = self._redis_access.get_random_aggregate(the_class=LocalGovernment)
            while self._training_subset.__contains__(random_local_government):
                random_local_government = self._redis_access.get_random_aggregate(the_class=LocalGovernment)
            self.log_info(random_local_government.name + ' added randomly to the subset')
            self._training_subset.append(random_local_government)

    def _crawl_subset(self):
        for local_government in self._training_subset:
            crawling_process = LocalGovernmentCrawlingProcess(local_government=local_government)
            crawling_process.crawl()

    def collect(self):
        self._initilize_subset()
        self._crawl_subset()


if __name__ == '__main__':
    collector = TrainingDataCollector(subset_size=1)
    collector.collect()
