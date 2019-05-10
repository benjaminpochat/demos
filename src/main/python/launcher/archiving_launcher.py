import os
import sys

from src.main.python.launcher.launcher import Launcher, ManualPage, Option


class ArchivingLauncher(Launcher):
    """
    A launcher to start crawl local governments web sites and archive documents detected as official reports.
    """

    SPECIFIC_DOMAIN_NAME_OPTION = '-d'
    NUMBER_OF_LOCAL_GOVERNMENTS_OPTION = '-n'
    TENSORFLOW_SERVING_MODE = '-tfs'

    def __init__(self, args: list):
        self.args = args

    def start_process(self):
        from src.main.python.process.archiving.archiver import DelibArchiver
        from src.main.python.process.local_government_selection.local_government_selector import LocalGovernmentSelector

        subset_size = 1
        domains = []
        if self.args.__contains__(self.SPECIFIC_DOMAIN_NAME_OPTION):
            n_option_index = sys.argv.index(self.SPECIFIC_DOMAIN_NAME_OPTION)
            domains.append(sys.argv[n_option_index + 1])
        elif self.args.__contains__(self.NUMBER_OF_LOCAL_GOVERNMENTS_OPTION):
            n_option_index = self.args.index(self.NUMBER_OF_LOCAL_GOVERNMENTS_OPTION)
            subset_size = int(self.args[n_option_index + 1])
        print('Start archiving data...')
        print('[ Ctrl + C ] to quit')
        selector = LocalGovernmentSelector(subset_size=subset_size, domains=domains)
        archiver = DelibArchiver(selector=selector)
        archiver.archive()

    def get_manual_page(self):
        return ArchivingManualPage()


class ArchivingManualPage(ManualPage):

    def get_title(self):
        return 'Welcome in Demos archiving manual page !'

    def get_usage(self):
        return 'demos archive [options]'

    def get_description(self):
        return 'Demos archiving module is a tool that stores in tha database all the official council reports found in the local governments\' web sites'  + os.linesep +\
               'It recognizes local governments official reports thanks to the classification model built with the Demos training module (see manual page "demos train -h"'

    def get_options(self):
        return [
            Option(ArchivingLauncher.SPECIFIC_DOMAIN_NAME_OPTION,
                   'sets a particular domain to crawl with the following syntax :' + os.linesep +
                   '\'demos archive -d <domaine_name>\'' + os.linesep +
                   'For example :' + os.linesep +
                   '\'demos achive -d chamonix.fr\' to crawl Chamonix city web site' + os.linesep +
                   'The domain name given must match a local government.' + os.linesep +
                   'By default, if this option is not used, the process chooses the local governement randomly'),
            Option(ArchivingLauncher.NUMBER_OF_LOCAL_GOVERNMENTS_OPTION,
                   'sets the number of local governments\' web sites to crawl with the following syntax :' + os.linesep +
                   '\'demos archive -n <number>\'' + os.linesep +
                   'For example :' + os.linesep +
                   '\'demos archive -n 10\' to crawl 10 local governments chosen randomly' + os.linesep +
                   'For endless crawling, use -1 value.' + os.linesep +
                   'By default, if this option is not used, only 1 local government is crawled at a time.' + os.linesep +
                   'This option is ignored if the parameter -d is used'),
            Option(ArchivingLauncher.TENSORFLOW_SERVING_MODE,
                   'activates the "tensorflow-serving mode"' + os.linesep +
                   'This mode must be used for production deployment, using a lightweight docker container for the classification process' + os.linesep +
                   'With this option, the 2 following properties are used : "tensorflow_serving_host" and "tensorflow_serving_port"')
        ]
