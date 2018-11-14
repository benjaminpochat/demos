import unittest
from classification_model.mlp_model_builder import MlpModelBuilder
from data_preparation.text_dataset_producer import text_dataset_loader


class TestMlpModelBuilder(unittest.TestCase):
    def test_build_model_with_few_small_texts(self):
        # given
        model_builder = MlpModelBuilder()
        text_file_root_folder = '../../../resources/data_preparation/text_dataset_producer'
        training_text_files_folder = 'training'
        validation_text_files_folder = 'validation'
        texts_and_labels = text_dataset_loader.load_texts_and_labels(
            text_file_root_folder,
            training_text_files_folder,
            validation_text_files_folder)

        data = (texts_and_labels[0], texts_and_labels[1]), (texts_and_labels[2], texts_and_labels[3])
        print(texts_and_labels[1])
        print(texts_and_labels[3])

        # when
        model_builder.build_model(data)

        # then