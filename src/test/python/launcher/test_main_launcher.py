import unittest
import io
import sys

from src.main.python.launcher.main_launcher import MainLauncher


class TestMainLauncher(unittest.TestCase):
    def test_launch_should_print_manual_page_if_argument_list_is_empty(self):
        # given
        launcher = MainLauncher([])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_manual_page_if_first_argument_is_dash_h(self):
        # given
        launcher = MainLauncher(['-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_error_if_first_argument_is_not_known(self):
        # given
        launcher = MainLauncher(['washdishes'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('The command washdishes is not defined in Demos.'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_training_manual_page_with_argument_train_only(self):
        # given
        launcher = MainLauncher(['train'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos training manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_manual_page_with_arguments_train_and_dash_h(self):
        # given
        launcher = MainLauncher(['train', '-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos training manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_error_with_arguments_train_and_a_wrong_option(self):
        # given
        launcher = MainLauncher(['train', 'washdishes'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('The command washdishes is not defined as a Demos training command.'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_collecting_manual_page_with_arguments_train_collect_dash_h(self):
        # given
        launcher = MainLauncher(['train', 'collect', '-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos collecting manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_classifying_manual_page_with_arguments_train_classify_dash_h(self):
        # given
        launcher = MainLauncher(['train', 'classify', '-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos classifying manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_modeling_manual_page_with_arguments_train_model_dash_h(self):
        # given
        launcher = MainLauncher(['train', 'model', '-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos modeling manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_archiving_manual_page_with_arguments_archive_dash_h(self):
        # given
        launcher = MainLauncher(['archive', '-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos archiving manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_test_manual_page_with_arguments_test_dash_h(self):
        # given
        launcher = MainLauncher(['test', '-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos test manual page ! --'))
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
