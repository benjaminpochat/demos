from src.main.python.launcher.classifying_launcher import ClassifyingLauncher
from src.main.python.launcher.modeling_launcher import ModelingLauncher
from src.main.python.launcher.collecting_launcher import CollectingLauncher


class TrainingLauncher:

    def __init__(self, options: list):
        self.options = options

    def launch(self):
        if self.options.__len__() == 0 or self.options[0] == '-h':
            self.print_manual_page()
        elif self.options[0] == 'collect':
            self.start_collecting_launcher()
        elif self.options[0] == 'classify':
            self.start_classifying_launcher()
        elif self.options[0] == 'model':
            self.start_modeling_launcher()
        else:
            print('The command ' + self.options[0] + ' is not defined as a Demos training command.')
            print('Please see manual page running "demos train -h"')

    @staticmethod
    def print_manual_page():
        print('')
        print('-- Welcome in Demos training manual page ! --')
        print('')
        print('Demos training module provide tools to build and train an classification model that recognizes what is an official report comming from local government')
        print('These tools are not supposed to run in production environment.')
        print('Their goal is to build a classification model that will be used in a archiving module')
        print('')
        print('Usage : demos train [command] [options]')
        print('')
        print('The commands available are :')
        print('')
        print('  "collect" : crawl the web to collect unclassified documents from the local government official web sites')
        print('              The collected web documents will be used do be manually classified, and then to build an automatic classification model')
        print('              See collect manual page to see the options in detail :')
        print('              "demos train collect -h"')
        print('')
        print('  "classify" : starts the manual classification process, to get classification data from a human user, for the documents collected with the "collect" command.')
        print('              See classify manual page to see the options in detail :')
        print('              "demos train classify -h"')
        print('')
        print('  "model" : build and train a classification model from the classification data gathered with the "classify command.')
        print('            Produces a Keras model file containing the trained model.')
        print('            See model manual page to see the options in detail :')
        print('            "demos train model -h"')
        print('')

    def start_collecting_launcher(self):
        launcher = CollectingLauncher(self.options[1:])
        launcher.launch()

    def start_classifying_launcher(self):
        launcher = ClassifyingLauncher(self.options[1:])
        launcher.launch()

    def start_modeling_launcher(self):
        launcher = ModelingLauncher(self.options[1:])
        launcher.launch()
