class CollectingLauncher:

    def __init__(self, options: list):
        self.options = options

    def launch(self):
        if self.options.__len__() > 0 and self.options[0] == '-h':
            self.print_manual_page()
        else:
            self.start_collecting()

    def start_collecting(self):
        from src.main.python.commons.configuration import Configuration
        from src.main.python.process.local_government_selection.local_government_selector import LocalGovernmentSelector
        from src.main.python.process.training.training_data_producer.training_data_collector import TrainingDataCollector

        domains = []
        subset_size = 1
        if self.options.__contains__('-d'):
            n_option_index = self.options.index('-d')
            domains.append(self.options[n_option_index + 1])
        elif self.options.__contains__('-n'):
            n_option_index = self.options.index('-n')
            subset_size = int(self.options[n_option_index + 1])
        Configuration(self.options)
        selector = LocalGovernmentSelector(subset_size=subset_size, domains=domains)
        collector = TrainingDataCollector(selector=selector)
        print('Start collecting data...')
        print('[ Ctrl + C ] to quit')
        collector.collect()

    @staticmethod
    def print_manual_page():
        print('')
        print('-- Welcome in Demos collecting manual page ! --')
        print('')
        print('Demos collecting module crawls the local government official web sites, and stores the web documents in Redis database.')
        print('')
        print('Usage : demos train collect [options]')
        print('')
        print('The options available are :')
        print('')
        print('  -n <number> : the number of local governments\' web sites to crawl (default is 1)')
        print('')
        print('  -d <domain name> : a particular domain to crawl. Must match a local government.')
        print('')
