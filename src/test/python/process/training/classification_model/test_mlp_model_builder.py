import unittest
from unittest.mock import Mock

from src.main.python.process.training.classification_model.mlp_model_builder import MlpModelBuilder
from src.main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader
import src.test.python.process.training.text_dataset_producer.test_text_dataset_loader as test_text_dataset_loader


class TestMlpModelBuilder(unittest.TestCase):
    def test_build_model_should_run_without_error_with_few_small_texts(self):

        # given
        model_builder = MlpModelBuilder()
        model_builder._train_model = Mock(side_effect=print('MlpModelBuilder._train_model mocked'))
        text_and_label_loader = TextAndLabelLoader()
        text_and_label_loader._get_random_web_documents_generator = test_text_dataset_loader.mock_get_random_web_documents_generator()
        texts_and_labels = text_and_label_loader.load_texts_and_labels(training_size=2, validation_size=2)

        data = (texts_and_labels[0], texts_and_labels[1]), (texts_and_labels[2], texts_and_labels[3])
        print(texts_and_labels[1])
        print(texts_and_labels[3])

        # when
        model_builder.build_model(data)

        # then

if __name__ == '__main__':
    unittest.main()