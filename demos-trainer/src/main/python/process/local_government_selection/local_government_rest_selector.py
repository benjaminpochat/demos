import requests as requests
import time as time

from src.main.python.commons.configuration import Configuration
from src.main.python.model.local_government import LocalGovernment
from src.main.python.commons.loggable import Loggable


class LocalGovernmentScrappingRestSelector(Loggable):

    def __init__(self, subset_size: int = 1, web_site: str = None):
        super().__init__()
        self._subset_size = subset_size
        self._web_site = web_site

    def select_local_governments(self):
        local_governments = []
        if self._web_site is not None:
            local_governments.append(self._select_local_government_from_web_site())
        else:
            local_governments = self._select_local_governments_randomly()
        self.log_info('Local governments selects to be scraped :')
        for local_government in local_governments:
            self.log_info('* ' + local_government.name + '(' + local_government.domain_name + ')')
        return local_governments

    def _select_local_governments_randomly(self):
        demos_core_host = Configuration().get_demos_core_host()
        demos_core_port = Configuration().get_demos_core_port()
        url = 'http://' + demos_core_host + ':' + demos_core_port + '/localGovernments/forScraping?size=' + str(self._subset_size)
        response = self._call_rest_service(url)
        local_government = self._map_rest_response(response)
        return local_government

    def _select_local_government_from_web_site(self):
        demos_core_host = Configuration().get_demos_core_host()
        demos_core_port = Configuration().get_demos_core_port()
        url = 'http://' + demos_core_host + ':' + demos_core_port + '/localGovernments?webSite=' + self._web_site
        response = self._call_rest_service(url)
        local_government = self._map_rest_response(response)
        return local_government

    def _call_rest_service(self, url):
        response = None
        number_of_retries = 60
        timeout_in_secondes = 1
        for i in range(1, number_of_retries):
            try:
                response = requests.get(url=url)
            except requests.exceptions.ConnectionError as e:
                self.log_info('GET ' + url + ' raised ConnectionError - try #' + str(i) + ' - next retry in ' + str(timeout_in_secondes) + ' seconds')
                time.sleep(timeout_in_secondes)
        if response is None:
            self.log_error('GET ' + url + ' do not respond after ' + str(number_of_retries * timeout_in_secondes) + ' seconds')
            raise requests.exceptions.ConnectionError
        elif response.status_code != 200:
            self.log_error('GET ' + url + ' status : {}'.format(response.status_code))
            self.log_error('GET ' + url + ' response : {}'.format(response.json()))
        else:
            self.log_debug('GET ' + url + ' status : {}'.format(response.status_code))
            self.log_debug('GET ' + url + ' response : {}'.format(response.json()))
        return response

    def _map_rest_response(self, response: requests.Response):
        local_governments = []
        for element in response.json():
            local_government = LocalGovernment()
            local_government.domain_name = element['webSite']
            local_government.id = str(element['id'])
            local_government.name = element['name']
            local_governments.append(local_government)
        return local_governments

