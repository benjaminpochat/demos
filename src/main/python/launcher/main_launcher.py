import os
import sys

from src.main.python.launcher.launcher import Launcher, ManualPage, Command


class MainLauncher(Launcher):
    """
    A class that handle command line to launch Demos tooling set such as :
    * demos train collect : collects web documents from official local governments web sites
    * demos train classify : classify the web documents collected, with the user input
    * demos train model : train and produce a model from the manual classification inputs
    * demos archive : crawl the local governments web sites and archive the web documents that matches with the classification
    """

    TRAIN_COMMAND = 'train'
    TEST_COMMAND = 'test'
    ARCHIVE_COMMAND = 'archive'
    ADMIN_COMMAND = 'admin'

    def __init__(self, args: list):
        super().__init__(args)

    def start_process(self):
        if self.args.__len__() == 0:
            self.get_manual_page().display()
        elif self.args[0] == self.ADMIN_COMMAND:
            self.start_admin_launcher()
        elif self.args[0] == self.TRAIN_COMMAND:
            self.start_training_launcher()
        elif self.args[0] == self.ARCHIVE_COMMAND:
            self.start_archiving_launcher()
        elif self.args[0] == self.TEST_COMMAND:
            self.start_test_launcher()
        else:
            print('The command ' + self.args[0] + ' is not defined in Demos.')
            print('Please see manual page running "demos -h"')

    def get_manual_page(self):
        return MainManualPage()

    def start_admin_launcher(self):
        from src.main.python.launcher.admin_launcher import AdminLauncher
        rebasing_launcher = AdminLauncher(self.args[1:])
        rebasing_launcher.launch()

    def start_training_launcher(self):
        from src.main.python.launcher.training_launcher import TrainingLauncher
        training_launcher = TrainingLauncher(self.args[1:])
        training_launcher.launch()

    def start_archiving_launcher(self):
        from src.main.python.launcher.archiving_launcher import ArchivingLauncher
        archiving_launcher = ArchivingLauncher(self.args[1:])
        archiving_launcher.launch()

    def start_test_launcher(self):
        from src.main.python.launcher.test_launcher import TestLauncher
        test_launcher = TestLauncher(self.args[1:])
        test_launcher.launch()


class MainManualPage(ManualPage):
    def get_title(self):
        return 'Welcome in Demos manual page !'

    def get_usage(self):
        return 'demos [command] [options]'

    def get_description(self):
        self.database = 'Demos is an experimental tooling set for collecting and archiving official reports coming from local government (city councils, district councils, etc...)' + os.linesep + 'For more information, see https://github.com/benjaminpochat/demos' + os.linesep + os.linesep + 'Requirements :' + os.linesep + '  * configure the configuration file config.yml' + os.linesep + '  * start the Redis database'
        return self.database

    def get_commands(self):
        return [
            Command(MainLauncher.TRAIN_COMMAND,
                    'a set of tools to collect unclassified documents, train a classification model, and produce a classification model to use for real archiving process' + os.linesep + \
                    'See training help page to see the options in details :' + os.linesep + \
                    '"demos train -h"'),
            Command(MainLauncher.TEST_COMMAND,
                    'a set of tools to test automatic classification performed by the model trained' + os.linesep + \
                    'See test help page to see the options in details :' + os.linesep + \
                    '"demos test -h"'),
            Command(MainLauncher.ARCHIVE_COMMAND,
                    'a set of tools to archive documents classified as official reports' + os.linesep + \
                    'See archiving help page to see the options in details :' + os.linesep + \
                    '"demos archive -h"'),
            Command(MainLauncher.ADMIN_COMMAND,
                    'a set of tools to administrate the system and its data.'+ os.linesep + \
                    'See administration help page to see the options in details :'+ os.linesep + \
                    '"demos admin -h"')
        ]


if __name__ == '__main__':
    launcher = MainLauncher(sys.argv[1:])
    launcher.launch()
