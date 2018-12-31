import sys
from src.main.python.commons.configuration import Configuration


def log_configuration():
    print('Starting with the following configuration :')
    for attribute_key in configuration.__dict__.keys():
        attribute_value = configuration.__dict__[attribute_key]
        print(attribute_key + '=' + attribute_value)


if __name__ == '__main__':
    print('Welcome in the delib_archer process.')
    configuration = Configuration(sys.argv[1:])
    log_configuration()
