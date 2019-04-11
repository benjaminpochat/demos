import os

from matplotlib import pyplot
import pickle
from sklearn import metrics
from tensorflow.python.keras import models

from src.main.python.commons.configuration import Configuration
from src.main.python.commons.data_subset_type import DataSubsetType
from src.main.python.process.training.text_dataset_producer.text_dataset_loader import TextAndLabelLoader

class RocCurveBuilder():

    def __init__(self):
        self.test_texts = None
        self.test_labels = None

    def build_roc_curve(self):
        self._load_test_texts_and_labels()
        false_positive_rates, true_positive_rates, thresholds, area_under_the_curve = self._get_roc_curve_data()
        self._draw_roc_curve(false_positive_rates, true_positive_rates, area_under_the_curve)

    def _get_roc_curve_data(self):
        predictions = self._get_model_predictions()
        false_positive_rates, true_positive_rates, thresholds = metrics.roc_curve(self.test_labels, predictions)
        area_under_the_curve = metrics.auc(false_positive_rates, true_positive_rates)
        return false_positive_rates, true_positive_rates, thresholds, area_under_the_curve

    def _draw_roc_curve(self, false_positive_rates, true_positive_rates, area_under_the_curve):
        pyplot.figure(1)
        pyplot.plot([0, 1], [0, 1], 'k--')
        pyplot.plot(false_positive_rates, true_positive_rates, label='Keras (area = {:.3f})'.format(area_under_the_curve))
        pyplot.xlabel('False positive rate')
        pyplot.ylabel('True positive rate')
        pyplot.title('ROC curve')
        pyplot.legend(loc='best')
        pyplot.show()

    def _load_test_texts_and_labels(self):
        text_and_label_loader = TextAndLabelLoader()
        self.test_texts, self.test_labels = text_and_label_loader.load_texts_and_labels_for_subset_type(DataSubsetType.TEST)

    def _load_and_reduce_vector(self):
        feature_selector_file_path = os.path.join(os.path.dirname(__file__), '../../../../resources/', Configuration().get_feature_selector_file())
        feature_selector = pickle.load(open(feature_selector_file_path, 'rb'))
        vectorizer_file_path = os.path.join(os.path.dirname(__file__), '../../../../resources/', Configuration().get_vectorizer_file())
        vectorizer = pickle.load(open(vectorizer_file_path, 'rb'))
        test_vector = vectorizer.transform(self.test_texts)
        reduced_test_vector = feature_selector.transform(test_vector).astype('float32')
        return reduced_test_vector

    def _get_model_predictions(self):
        reduced_test_vector = self._load_and_reduce_vector()
        keras_model = models.load_model('/home/benjamin/Documents/workspace/demos/src/main/resources/mlp_model.h5')
        class_predictions = keras_model.predict(reduced_test_vector)
        y_pred_keras = class_predictions.ravel()
        return y_pred_keras



