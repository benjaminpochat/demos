import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

from src.main.python.commons.configuration import Configuration


class NgramVectorizer:
    """A class that tokenize and vectorize texts

    Attributes:
        _ngram_range                    Range (inclusive) of n-gram sizes for tokenizing text.
        _feature_number_limit           Limit on the number of features. We use the top 20K features.
        _token_mode                     Whether text should be split into word or character n-grams.
                                        One of 'word', 'char'.
        _min_document_token_frequency   Minimum document/corpus frequency below which a token will be discarded.

    see https://developers.google.com/machine-learning/guides/text-classification/step-3#n-gram_vectors_option_a
    """

    def __init__(self, ngram_range: range = (1, 2), feature_number_limit: int = 20000, token_mode: str = 'word', min_document_token_frequency: int = 2):
        self._ngram_range = ngram_range
        self._feature_number_limit = feature_number_limit
        self._token_mode = token_mode
        self._min_document_token_frequency = min_document_token_frequency

    def ngram_vectorize(self, training_texts, training_labels, validation_texts):
        """Vectorizes texts as n-gram vectors.

        1 text = 1 tf-idf vector the length of vocabulary of unigrams + bigrams.

        # Arguments
            training_texts: list, training text strings.
            training_labels: np.ndarray, training labels.
            validation_texts: list, validation text strings.

        # Returns
            training_vector, validation_vector: vectorized training and validation texts
        """
        tf_idf_vectorizer = self._initialize_tf_idf_vectorizer()

        # Learn vocabulary from training texts and vectorize training texts.
        training_vector = tf_idf_vectorizer.fit_transform(training_texts)

        # Learn vocabulary from validation texts and vectorize validation texts.
        validation_vector = tf_idf_vectorizer.transform(validation_texts)

        # Select top 'k' of the vectorized features.
        best_feature_selector = self._get_best_features_selector(training_labels, training_vector)
        reduced_training_vector = self._reduce_vector_to_best_features(best_feature_selector, training_vector)
        reduced_validation_vector = self._reduce_vector_to_best_features(best_feature_selector, validation_vector)

        self.save_tf_idf_vectorizer(tf_idf_vectorizer)
        self.save_best_feature_selector(best_feature_selector)

        return reduced_training_vector, reduced_validation_vector

    def _reduce_vector_to_best_features(self, best_feature_selector: SelectKBest, training_vector):
        return best_feature_selector.transform(training_vector).astype('float32')

    def _get_best_features_selector(self, training_labels, training_vector):
        selector = SelectKBest(f_classif, k=min(self._feature_number_limit, training_vector.shape[1]))
        selector.fit(training_vector, training_labels)
        return selector

    def _initialize_tf_idf_vectorizer(self):
        tf_idf_vectorizer = TfidfVectorizer(
            ngram_range=self._ngram_range,
            dtype='int32',
            strip_accents='unicode',
            decode_error='replace',
            analyzer=self._token_mode,
            min_df=self._min_document_token_frequency
        )
        return tf_idf_vectorizer

    def save_tf_idf_vectorizer(self, tf_idf_vectorizer: TfidfVectorizer):
        vectorizer_file = open(self.get_vectorizer_file_path(), 'wb')
        pickle.dump(tf_idf_vectorizer, vectorizer_file)
        vectorizer_file.close()

    def get_vectorizer_file_path(self):
        return Configuration().get_vectorizer_file_path()

    def save_best_feature_selector(self, best_feature_selector: SelectKBest):
        feature_selector_file = open(self.get_feature_selector_file_path(), 'wb')
        pickle.dump(best_feature_selector, feature_selector_file)
        feature_selector_file.close()

    def get_feature_selector_file_path(self):
        return Configuration().get_feature_selector_file_path()
