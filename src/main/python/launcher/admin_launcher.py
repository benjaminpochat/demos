from src.main.python.model.web_resource import WebDocument
from src.main.python.model.local_government import LocalGovernment
from src.main.python.persistence.redis_index_manager import RedisIndexManager
from src.main.python.process.local_government_initialization.local_government_initializer import LocalGovernmentInitializer
from src.main.python.commons.configuration import Configuration


class AdminLauncher:
    def __init__(self, options: list):
        self.options = options

    def launch(self):
        if self.options.__len__() == 0 or self.options[0] == '-h':
            self.print_manual_page()
        elif self.options[0] == 'init_data':
            self.start_initializing_data()
        elif self.options[0] == 'update_indices':
            self.start_updating_indices()
        else:
            print('The command ' + self.options[0] + ' is not defined as a Demos rebase command.')
            print('Please see manual page running "demos train -h"')

    def start_initializing_data(self):
        print(self.options)
        print('Are you sure you want to initialize the root data of your database ?')
        print('The list of the web sites to crawl will be updated')
        input('[Ctrl+C : stop | Any other key : continue]')
        Configuration(self.options)
        initializer = LocalGovernmentInitializer()
        initializer.log_info('Starting initialization of french communes')
        initializer.store_communes_of_france()
        initializer.create_index_on_domain_name()

    def start_updating_indices(self):
        Configuration(self.options)
        index_manager = RedisIndexManager()
        index_manager.update_index(LocalGovernment, 'domain_name')
        index_manager.update_index(WebDocument, 'classified_as_official_report')
        index_manager.update_index(WebDocument, 'local_government')

    @staticmethod
    def print_manual_page():
        print('')
        print('-- Welcome in Demos admin manual page ! --')
        print('')
        print('Usage : demos admin [command]')
        print('')
        print('The commands available are :')
        print('')
        print('  "update_indices" : Updates database indices.')
        print('')
        print('  "init_data" : Initialize into database the data necessary to start scraping, classifying, and training.')
        print('              The data initialized are :')
        print('              - the list of local government (french communes)')
        print('              - the domain names of official web sites for each local government')
        print('              CAUTION : If your database is not empty, this will screw up your data !')
        print('')
