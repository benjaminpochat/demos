from src.main.python.process.local_government_initialization.local_government_initializer import LocalGovernmentInitializer
from src.main.python.commons.configuration import Configuration


class RebasingLauncher:
    def __init__(self, options: list):
        self.options = options

    def launch(self):
        print(self.options)
        print('Are you sure you want to rebase the root data of your database ?')
        print('The list of the web sites to crawl will be updated')
        input('[Ctrl+C : stop | Any other key : continue]')
        Configuration(self.options)
        initializer = LocalGovernmentInitializer()
        initializer.log_info('Starting initialization of french communes')
        initializer.store_communes_of_france()
        initializer.create_index_on_domain_name()
