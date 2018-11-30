import unittest

from unittest.mock import MagicMock
from src.main.python.model.local_government import LocalGovernment
from src.main.python.process.local_government_initialization.local_government_initializer import LocalGovernmentInitializer


class TestLocalGovernmentInitializer(unittest.TestCase):
    def test_try_domain_should_return_first_try(self):
        # given
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'Béchy'}
        commune.id = 'bechy'
        initializer = LocalGovernmentInitializer()
        initializer.get_page = MagicMock(return_value='site web de la commune de Béchy')

        # when
        initializer.find_domain(commune)

        # then
        self.assertEqual(commune.domain_name, 'bechy.fr')

    def test_try_domain_should_return_nothing(self):
        # given
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'Gruffy'}
        initializer = LocalGovernmentInitializer()
        initializer.get_page = MagicMock(return_value='Le site commercial de l\épicerie de Gruffy')

        # when
        initializer.find_domain(commune)

        # then
        self.assertEqual(commune.domain_name, None)

    def test_try_domain_should_set_domain_if_dash_ommited(self):
        # given
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'La Chapelle-Faucher'}
        commune.id = 'le_chapelle_faucher'
        initializer = LocalGovernmentInitializer()
        initializer.get_page = MagicMock(return_value='Le site de la commune de La Chapelle Faucher')

        # when
        initializer.find_domain(commune)

        # then
        self.assertEqual(commune.domain_name, 'la_chapelle_faucher.fr')

    def test_get_domain_tries_for_Guerandes_with_an_accent(self):
        # given
        initializer = LocalGovernmentInitializer()
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'Guérandes'}

        # when
        domains = initializer.get_domain_tries(commune)

        # then
        self.assertTrue(domains.__contains__('guerandes.fr'))
        self.assertTrue(domains.__contains__('guerandes.com'))
        self.assertTrue(domains.__contains__('guerandes.org'))
        self.assertTrue(domains.__contains__('ville-guerandes.fr'))

    def test_get_domain_tries_for_Le_Mans_with_space(self):
        # given
        initializer = LocalGovernmentInitializer()
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'Le Mans'}

        # when
        domains = initializer.get_domain_tries(commune)

        # then
        self.assertTrue(domains.__contains__('lemans.fr'), 'domains does not contain \'lemans.fr\'')
        self.assertTrue(domains.__contains__('le-mans.fr'), 'domains does not contain \'le-mans.fr\'')
        self.assertTrue(domains.__contains__('le_mans.fr'), 'domains does not contain \'le_mans.fr\'')
        self.assertTrue(domains.__contains__('lemans.com'), 'domains does not contain \'lemans.com\'')
        self.assertTrue(domains.__contains__('le-mans.com'), 'domains does not contain \'le-mans.com\'')
        self.assertTrue(domains.__contains__('le_mans.com'), 'domains does not contain \'le_mans.com\'')
        self.assertTrue(domains.__contains__('lemans.org'), 'domains does not contain \'lemans.fr\'')
        self.assertTrue(domains.__contains__('le-mans.org'), 'domains does not contain \'le-mans.org\'')
        self.assertTrue(domains.__contains__('le_mans.org'), 'domains does not contain \'le_mans.org\'')
        self.assertTrue(domains.__contains__('ville-le-mans.fr'), 'domains does not contain \'ville-le-mans.fr\'')
        self.assertTrue(domains.__contains__('ville-le_mans.fr'), 'domains does not contain \'ville-le_mans.fr\'')
        self.assertTrue(domains.__contains__('ville-le_mans.fr'), 'domains does not contain \'ville-le_mans.fr\'')

    def test_get_domain_tries_for_L_Hopital_with_quote_and_accent(self):
        # given
        initializer = LocalGovernmentInitializer()
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'L\'Hôpital'}

        # when
        domains = initializer.get_domain_tries(commune)

        # then
        self.assertTrue(domains.__contains__('lhopital.fr'))
        self.assertTrue(domains.__contains__('l-hopital.fr'))
        self.assertTrue(domains.__contains__('l_hopital.fr'))

    def test_try(self):
        # given
        commune = LocalGovernment()
        commune.national_typology = {'nom_complet': 'Champs'}
        initializer = LocalGovernmentInitializer()
        #initializer.get_page = MagicMock(return_value='site web de la commune de Béchy')

        # when
        initializer.find_domain(commune)

        # then
        print(commune.domain_name)

#lachapellefaucher

if __name__ == '__main__':
    unittest.main()