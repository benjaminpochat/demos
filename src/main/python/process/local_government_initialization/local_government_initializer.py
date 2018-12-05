import json
import requests
import unidecode
import re
import sys

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.local_government import LocalGovernment
from src.main.python.commons.loggable import Loggable


class LocalGovernmentInitializer(Loggable):
    _redis_access = RedisAccess()
    _number_of_communes = 0
    _number_of_domains_previously_searched = 0
    _number_of_domains_currently_searched = 0

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
            commune.name = commune_dict['fields']['nom_complet']
            commune.national_typology = commune_dict['fields']
            commune.id = 'fr-commune-' + commune_dict['recordid']
            self._redis_access.store_aggregate(commune)

    def update_communes_of_france_with_domains(self):
        communes = self._redis_access.list_aggregates(LocalGovernment, 'fr-commune*')
        self._number_of_communes = communes.__len__()
        for commune in communes:
            if commune.domain_searched is None or not commune.domain_searched:
                self.find_domain(commune)
                commune.domain_searched = True
                self._redis_access.store_aggregate(commune)
                self._number_of_domains_currently_searched = self._number_of_domains_currently_searched + 1
            else:
                self._number_of_domains_previously_searched = self._number_of_domains_previously_searched + 1
            self.log_info(str(self._number_of_domains_currently_searched)
                          + ' domains currently searched - '
                          + str(self._number_of_domains_previously_searched)
                          + ' domains previously searched - '
                          + str(self._number_of_communes)
                          + ' communes.')

    def find_domain(self, commune: LocalGovernment):
        self.log_info('Start finding domain for commune \"' + commune.get_id() + '\" (' + commune.name + ')')
        domain_tries = self.get_domain_tries(commune)
        commune.domain_name = None
        for domain in domain_tries:
            page_content = self.get_page(domain)
            if page_content is not None and self.is_official_commune_web_page(page_content, commune):
                self.log_info('\"' + domain + '\" found as domain_name for commune \"' + commune.get_id() + '\" (' + commune.name + ')')
                commune.domain_name = domain
                break
        if commune.domain_name is None:
            self.log_info('no domain found for commune \"' + commune.get_id() + '\" (' + commune.name + ')')

    def get_domain_tries(self, commune):
        ascii_names = self.get_ascii_commune_names(commune)
        domain_tries = []
        for ascii_name in ascii_names:
            domain_tries.append(ascii_name + '.fr')
            domain_tries.append('www.' + ascii_name + '.fr')
            domain_tries.append('ville-' + ascii_name + '.fr')
            domain_tries.append('www.ville-' + ascii_name + '.fr')
            domain_tries.append(ascii_name + '.org')
            domain_tries.append('www.' + ascii_name + '.org')
            domain_tries.append(ascii_name + '.com')
            domain_tries.append('www.' + ascii_name + '.com')
        return domain_tries

    def get_ascii_commune_names(self, commune):
        ascii_commune_name_url_compliant = unidecode.unidecode(commune.national_typology['nom_complet'].lower())
        ascii_commune_name_url_compliant = ascii_commune_name_url_compliant.replace(' ', '_')
        ascii_commune_name_url_compliant = ascii_commune_name_url_compliant.replace('-', '_')
        ascii_commune_name_url_compliant = ascii_commune_name_url_compliant.replace('\'', '_')
        ascii_commune_names_url_compliant = [ascii_commune_name_url_compliant]
        if ascii_commune_name_url_compliant.find('_') > -1:
            ascii_commune_names_url_compliant.append(ascii_commune_name_url_compliant.replace('_', '-'))
            ascii_commune_names_url_compliant.append(ascii_commune_name_url_compliant.replace('_', ''))
        return ascii_commune_names_url_compliant

    def get_page(self, url: str):
        self.log_debug('Try to request \"' + url + '\"')
        try:
            response = requests.get('http://' + url, allow_redirects=False, timeout=60)
            content = response.text
        except Exception as e:
            self.log_debug('Failed to request \"' + url + '\"')
            self.log_debug(e.__str__())
            content = None
        self.log_debug('Successed to request \"' + url + '\"')
        return content

    def is_official_commune_web_page(self, page_content, commune):
        # Contains 'commune' or 'mairie' or 'municipal'
        page_content_lower_cased = page_content.lower()
        is_official_web_page = self._is_key_words_contained_in_page(page_content_lower_cased)
        is_official_web_page = is_official_web_page and self.is_commune_full_name_contained_in_page(commune, page_content_lower_cased)
        return is_official_web_page

    def is_commune_full_name_contained_in_page(self, commune, page_content_lower_cased):
        commune_full_name = commune.national_typology['nom_complet']
        commune_full_name_regex = re.compile(commune_full_name.replace('-', '[ -]'), re.IGNORECASE)
        return commune_full_name_regex.search(page_content_lower_cased) != None

    def _is_key_words_contained_in_page(self, page_content_lower_cased):
        return page_content_lower_cased.find('commune') > -1 \
               or page_content_lower_cased.find('mairie') > -1 \
               or page_content_lower_cased.find('municipal') > -1


if __name__ == '__main__':
    if sys.argv.__contains__('-h'):
        print('Command line for initializing the list of french communes with their domain names in database')
        print('Preresites : start the database, see start_sb.sh script')
        print('Usage : init_french_communes [opt]')
        print('Options :')
        print('  -R reset the data')
        print('')
    initializer = LocalGovernmentInitializer()
    initializer.log_info('Starting initialization of french communes')
    if sys.argv.__contains__('-R'):
        initializer.store_communes_of_france()
    initializer.update_communes_of_france_with_domains()
