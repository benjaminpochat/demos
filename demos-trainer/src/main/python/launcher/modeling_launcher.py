import os

from src.main.python.launcher.launcher import Launcher, ManualPage


class ModelingLauncher(Launcher):
    """
    A launcher to build and save the prediction model from the dataset.
    """

    def get_manual_page(self):
        return ModelingManualPage()

    def __init__(self, args: list):
        self.args = args

    def start_process(self):
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
        texts_and_labels = text_and_label_loader.load_texts_and_labels()
        data = (texts_and_labels[0], texts_and_labels[1]), (texts_and_labels[2], texts_and_labels[3])
        model_builder.build_model(data)


class ModelingManualPage(ManualPage):
    def get_title(self):
        return 'Welcome in Demos modeling manual page !'

    def get_usage(self):
        return 'demos train model'

    def get_description(self):
        return 'Demos modeling build and trains an automatic classification model.' + os.linesep +\
               'It produces 3 files : ' + os.linesep +\
               '- a model file' + os.linesep +\
               '- a vectorizer file' + os.linesep +\
               '- and a feature selector file' + os.linesep +\
               'These files can be used with \'demos test\' and \'demos archive\' commands to classify automatically documents.'
