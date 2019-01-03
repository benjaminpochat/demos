from tensorflow.python.keras import models
from sklearn.feature_extraction.text import TfidfVectorizer

from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.classification import Classification


class LocalGovernmentPdfClassifier:
    def __init__(self, model: models, vocabulary: dict):
        self._model = model
        self._vocabulary = vocabulary

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
        classifications = []
        for class_prediction in class_predictions:
            classification = Classification()
            if class_prediction > 0.75:
                classification.classified_as_official_council_report = Boolean.TRUE
            elif class_prediction < 0.25:
                classification.classified_as_official_council_report = Boolean.FALSE
        classifications.append(classification)

        return classifications
