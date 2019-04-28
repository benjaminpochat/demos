import os

from tensorflow.python.keras import models

from src.main.python.commons.boolean_enum import Boolean
from src.main.python.model.classification import Classification
from src.main.python.commons.configuration import Configuration
from src.main.python.process.archiving.vectorizer import Vectorizer


class LocalGovernmentPdfClassifier:
    def __init__(self):
        self._configuration = Configuration()
        self._model = self._load_model()

    def classify(self, text_content: str):
        vectorized_text = Vectorizer().vectorize(text_content)
        class_predictions = self._model.predict([vectorized_text], verbose=1)
        classifications = self.convert_predictions_as_classifications(class_predictions)
        return classifications[0]

    def convert_predictions_as_classifications(self, class_predictions):
        classifications = []
        for class_prediction in class_predictions:
            classification = Classification(class_prediction=class_prediction)
            if class_prediction > 0.75:
                classification.classified_as_official_council_report = Boolean.TRUE
            elif class_prediction < 0.25:
                classification.classified_as_official_council_report = Boolean.FALSE
        classifications.append(classification)
        return classifications

    def _load_model(self):
        model_file_path = os.path.join(
            os.path.dirname(__file__),
            '../../../resources/',
            self._configuration.get_model_file())
        model = models.load_model(model_file_path)
        return model
