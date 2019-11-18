import os
import yaml
import logging.config


from src.main.python.commons.singleton import Singleton


class Configuration(metaclass=Singleton):
    """
    A class to handle configuration.
    Every attribute of the configuration is a string.
    See config.yml to know the entire list of configuration items.
    """

    def __init__(self, command_line_arguments: list = []):
        self.initialize_attributes_from_config_file()
        self.overload_values_with_command_line_arguments(command_line_arguments)
        self.convert_attributes_as_strings()
        self.log_configuration()

    def initialize_attributes_from_config_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), '../../resources/config.yml')
        yaml_file = open(config_file_path, 'r')
        config_dict = yaml.load(yaml_file)
        self.__dict__ = config_dict

    def overload_values_with_command_line_arguments(self, command_line_arguments):
        i = 0
        while i < command_line_arguments.__len__():
            if command_line_arguments[i].startswith('--'):
                argument_key = command_line_arguments[i][2:]
                if not self.__dict__.keys().__contains__(argument_key):
                    raise ConfigurationException('Argument \'' + argument_key + '\' is not a configuration item !')
                if i + 2 > command_line_arguments.__len__():
                    raise ConfigurationException('Argument \'' + argument_key + '\' has no value !')
                argument_value = command_line_arguments[i + 1]
                self.__dict__[argument_key] = argument_value
                command_line_arguments.pop(i)
                command_line_arguments.pop(i)
            else:
                i += 1

    def convert_attributes_as_strings(self):
        for key in self.__dict__.keys():
            self.__dict__[key] = str(self.__dict__[key])

    def log_configuration(self):
        self.configure_logging()
        logger = logging.getLogger('demos')
        logger.info('The configuration loaded is :')
        for attribute_key in self.__dict__.keys():
            attribute_value = self.__dict__[attribute_key]
            logger.info(attribute_key + '=' + attribute_value)

    def configure_logging(self):
        logging_file_path = os.path.join(
            os.path.dirname(__file__),
            '../../resources',
            self.get_logging_config_file())
        logging.config.fileConfig(logging_file_path)

    def get_database_host(self):
        return self.database_host

    def get_database_port(self):
        return self.database_port

    def get_keras_model_file(self):
        return self.keras_model_file

    def get_tensorflow_model_file(self):
        return self.tensorflow_model_file

    def get_vectorizer_file(self):
        return self.vectorizer_file

    def get_feature_selector_file(self):
        return self.feature_selector_file

    def get_logging_config_file(self):
        return self.logging_config_file

    def get_traning_dataset_percent(self):
        return int(self.traning_dataset_percent)

    def get_validation_dataset_percent(self):
        return int(self.validation_dataset_percent)

    def get_test_dataset_percent(self):
        return int(self.test_dataset_percent)

    def get_tensortflow_serving_host(self):
        return self.tensortflow_serving_host

    def get_tensortflow_serving_port(self):
        return self.tensortflow_serving_port

    def get_demos_core_host(self):
        return self.demos_core_host

    def get_demos_core_port(self):
        return self.demos_core_port

    def get_tensortflow_serving_port(self):
        return self.tensortflow_serving_port

    def get_demos_home(self):
        return os.environ.get('DEMOS_HOME')

    def _get_resource_file_path(self, file_name:str):
        return os.path.join(self.get_demos_home(), 'src', 'main', 'resources', file_name)

    def get_keras_model_file_path(self):
        return self._get_resource_file_path(self.get_keras_model_file())

    def get_tensorflow_model_file_path(self):
        return self._get_resource_file_path(self.get_tensorflow_model_file())

    def get_vectorizer_file_path(self):
        return self._get_resource_file_path(self.get_vectorizer_file())

    def get_feature_selector_file_path(self):
        return self._get_resource_file_path(self.get_feature_selector_file())


class ConfigurationException(Exception):

    def __init__(self, message: str):
        self.message = message
