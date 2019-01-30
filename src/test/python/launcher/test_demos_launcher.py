import unittest
import io
import sys

from src.main.python.launcher.demos_launcher import GlobalLauncher


class TestGlobalLauncher(unittest.TestCase):
    def test_launch_should_print_manual_page_if_argument_list_is_empty(self):
        # given
        launcher = GlobalLauncher([])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_manual_page_if_first_argument_is_dash_h(self):
        # given
        launcher = GlobalLauncher(['-h'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('-- Welcome in Demos manual page ! --'))
        sys.stdout = sys.__stdout__

    def test_launch_should_print_error_if_first_argument_is_not_known(self):
        # given
        launcher = GlobalLauncher(['washdishes'])
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # when
        launcher.launch()

        # then
        self.assertTrue(captured_output.getvalue().strip().startswith('The command washdishes is not defined in Demos.'))
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
