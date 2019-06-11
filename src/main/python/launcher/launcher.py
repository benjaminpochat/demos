import os
from abc import abstractclassmethod

from src.main.python.commons.configuration import Configuration

class Launcher:
    """
    An abstract class to standardize all launchers
    """

    def __init__(self, args: list):
        self.args = args

    @abstractclassmethod
    def start_process(self):
        pass

    @abstractclassmethod
    def get_manual_page(self):
        pass

    def launch(self):
        if self.args.__len__() == 0 or self.args[0] == '-h':
            self.get_manual_page().display()
        else:
            Configuration(self.args).overload_values_with_command_line_arguments(self.args)
            self.start_process()


class ManualPage:
    """
    An abstract class to standardize the manual pages of all launchers.
    """

    @abstractclassmethod
    def get_title(self):
        pass

    @abstractclassmethod
    def get_usage(self):
        pass

    @abstractclassmethod
    def get_description(self):
        pass

    def get_options(self):
        return []

    def get_commands(self):
        return []

    def display(self):
        self.display_title()
        self.display_description()
        self.display_usage()
        self.display_commands()
        self.display_options()

    def display_title(self):
        print('')
        print('-- ' + self.get_title() + ' --')
        print('')

    def display_usage(self):
        print('Usage : ' + self.get_usage())
        print('')

    def display_description(self):
        if self.get_description() is not None:
            for description_line in self.get_description_lines():
                print(description_line)
            print('')

    def display_commands(self):
        if self.get_commands():
            print('The commands available are :')
            for command in self.get_commands():
                print('')
                print('  ' + command.symbol + ' :')
                for description_line in command.get_description_lines():
                    print('    ' + description_line)
            print('')

    def display_options(self):
        if self.get_options():
            print('The options available are :')
            for option in self.get_options():
                print('')
                print('  ' + option.symbol + ' :')
                for description_line in option.get_description_lines():
                    print('    ' + description_line)
            print('')

    def get_description_lines(self):
        return self.get_description().split(os.linesep)



class Command:
    """
    An command available in a launcher.
    Only one command can be executed at a time.
    """
    def __init__(self, symbol: str, description: str):
        self.symbol = symbol
        self.description = description

    def get_description_lines(self):
        return self.description.split(os.linesep)


class Option:
    """
    An option available in a launcher.
    Several options can be used at a time.
    """
    def __init__(self, symbol: str, description: str):
        self.symbol = symbol
        self.description = description

    def get_description_lines(self):
        return self.description.split(os.linesep)
