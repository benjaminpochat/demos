import os

from src.main.python.launcher.launcher import Launcher, ManualPage, Command


class TrainingLauncher(Launcher):
    """
    A launcher to access features to prepare dataset and train a prediction model;
    """

    COLLECT_COMMAND = 'collect'
    CLASSIFY_COMMAND = 'classify'
    MODEL_COMMAND = 'model'

    def __init__(self, args: list):
        self.args = args

    def start_process(self):
        if self.args[0] == self.COLLECT_COMMAND:
            self.start_collecting_launcher()
        elif self.args[0] == self.CLASSIFY_COMMAND:
            self.start_classifying_launcher()
        elif self.args[0] == self.MODEL_COMMAND:
            self.start_modeling_launcher()
        else:
            print('The command ' + self.args[0] + ' is not defined as a Demos training command.')
            print('Please see manual page running "demos train -h"')

    def get_manual_page(self):
        return TrainingManualPage()

    def start_collecting_launcher(self):
        from src.main.python.launcher.collecting_launcher import CollectingLauncher
        launcher = CollectingLauncher(self.args[1:])
        launcher.launch()

    def start_classifying_launcher(self):
        from src.main.python.launcher.classifying_launcher import ClassifyingLauncher
        launcher = ClassifyingLauncher(self.args[1:])
        launcher.launch()

    def start_modeling_launcher(self):
        from src.main.python.launcher.modeling_launcher import ModelingLauncher
        launcher = ModelingLauncher(self.args[1:])
        launcher.launch()


class TrainingManualPage(ManualPage):
    def get_title(self):
        return 'Welcome in Demos training manual page !'

    def get_usage(self):
        return 'demos train [command] [options]'

    def get_description(self):
        return 'Demos training module provide tools to build and train an classification model that recognizes what is an official report comming from local government' + os.linesep +\
               'These tools are not supposed to run in production environment.' + os.linesep +\
               'Their goal is to build a classification model that will be used in a archiving module'

    def get_commands(self):
        return [
            Command(TrainingLauncher.COLLECT_COMMAND,
                    'Crawls the web to collect unclassified documents from the local government official web sites' + os.linesep+
                    'The collected web documents will be used do be manually classified, and then to build an automatic classification model'+ os.linesep+
                    'See collect manual page to see the options in detail :'+os.linesep+
                    '\'demos train ' + TrainingLauncher.COLLECT_COMMAND + ' -h\''),
            Command(TrainingLauncher.CLASSIFY_COMMAND,
                    'Starts the manual classification process, to get classification data from a human user, for the documents collected with the "collect" command.' + os.linesep +
                    'See classify manual page to see the options in detail :' + os.linesep +
                    '\'demos train ' + TrainingLauncher.CLASSIFY_COMMAND + ' -h\''),
            Command(TrainingLauncher.MODEL_COMMAND,
                    'Builds and train a classification model from the classification data gathered with the "classify command.' + os.linesep +
                    'Produces a Keras model file containing the trained model.' + os.linesep +
                    'See model manual page to see the options in detail :' + os.linesep +
                    '\'demos train ' + TrainingLauncher.MODEL_COMMAND + ' -h\''),
        ]