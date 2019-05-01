import os

from src.main.python.launcher.launcher import Launcher, ManualPage, Command
from src.main.python.model.web_resource import WebDocument
from src.main.python.model.local_government import LocalGovernment
from src.main.python.persistence.redis_index_manager import RedisIndexManager
from src.main.python.process.local_government_initialization.local_government_initializer import \
    LocalGovernmentInitializer
from src.main.python.commons.configuration import Configuration


class AdminLauncher(Launcher):
    """
    A launcher for the administration features.
    """

    INITIALIZE_DATA_COMMAND = 'init_data'
    UPDATE_INDICES_COMMAND = 'update_indices'

    def __init__(self, args: list):
        super().__init__(args)

    def start_process(self):
        if self.args[0] == self.INITIALIZE_DATA_COMMAND:
            self.start_initializing_data()
        elif self.args[0] == self.UPDATE_INDICES_COMMAND:
            self.start_updating_indices()
        else:
            print('The command ' + self.args[0] + ' is not defined as a Demos rebase command.')
            print('Please see manual page running "demos train -h"')

    def start_initializing_data(self):
        print(self.args)
        print('Are you sure you want to initialize the root data of your database ?')
        print('The list of the web sites to crawl will be updated')
        input('[Ctrl+C : stop | Any other key : continue]')
        Configuration(self.args)
        initializer = LocalGovernmentInitializer()
        initializer.log_info('Starting initialization of french communes')
        initializer.store_communes_of_france()
        initializer.create_index_on_domain_name()

    def start_updating_indices(self):
        Configuration(self.args)
        index_manager = RedisIndexManager()
        index_manager.update_index(LocalGovernment, 'domain_name')
        index_manager.update_index(WebDocument, 'classified_as_official_report')
        index_manager.update_index(WebDocument, 'local_government')
        index_manager.update_index(WebDocument, 'subset_type')

    def get_manual_page(self):
        return AdminManualPage()


class AdminManualPage(ManualPage):
    def __init__(self):
        super().__init__()

    def get_title(self):
        return 'Welcome in Demos admin manual page !'

    def get_usage(self):
        return 'demos admin [command]'

    def get_description(self):
        return None

    def get_commands(self):
        return [
            Command(AdminLauncher.UPDATE_INDICES_COMMAND,
                    'Updates database indices.'),
            Command(AdminLauncher.INITIALIZE_DATA_COMMAND,
                    'Initialize into database the data necessary to start scraping, classifying, and training.' + os.linesep + \
                    'The data initialized are :' + os.linesep + \
                    '- the list of local government(french communes)' + os.linesep + \
                    '- the domain names of official web sites for each local government' + os.linesep + \
                    '/!\\ CAUTION : If your database is not empty, this will screw up your data !')
        ]
