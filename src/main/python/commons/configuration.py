import os

import yaml


class Configuration:

    def __init__(self):
        config_file_path = os.path.join(os.path.dirname(__file__),
                     '../../resources/config.yml')
        ymlfile = open(config_file_path, 'r')
        config_dict  = yaml.load(ymlfile)
        self.database_host = config_dict['database']['host']
        self.database_port = config_dict['database']['port']
        self.database_port = config_dict['machine_learning_model']['model_file']
        self.database_port = config_dict['machine_learning_model']['vocabulary_file']