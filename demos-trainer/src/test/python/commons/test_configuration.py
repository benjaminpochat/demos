import unittest
from src.main.python.commons.configuration import Configuration
from src.main.python.commons.configuration import ConfigurationException


class TestConfiguration(unittest.TestCase):
    def tearDown(self):
        configuration_class = Configuration.__class__
        configuration_class._instances.clear()

    def test_init_should_load_default_configuration_values(self):
        # given

        # when
        configuration = Configuration()

        # then
        self.assertEqual(configuration.get_database_host(), 'localhost')
        self.assertEqual(configuration.get_database_port(), '6379')
        self.assertEqual(configuration.get_keras_model_file(), 'mlp_model.h5')
        self.assertEqual(configuration.get_tensorflow_model_file(), 'mlp_model.pb')
        self.assertEqual(configuration.get_feature_selector_file(), 'feature_selector.pkl')
        self.assertEqual(configuration.get_vectorizer_file(), 'vectorizer.pkl')
        self.assertEqual(configuration.get_tensortflow_serving_host(), 'localhost')
        self.assertEqual(configuration.get_tensortflow_serving_port(), '8501')

    def test_init_with_arguments_should_load_primarily_arguments_configuration_values(self):
        # given
        args = ['--database_host', 'dbserver', '--database_port', '666']

        # when
        configuration = Configuration(args)

        # then
        self.assertEqual(configuration.database_host, 'dbserver')
        self.assertEqual(configuration.database_port, '666')
        self.assertEqual(configuration.keras_model_file, 'mlp_model.h5')
        self.assertEqual(configuration.tensorflow_model_file, 'mlp_model.pb')
        self.assertEqual(configuration.feature_selector_file, 'feature_selector.pkl')
        self.assertEqual(configuration.vectorizer_file, 'vectorizer.pkl')

    def test_init_with_unknown_arguments_should_raise_an_error(self):
        # given
        args = ['--xxx', 'yyy']
        exception = None

        # when
        try:
            Configuration(args)
        except ConfigurationException as e:
            exception = e

        # then
        self.assertIsNotNone(exception)
        self.assertEqual(exception.message, 'Argument \'xxx\' is not a configuration item !')

    def test_init_with_missing_value_should_raise_an_error(self):
        # given
        args = ['--database_port', '666', '--database_host']

        # when
        try:
            Configuration(args)
        except ConfigurationException as e:
            exception = e

        # then
        self.assertIsNotNone(exception)
        self.assertEqual(exception.message, 'Argument \'database_host\' has no value !')

if __name__ == '__main__':
    unittest.main()
