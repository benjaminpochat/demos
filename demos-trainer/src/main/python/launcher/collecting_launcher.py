import os

from src.main.python.launcher.launcher import Launcher, ManualPage, Option


class CollectingLauncher(Launcher):

    SPECIFIC_DOMAIN_NAME_OPTION = '-d'
    NUMBER_OF_LOCAL_GOVERNMENTS_OPTION = '-n'

    def get_manual_page(self):
        return CollectingManualPage()

    def __init__(self, args: list):
        self.args = args

    def start_process(self):
        from src.main.python.process.local_government_selection.local_government_redis_selector import LocalGovernmentRedisSelector
        from src.main.python.process.training.training_data_producer.training_data_collector import TrainingDataCollector

        domains = []
        subset_size = 1
        if self.args.__contains__(self.SPECIFIC_DOMAIN_NAME_OPTION):
            d_option_index = self.args.index(self.SPECIFIC_DOMAIN_NAME_OPTION)
            domains.append(self.args[d_option_index + 1])
        elif self.args.__contains__(self.NUMBER_OF_LOCAL_GOVERNMENTS_OPTION):
            n_option_index = self.args.index(self.NUMBER_OF_LOCAL_GOVERNMENTS_OPTION)
            subset_size = int(self.args[n_option_index + 1])
        selector = LocalGovernmentRedisSelector(subset_size=subset_size, domains=domains)
        collector = TrainingDataCollector(selector=selector)
        print('Start collecting data...')
        print('[ Ctrl + C ] to quit')
        collector.collect()


class CollectingManualPage(ManualPage):
    def get_title(self):
        return 'Welcome in Demos collecting manual page !'

    def get_usage(self):
        return 'demos train collect [options]'

    def get_description(self):
        return 'Demos collecting module crawls the local government official web sites, and stores the web documents in Redis database.'

    def get_options(self):
        return [
            Option(CollectingLauncher.SPECIFIC_DOMAIN_NAME_OPTION,
                   'set a particular domain to crawl with the following syntax :' + os.linesep +
                   '\'demos archive -d <domaine_name>\'' + os.linesep +
                   'For example :' + os.linesep +
                   '\'demos achive -d chamonix.fr\' to crawl Chamonix city web site' + os.linesep +
                   'The domain name given must match a local government.' + os.linesep +
                   'By default, if this option is not used, the process chooses the local governement randomly'),
            Option(CollectingLauncher.NUMBER_OF_LOCAL_GOVERNMENTS_OPTION,
                   'set the number of local governments\' web sites to crawl with the following syntax :' + os.linesep +
                   '\'demos archive -n <number>\'' + os.linesep +
                   'For example :' + os.linesep +
                   '\'demos archive -n 10\' to crawl 10 local governments chosen randomly' + os.linesep +
                   'For endless crawling, use -1 value.' + os.linesep +
                   'By default, if this option is not used, only 1 local government is crawled at a time.' + os.linesep +
                   'This option is ignored if the parameter -d is used')
        ]
