import json
import requests
import socket
import unidecode

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.local_government import LocalGovernment


class LocalGovernmentInitializer():
    _redis_access = RedisAccess()

    def store_data(self):
        self.store_communes_of_france()

    def store_communes_of_france(self):
        """
        Importing communes of France.
        The official data is given there ; https://www.insee.fr/fr/information/2114819
        We use the data given here as they are formatted in json : https://public.opendatasoft.com/explore/dataset/liste-des-communes-francaises
        :return:
        """
        data_file = open(
            '../../../../../data/local_gov_list/france/communes/liste-des-communes-francaises-converted.json', 'r')
        data = json.load(data_file)
        for commune_dict in data:
            commune = LocalGovernment()
            commune.name = commune_dict['fields']['nomcomplet']
            commune.national_typology = commune_dict['fields']
            commune.id = 'fr-commune-' + commune_dict['recordid']
            self._redis_access.store_aggregate(commune)

    def find_domain(self, commune: LocalGovernment):
        domain_tries = self.get_domain_tries(commune)
        for domain in domain_tries:
            page_content = self.get_page(domain)
            if page_content is not None and self.is_official_commune_web_page(page_content, commune):
                return domain

    def get_domain_tries(self, commune):
        ascii_names = self.get_ascii_commune_names(commune)
        domain_tries = []
        for ascii_name in ascii_names:
            domain_tries.append(ascii_name + '.fr')
            domain_tries.append(ascii_name + '.org')
            domain_tries.append(ascii_name + '.com')
            domain_tries.append('ville-' + ascii_name + '.fr')
        return domain_tries

    def get_ascii_commune_names(self, commune):
        ascii_commune_name_url_compliant = unidecode.unidecode(commune.national_typology['nomcomplet'].lower())
        ascii_commune_name_url_compliant = ascii_commune_name_url_compliant.replace(' ', '_')
        ascii_commune_name_url_compliant = ascii_commune_name_url_compliant.replace('-', '_')
        ascii_commune_name_url_compliant = ascii_commune_name_url_compliant.replace('\'', '_')
        ascii_commune_names_url_compliant = [ascii_commune_name_url_compliant]
        if ascii_commune_name_url_compliant.find('_') > -1:
            ascii_commune_names_url_compliant.append(ascii_commune_name_url_compliant.replace('_', '-'))
            ascii_commune_names_url_compliant.append(ascii_commune_name_url_compliant.replace('_', ''))
        return ascii_commune_names_url_compliant

    def get_page(self, url: str):
        try:
            response = requests.get('http://' + url)
            content = response.text
        except requests.exceptions.ConnectionError:
            content = None
        return content

    def is_official_commune_web_page(self, page_content, commune):
        # Contains 'commune' or 'mairie' or 'municipal'
        page_content_lower_cased = page_content.lower()
        is_official_web_page = page_content_lower_cased.find('commune') > -1 \
                               or page_content_lower_cased.find('mairie') > -1 \
                               or page_content_lower_cased.find('municipal') > -1
        # Contains commune's full name
        is_official_web_page = is_official_web_page \
                               and page_content_lower_cased.find(commune.national_typology['nomcomplet'].lower()) > -1
        return is_official_web_page


if __name__ == '__main__':
    initializer = LocalGovernmentInitializer()
    initializer.store_data()
