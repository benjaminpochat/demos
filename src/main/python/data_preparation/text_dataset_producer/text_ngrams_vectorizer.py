from builtins import range

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif


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

    def __init__(self, ngram_range :range = (1, 2), feature_number_limit :int = 20000, token_mode :str = 'word', min_document_token_frequency :int = 2):
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
        # Create keyword arguments to pass to the 'tf-idf' vectorizer.
        kwargs = {
                'ngram_range': self._ngram_range,  # Use 1-grams + 2-grams.
                'dtype': 'int32',
                'strip_accents': 'unicode',
                'decode_error': 'replace',
                'analyzer': self._token_mode,  # Split text into word tokens.
                'min_df': self._min_document_token_frequency,
        }
        tf_idf_vectorizer = TfidfVectorizer(**kwargs)

        # Learn vocabulary from training texts and vectorize training texts.
        training_vector = tf_idf_vectorizer.fit_transform(training_texts)

        # Vectorize validation texts.
        validation_vector = tf_idf_vectorizer.transform(validation_texts)

        # Select top 'k' of the vectorized features.
        selector = SelectKBest(f_classif, k=min(self._feature_number_limit, training_vector.shape[1]))
        selector.fit(training_vector, training_labels)
        training_vector = selector.transform(training_vector).astype('float32')
        validation_vector = selector.transform(validation_vector).astype('float32')
        return training_vector, validation_vector

