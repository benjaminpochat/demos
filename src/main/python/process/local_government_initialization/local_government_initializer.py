from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.persistence.redis_index_manager import RedisIndexManager
from src.main.python.model.local_government import LocalGovernment
from src.main.python.commons.loggable import Loggable


class LocalGovernmentInitializer(Loggable):


    def store_communes_of_france(self):
        """
        Importing communes of France from the file data/local_gov_list/france/communes/fr_communes.csv
        """
        data_file = open('./data/local_gov_list/france/communes/fr_communes.csv', 'r')
        redis_access = RedisAccess()
        for line in data_file :
            self.log_debug('Reading line : ' + line.strip())
            values = line.split(";")
            commune = LocalGovernment()
            commune.id = 'fr-commune-' + values[0].strip()
            commune.name = values[1].strip()
            commune.domain_name = values[2].strip()
            redis_access.store_aggregate(commune)
        data_file.close()

    def create_index_on_domain_name(self):
        index_manager = RedisIndexManager()
        index_manager.drop_index(LocalGovernment, 'domain_name')
        index_manager.create_index(LocalGovernment, 'domain_name')
