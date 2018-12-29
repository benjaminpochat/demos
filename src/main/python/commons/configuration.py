import os

import yaml


class Configuration:
    """
    A class to handle configuration
    Every attribute of the configuration is a string
    """

    def __init__(self, command_line_arguments: list = []):
        self.initialize_attributes_from_config_file()
        self.overload_values_with_command_line_arguments(command_line_arguments)
        self.convert_attributes_as_strings()

    def initialize_attributes_from_config_file(self):
        config_file_path = os.path.join(os.path.dirname(__file__), '../../resources/config.yml')
        yaml_file = open(config_file_path, 'r')
        config_dict = yaml.load(yaml_file)
        self.__dict__ = config_dict

    def overload_values_with_command_line_arguments(self, command_line_arguments):
        i = 0
        while i < command_line_arguments.__len__():
            argument_key = command_line_arguments[i][2:]
            if not self.__dict__.keys().__contains__(argument_key):
                raise ConfigurationException('Argument \'' + argument_key + '\' is not a configuration item !')
            if i + 2 > command_line_arguments.__len__():
                raise ConfigurationException('Argument \'' + argument_key + '\' has no value !')
            argument_value = command_line_arguments[i + 1]
            self.__dict__[argument_key] = argument_value
            i += 2

    def convert_attributes_as_strings(self):
        for key in self.__dict__.keys():
            self.__dict__[key] = str(self.__dict__[key])


class ConfigurationException(Exception):

    def __init__(self, message: str):
        self.message = message
