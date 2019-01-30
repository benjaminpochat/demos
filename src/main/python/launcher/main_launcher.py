import sys

from src.main.python.launcher.archiving_launcher import ArchivingLauncher
from src.main.python.launcher.training_launcher import TrainingLauncher


class MainLauncher:
    """
    A class that handle command line to launch Demos tooling set such as :
    * demos train collect : collects web documents from official local governments web sites
    * demos train classify : classify the web documents collected, with the user input
    * demos train model : train and produce a model from the manual classification inputs
    * demos archive : crawl the local governments web sites and archive the web documents that matches with the classification
    """
    def __init__(self, command_line_arguments: list):
        self.command_line_arguments = command_line_arguments

    def launch(self):
        if self.command_line_arguments.__len__() == 0 or self.command_line_arguments[0] == '-h':
            self.print_root_manual_page()
        elif self.command_line_arguments[0] == 'train':
            self.start_training_launcher()
        elif self.command_line_arguments[0] == 'archive':
            self.start_archiving_launcher()
        else:
            print('The command ' + self.command_line_arguments[0] + ' is not defined in Demos.')
            print('Please see manual page running "demos -h"')

    @staticmethod
    def print_root_manual_page():
        print('')
        print('-- Welcome in Demos manual page ! --')
        print('')
        print('Demos is an experimental tooling set for collecting and archiving official reports coming from local government (city councils, district councils, etc...)')
        print('For more information, see https://github.com/benjaminpochat/delib-archiver')
        print('')
        print('Requirements : ')
        print('  * configure the configuration file config.yml')
        print('  * start the Redis database')
        print('')
        print('Usage : demos [command] [options]')
        print('')
        print('The commands available are :')
        print('')
        print('  "train" : a set of tools to collect unclassified documents, train a classification model, and produce a classification model to use for real archiving process')
        print('            See training help page to see the options in details :')
        print('            "demos train -h"')
        print('')
        print('  "archive" : a set of tools to archive documents classified as official reports')
        print('              See archiving help page to see the options in details :')
        print('              "demos archive -h"')
        print('')

    def start_training_launcher(self):
        training_launcher = TrainingLauncher(self.command_line_arguments[1:])
        training_launcher.launch()

    def start_archiving_launcher(self):
        archiving_launcher = ArchivingLauncher(self.command_line_arguments[1:])
        archiving_launcher.launch()


if __name__ == '__main__':
    launcher = MainLauncher(sys.argv[1:])
    launcher.launch()
