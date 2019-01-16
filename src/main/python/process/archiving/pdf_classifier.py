import os
import pickle

from tensorflow.python.keras import models
from sklearn.feature_extraction.text import TfidfVectorizer

from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.classification import Classification
from src.main.python.commons.configuration import Configuration


class LocalGovernmentPdfClassifier:
    def __init__(self):
        self._configuration = Configuration()
        self._model = self._load_model()
        self._vocabulary = self._load_vocabulary()

    def classify(self, text_content: list):
        tf_idf_vectorizer = TfidfVectorizer(ngram_range=(1,2),
                                            dtype='int32',
                                            strip_accents='unicode',
                                            decode_error='replace',
                                            analyzer='word',
                                            min_df=2,
                                            vocabulary=self._vocabulary)
        vectorized_texts = tf_idf_vectorizer.fit_transform(text_content)
        class_predictions = self._model.predict(vectorized_texts, verbose=1)
        classifications = self.convert_predictions_as_classifications(class_predictions)
        return classifications

    def convert_predictions_as_classifications(self, class_predictions):
        classifications = []
        for class_prediction in class_predictions:
            classification = Classification()
            if class_prediction > 0.75:
                classification.classified_as_official_council_report = Boolean.TRUE
            elif class_prediction < 0.25:
                classification.classified_as_official_council_report = Boolean.FALSE
        classifications.append(classification)
        return classifications

    def _load_vocabulary(self):
        vocabulary_file_path = os.path.join(
            os.path.dirname(__file__),
            '../../../resources/',
            self._configuration.get_vocabulary_file())
        vocabulary = pickle.load(open(vocabulary_file_path, 'rb'))
        return vocabulary

    def _load_model(self):
        model_file_path = os.path.join(
            os.path.dirname(__file__),
            '../../../resources/',
            self._configuration.get_model_file())
        model = models.load_model(model_file_path)
        return model
