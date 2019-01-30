from src.main.python.process.archiving.archiver import DelibArchiver
from src.main.python.process.local_government_selection.local_government_selector import LocalGovernmentSelector
from src.main.python.commons.configuration import Configuration


class ArchivingLauncher:
    def __init__(self, options: list):
        self.options = options

    def launch(self):
        if self.options.__len__() > 0 and self.options[0] == '-h':
            self.print_manual_page()
        else:
            self.start_archiving()

    @staticmethod
    def print_manual_page():
        print('')
        print('-- Welcome in Demos archiving manual page ! --')
        print('')
        print('Demos archiving module is a tool that stores in tha database all the official council reports found in the local governments\' web sites')
        print('It recognizes local governments official reports thanks to the classification model built with the Demos training module (see manual page "demos train -h")')
        print('')
        print('Usage : demos train archive [options]')
        print('')
        print('The options available are :')
        print('')
        print('  -d <domain name> : a particular domain to crawl. Must match a local government.')
        print('     By default, the process chooses the local governement randomly')
        print('')
        print('  -n <number> : the number of local governments\' web sites to crawl (default is 1)')
        print('     Ignored if the parameter -d is used')
        print('     By default, the process never ends (value -1).')
        print('')

    def start_archiving(self):
        subset_size = 1
        domains = []
        if self.options.__contains__('-d'):
            n_option_index = sys.argv.index('-d')
            domains.append(sys.argv[n_option_index + 1])
        elif self.options.__contains__('-n'):
            n_option_index = self.options.index('-n')
            subset_size = int(self.options[n_option_index + 1])
        print('Start archiving data...')
        print('[ Ctrl + C ] to quit')
        Configuration(self.options)
        selector = LocalGovernmentSelector(subset_size=subset_size, domains=domains)
        archiver = DelibArchiver(selector=selector)
        archiver.archive()
