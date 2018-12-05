import unittest
import numpy as np

from main.python.process.training.text_dataset_producer.text_ngrams_vectorizer import NgramVectorizer
from main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader


class TestTextNgramsVectorizer(unittest.TestCase):

    def test_vectorize_few_small_texts(self):
        # given
        vectorizer = NgramVectorizer()

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

    def test_vectorize_few_big_texts(self):
        # given
        vectorizer = NgramVectorizer()
        text_file_root_folder = 'src/test/resources/process/training/text_dataset_producer'
        training_text_files_folder = 'training'
        validation_text_files_folder = 'validation'
        text_and_label_loader = TextAndLabelLoader()
        texts_and_labels = text_and_label_loader.load_texts_and_labels(
            text_file_root_folder,
            training_text_files_folder,
            validation_text_files_folder)

        # when
        vectors = vectorizer.ngram_vectorize(
            texts_and_labels[0],
            texts_and_labels[1],
            texts_and_labels[2])

        # then
        print('Train results')
        print(vectors[0])
        print('Validation results')
        print(vectors[1])

if __name__ == '__main__':
    unittest.main()