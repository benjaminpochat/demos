import unittest
import os

from unittest.mock import Mock
from main.python.classification_model.mlp_model_builder import MlpModelBuilder
from main.python.data_preparation.text_dataset_producer.text_dataset_loader import TextAndLabelLoader


class TestMlpModelBuilder(unittest.TestCase):
    def test_build_model_with_few_small_texts(self):

        # given
        model_builder = MlpModelBuilder()
        model_builder._train_model = Mock(side_effect=print('MlpModelBuilder._train_model mocked'))
        text_file_root_folder = os.path.join(os.path.dirname(__file__), '../../resources/data_preparation/text_dataset_producer')
        training_text_files_folder = 'training'
        validation_text_files_folder = 'validation'
        text_and_label_loader = TextAndLabelLoader();
        texts_and_labels = text_and_label_loader.load_texts_and_labels(
            text_file_root_folder,
            training_text_files_folder,
            validation_text_files_folder)

        data = (texts_and_labels[0], texts_and_labels[1]), (texts_and_labels[2], texts_and_labels[3])
        print(texts_and_labels[1])
        print(texts_and_labels[3])

        # when
        model_builder.build_model(data)

        # then

if __name__ == '__main__':
    unittest.main()