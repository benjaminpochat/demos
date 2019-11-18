from src.main.python.model.local_government import LocalGovernment
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.commons.loggable import Loggable


class LocalGovernmentRedisSelector(Loggable):
    """
    A class to build a subset of the local governements.
    The selection is done :
    - from the domains if the attribute "domains" is set
    - randomly otherwise
    """
    def __init__(self, subset_size: int = 1, domains: list=[]):
        super().__init__()
        self._subset_size = subset_size
        self._domains = domains
        self._redis_access = RedisAccess()

    def select_local_governments(self):
        selected_subset = []
        if self._domains.__len__() > 0:
            self._feed_subset_from_domains(selected_subset)
        else:
            self._feed_subset_randomly(selected_subset)
        return selected_subset

    def _feed_subset_randomly(self, selected_subset):
        for i in range(0, self._subset_size):
            random_local_government = self._redis_access.get_random_aggregate(the_class=LocalGovernment)
            while self._is_random_local_government_not_acceptable(random_local_government=random_local_government,
                                                                  selected_subset=selected_subset):
                random_local_government = self._redis_access.get_random_aggregate(the_class=LocalGovernment)
            selected_subset.append(random_local_government)
            self.log_info(random_local_government.name + ' added to the local government subset.')

    def _feed_subset_from_domains(self, selected_subset):
        for domain in self._domains:
            self.log_debug('Finding local governement for domain ' + domain)
            local_government_keys = self._redis_access.search_aggregate_keys_by_attribute_value(LocalGovernment, 'domain_name', domain)
            for local_government_key in local_government_keys:
                self.log_debug('Loading local governement for key ' + local_government_key)
                local_government = self._redis_access.get_aggregate(LocalGovernment, local_government_key)
                selected_subset.append(local_government)
                self.log_info(local_government.name + ' added to the local government subset.')

    def _is_random_local_government_not_acceptable(self, random_local_government: LocalGovernment, selected_subset: list):
        return random_local_government.domain_name.__len__() < 1 or selected_subset.__contains__(random_local_government)
