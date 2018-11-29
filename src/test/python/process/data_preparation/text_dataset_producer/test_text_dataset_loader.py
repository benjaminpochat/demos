import unittest

from main.python.process.data_preparation.text_dataset_producer.text_dataset_loader import TextAndLabelLoader


class TestTextAndLabelLoader(unittest.TestCase):
    def test_randomize_training_texts_and_labels_should_shuffle_numbers_one_to_ten(self):
        # given
        texts = ['un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix']
        labels = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        loader = TextAndLabelLoader()

        # when
        shuffled_texts, shuffled_labels = loader.shuffle_texts_and_labels(texts, labels)

        # then
        self.assertEqual(shuffled_texts.index('un'), shuffled_labels.index('one'))
        self.assertEqual(shuffled_texts.index('deux'), shuffled_labels.index('two'))
        self.assertEqual(shuffled_texts.index('trois'), shuffled_labels.index('three'))
        self.assertEqual(shuffled_texts.index('quatre'), shuffled_labels.index('four'))
        self.assertEqual(shuffled_texts.index('cinq'), shuffled_labels.index('five'))
        self.assertEqual(shuffled_texts.index('six'), shuffled_labels.index('six'))
        self.assertEqual(shuffled_texts.index('sept'), shuffled_labels.index('seven'))
        self.assertEqual(shuffled_texts.index('huit'), shuffled_labels.index('eight'))
        self.assertEqual(shuffled_texts.index('neuf'), shuffled_labels.index('nine'))
        self.assertEqual(shuffled_texts.index('dix'), shuffled_labels.index('ten'))
        self.assertFalse(texts.index('un') == shuffled_texts.index('un')
                         and texts.index('deux') == shuffled_texts.index('deux')
                         and texts.index('trois') == shuffled_texts.index('trois')
                         and texts.index('quatre') == shuffled_texts.index('quatre')
                         and texts.index('cinq') == shuffled_texts.index('cinq')
                         and texts.index('six') == shuffled_texts.index('six')
                         and texts.index('sept') == shuffled_texts.index('sept')
                         and texts.index('huit') == shuffled_texts.index('huit')
                         and texts.index('neuf') == shuffled_texts.index('neuf')
                         and texts.index('dix') == shuffled_texts.index('dix'))