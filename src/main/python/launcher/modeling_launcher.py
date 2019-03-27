class ModelingLauncher:
    def __init__(self, options: list):
        self.options = options

    def launch(self):
        if self.options.__len__() > 0 and  self.options[0] == '-h':
            self.print_manual_page()
        else:
            self.start_modeling()

    def print_manual_page(self):
        print('')
        print('-- Welcome in Demos modeling manual page ! --')
        print('')
        print('Demos modeling build and trains an automatic classification model.')
        print('It produces 2 files : a model file and a vocabulary file that can be used to collect automatically and widely local government official reports')
        print('')
        print('Usage : demos train model')
        print('')

    def start_modeling(self):
        import logging
        from logging import StreamHandler

        from src.main.python.process.training.classification_model.mlp_model_builder import MlpModelBuilder
        from src.main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader

        log_handler = StreamHandler()
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        model_builder = MlpModelBuilder()
        model_builder._logger.addHandler(log_handler)

        text_and_label_loader = TextAndLabelLoader()
        texts_and_labels = text_and_label_loader.load_texts_and_labels(training_size=10, validation_size=10)
        data = (texts_and_labels[0], texts_and_labels[1]), (texts_and_labels[2], texts_and_labels[3])
        model_builder.build_model(data)
