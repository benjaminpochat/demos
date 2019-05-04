import pickle

from src.main.python.commons.configuration import Configuration


class Vectorizer:
    """
    A class to convert texts to vectors.
    The vectorization process uses :
    * the vectorizer that has been previously saved as the pickle file given in vectorizer_file property
    * the feature selector that has been previously saved as the pickle file given in feature_selector_file property
    """

    def __init__(self):
        self.feature_selector = pickle.load(open(Configuration().get_feature_selector_file_path(), 'rb'))
        self.vectorizer = pickle.load(open(Configuration().get_vectorizer_file_path(), 'rb'))

    def vectorize(self, text: str):
        vector = self.vectorizer.transform([text])
        reduced_vector = self.feature_selector.transform(vector).astype('float32')
        return reduced_vector
