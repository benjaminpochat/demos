import json
from src.main.python.persistence.redis_access import RedisAccess

from src.main.python.model.local_government import LocalGovernment


class LocalGovernmentInitializer():

    _redis_access = RedisAccess()

    def store_data(self):
        self.store_communes_of_france()

    def store_communes_of_france(self):
        data_file = open('../../../../../data/local_gov_list/france/communes/liste-des-communes-francaises.json', 'r')
        data = json.load(data_file)
        for commune_dict in data:
            commune = LocalGovernment()
            commune.name = commune_dict['fields']['nom_complet']
            commune.national_typology = commune_dict['fields']
            commune.id = 'fr-commune-' + commune_dict['recordid']
            self._redis_access.store_agregate(commune)


if __name__ == '__main__':
    initializer = LocalGovernmentInitializer()
    initializer.store_data()
