from abc import abstractmethod

from commons.boolean_enum import Boolean
from model.classification import Classification


class AbstractClassifier:

    @abstractmethod
    def classify(self, text_content: str):
        pass

    def convert_predictions_as_classifications(self, class_predictions):
        classifications = []
        for class_prediction in class_predictions:
            classification = Classification(class_prediction=class_prediction)
            if class_prediction > 0.5:
                classification.classified_as_official_council_report = Boolean.TRUE
            elif class_prediction < 0.5:
                classification.classified_as_official_council_report = Boolean.FALSE
        classifications.append(classification)
        return classifications