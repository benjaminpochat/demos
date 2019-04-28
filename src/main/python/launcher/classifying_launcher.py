import os

from src.main.python.launcher.launcher import Launcher, ManualPage, Option


class ClassifyingLauncher(Launcher):

    SHOW_STATISTICS_OPTION = '-s'
    DISTRIBUTE_CLASSIFICATION_OPTION = '-D'
    CLEAR_CLASSIFICATION_OPTION = '-C'

    def __init__(self, args: list):
        super().__init__(args)

    def get_manual_page(self):
        return ClassifyingManualPage()

    def start_process(self):
        from src.main.python.process.training.training_data_producer.manual_classifier import \
            ManualWebDocumentClassifier

        classifier = ManualWebDocumentClassifier()
        if self.args.__contains__(self.CLEAR_CLASSIFICATION_OPTION):
            classifier.clear_classification()
        if self.args.__contains__(self.DISTRIBUTE_CLASSIFICATION_OPTION):
            classifier.distribute_classification()
            exit(0)
        if self.args.__contains__(self.SHOW_STATISTICS_OPTION):
            classifier.show_classification_statistics()
            exit(0)
        while True:
            input('Start next classification ? [Ctrl+C : quit | Enter : continue]')
            classifier.classify()


class ClassifyingManualPage(ManualPage):

    def __init__(self):
        super().__init__()

    def get_title(self):
        return 'Welcome in Demos classifying manual page !'

    def get_usage(self):
        return 'demos train classify [options]'

    def get_description(self):
        return  'Demos classification module is a tool to classify manually the documents found on the local governments\' web sites.' + os.linesep + \
                'These classifications data will be used afterward to build an automatic classification model'

    def get_options(self):
        return [
                Option(ClassifyingLauncher.SHOW_STATISTICS_OPTION,
                    'get the statistics of the classification : number of documents classified, total of documents'),
                Option(ClassifyingLauncher.CLEAR_CLASSIFICATION_OPTION,
                    'clear the classification on all documents before starting' + os.linesep +
                    '/!\\ CAUTION : All the manual classification is lost after it has been cleared !'),
                Option(ClassifyingLauncher.DISTRIBUTE_CLASSIFICATION_OPTION,
                    'distribute the dataset classified manually into the 3 subsets of data :' + os.linesep +
                    '* the training dataset, use to train the model while building the model' + os.linesep +
                    '* the validation dataset, use to validate the model while building the model' + os.linesep +
                    '* the test dataset, use to evaluate the model by drawing the ROC curve' + os.linesep +
                    'The proportion of the 3 slots is given by the 3 following properties in config.yml file : traning_dataset_percent, validation_dataset_percent, test_dataset_percent.' + os.linesep +
                    '/!\\ CAUTION : The 3 subsets are shuffled and previous distribution is lost and the 3 after this action.')
            ]
