import unittest
from src.main.python.commons.configuration import Configuration


class TestConfiguration(unittest.TestCase):

    def test_init_should_load_default_configuration_values(self):
        # given

        # when
        configuration = Configuration()

        # then
        self.assertEqual(configuration.database_host, 'localhost')

if __name__ == '__main__':
    unittest.main()
