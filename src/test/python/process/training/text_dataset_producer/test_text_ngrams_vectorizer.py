import os
import unittest
from unittest.mock import Mock

import numpy as np

from src.main.python.commons.configuration import Configuration
from src.main.python.process.training.text_dataset_producer.text_ngrams_vectorizer import NgramVectorizer
from src.main.python.commons.boolean_enum import Boolean


class TestTextNgramsVectorizer(unittest.TestCase):

    def test_vectorize_few_small_texts(self):
        # given
        vectorizer = NgramVectorizer()
        vectorizer.get_vectorizer_file_path = Mock(return_value=vectorizer.get_vectorizer_file_path().replace(".pkl", ".test.pkl"))
        vectorizer.get_feature_selector_file_path = Mock(return_value=vectorizer.get_feature_selector_file_path().replace(".pkl", ".test.pkl"))

        # when
        vectors = vectorizer.ngram_vectorize(
            ['J''avoue j''en ai bavé pas vous, mon amour, avant d''avoir eu vent de vous, mon amour',
             'J''me fais des rides, en Ford Mustang',
             'Le carré de l''hypothenus est égal à la somme des carrés des côtés',
             'Dans le port d''Amsterdam, y''a des marins qui chantent',
             'L''amour est enfant de Bohème qui n''a jamais jamais connu de loi',
             'dans un plan, une droite parallèle à l''un des côtés d''un triangle sectionne ce dernier en un triangle semblable'],
            np.array([['poésie'], ['poésie'], ['math'], ['poésie'], ['poésie'], ['math']], np.str_),
            ['Hélas avril en vain me voue, à l''amour',
             'Et j''avais voulu voir en vous, cet amour'])

        # then
        print('Train results')
        print(vectors[0])
        print('Validation results')
        print(vectors[1])
        os.remove(vectorizer.get_feature_selector_file_path())
        os.remove(vectorizer.get_vectorizer_file_path())


    def test_vectorize_few_big_texts(self):
        # given
        vectorizer = NgramVectorizer()
        vectorizer.get_vectorizer_file_path = Mock(return_value=vectorizer.get_vectorizer_file_path().replace(".pkl", ".test.pkl"))
        vectorizer.get_feature_selector_file_path = Mock(return_value=vectorizer.get_feature_selector_file_path().replace(".pkl", ".test.pkl"))
        demos_home = Configuration().get_demos_home()
        common_path = os.path.join(demos_home, 'src', 'test', 'resources', 'process', 'training', 'text_dataset_producer', 'training')

        file1 = open(os.path.join(common_path, 'city_council_report', 'CM%2001%2007%202013%20-%20Proc%C3%A8s-verbal.pdf.txt'))
        file2 = open(os.path.join(common_path, 'city_council_report', 'CM%2015%2009%202014-%20Proc%C3%A8s-verbal.pdf.txt'))
        file3 = open(os.path.join(common_path, 'others', 'Actus%20politique%20de%20la%20ville%201.pdf.txt'))
        file4 = open(os.path.join(common_path, 'city_council_report', 'CM17.05.23%20-%20PV.pdf.txt'))

        # when
        vectors = vectorizer.ngram_vectorize(
            [file1.read(), file2.read(), file3.read()],
            [Boolean.TRUE.to_int(), Boolean.TRUE.to_int(), Boolean.FALSE.to_int()],
            [file4.read()])

        # then
        print('Train results')
        print(vectors[0])
        print('Validation results')
        print(vectors[1])
        os.remove(vectorizer.get_feature_selector_file_path())
        os.remove(vectorizer.get_vectorizer_file_path())


if __name__ == '__main__':
    unittest.main()
