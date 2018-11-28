import unittest

from main.python.process.data_preparation.text_dataset_producer.text_dataset_producer import TextDatasetProducer


class TestTextDatasetProducer(unittest.TestCase):

    def test_build_dataset_from_word_list(self):
        # given
        word_list = ['il', 'pleut', 'comme', 'vache', 'qui', 'pisse', 'et', 'qui', 'transpire', 'comme', 'un', 'boeuf', 'qui', 'tache']
        number_of_words = 3
        producer = TextDatasetProducer()

        # when
        result = producer.build_dataset_from_word_list(word_list, number_of_words)

        # then
        print(result)
        self.assertTupleEqual(
            result,
            ([0, 0, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0],
             [['UNKNOWN', 9], ('qui', 3), ('comme', 2)],
             {'UNKNOWN': 0, 'comme': 2, 'qui': 1},
             {0: 'UNKNOWN', 1: 'qui', 2: 'comme'}))

    def test_build_dataset_from_text(self):
        # given
        text = 'il pleut comme vache qui pisse et qui transpire comme un boeuf qui tache'
        number_of_words = 3
        producer = TextDatasetProducer()

        # when
        result = producer.build_dataset_from_text(text, number_of_words)

        # then
        print(result)
        self.assertTupleEqual(
            result,
            ([0, 0, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0],
             [['UNKNOWN', 9], ('qui', 3), ('comme', 2)],
             {'UNKNOWN': 0, 'comme': 2, 'qui': 1},
             {0: 'UNKNOWN', 1: 'qui', 2: 'comme'}))


if __name__ == '__main__':
    unittest.main()
