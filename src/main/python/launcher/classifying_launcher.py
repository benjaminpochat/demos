from src.main.python.process.training.training_data_producer.manual_classifier import ManualWebDocumentClassifier


class ClassifyingLauncher:
    def __init__(self, options: list):
        self.options = options

    def launch(self):
        if self.options.__len__() > 0 and self.options[0] == '-h':
            self.print_manual_page()
        else:
            self.start_classifying()

    def print_manual_page(self):
        print('')
        print('-- Welcome in Demos classifying manual page ! --')
        print('')
        print('Demos classification module is a tool to classify manually the documents found on the local governments\' web sites.')
        print('These classifications data will be used afterward to build an automatic classification model')
        print('')
        print('Usage : demos train classify [options]')
        print('')
        print('The options available are :')
        print('')
        print('  -C clear the classification on all documents before starting')
        print('')
        print('  -s get the status of the classification : number of documents classified, total of documents')
        print('')

    def start_classifying(self):
        classifier = ManualWebDocumentClassifier()
        if self.options.__contains__('-C'):
            classifier.clear_classification()
        if self.options.__contains__('-s'):
            classifier.show_classification_status()
        while True:
            input('Start next classification ? [Ctrl+C : quit | Enter : continue]')
            classifier.classify()
