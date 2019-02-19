import sys

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.persistence.redis_index_manager import RedisIndexManager
from src.main.python.model.local_government import LocalGovernment
from src.main.python.commons.loggable import Loggable


class LocalGovernmentInitializer(Loggable):
    _redis_access = RedisAccess()

    def store_communes_of_france(self):
        """
        Importing communes of France from the file data/local_gov_list/france/communes/fr_communes.csv
        """
        data_file = open('./data/local_gov_list/france/communes/fr_communes.csv', 'r')
        for line in data_file :
            self.log_debug('Reading line : ' + line)
            values = line.split(";")
            commune = LocalGovernment()
            commune.id = 'fr-commune-' + values[0].strip()
            commune.name = values[1].strip()
            commune.domain_name = values[2].strip().replace('http://', '').replace('https://', '')
            self._redis_access.store_aggregate(commune)
        data_file.close()

    def create_index_on_domain_name(self):
        index_manager = RedisIndexManager()
        index_manager.drop_index(LocalGovernment, 'domain_name')
        index_manager.create_index(LocalGovernment, 'domain_name')


if __name__ == '__main__':
    if sys.argv.__contains__('-h'):
        print('Command line for initializing the list of french communes with their domain names in database')
        print('Preresites : start the database, see start_sb.sh script')
        print('')
    initializer = LocalGovernmentInitializer()
    initializer.log_info('Starting initialization of french communes')
    initializer.store_communes_of_france()
    initializer.create_index_on_domain_name()



