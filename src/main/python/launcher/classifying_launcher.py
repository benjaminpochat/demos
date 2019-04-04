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
        print('  -s get the statistics of the classification : number of documents classified, total of documents')
        print('')
        print('  -C clear the classification on all documents before starting')
        print('     /!\\ CAUTION : All the manual classification is lost after it has been cleared !')
        print('')
        print('  -D distribute the dataset classified manually into the 3 subsets of data :')
        print('     * the training dataset, use to train the model while building the model')
        print('     * the validation dataset, use to validate the model while building the model')
        print('     * the test dataset, use to evaluate the model by drawing the ROC curve')
        print('     The proportion of the 3 slots is given by the 3 following properties in config.yml file : traning_dataset_percent, validation_dataset_percent, test_dataset_percent.')
        print('     /!\\ CAUTION : The 3 subsets are shuffled and previous distribution is lost and the 3 after this action.')
        print('')

    def start_classifying(self):
        from src.main.python.process.training.training_data_producer.manual_classifier import ManualWebDocumentClassifier

        classifier = ManualWebDocumentClassifier()
        if self.options.__contains__('-C'):
            classifier.clear_classification()
        if self.options.__contains__('-D'):
            classifier.distribute_classification()
            exit(0)
        if self.options.__contains__('-s'):
            classifier.show_classification_statistics()
            exit(0)
        while True:
            input('Start next classification ? [Ctrl+C : quit | Enter : continue]')
            classifier.classify()
