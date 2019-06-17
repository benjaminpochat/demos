from tensorflow.python.keras import models

from src.main.python.commons.configuration import Configuration
from src.main.python.process.archiving.abstract_pdf_classifier import AbstractClassifier
from src.main.python.process.archiving.operational_text_vectorizer import OperationalTextVectorizer

class LocalPdfClassifier(AbstractClassifier):
    """
    A classifier that uses only local path's code.
    This classifier is for local tests.
    For production deployment, see RestClientClassifier.
    """

    def __init__(self):
        self._configuration = Configuration()
        self._model = models.load_model(Configuration().get_keras_model_file_path())

    def classify(self, text_content: str):
        vectorized_text = OperationalTextVectorizer().vectorize(text_content)
        class_predictions = self._model.predict([vectorized_text], verbose=1)
        classifications = self.convert_predictions_as_classifications(class_predictions)
        return classifications[0]


