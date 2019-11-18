import random

from src.main.python.commons.data_subset_type import DataSubsetType
from src.main.python.commons.loggable import Loggable
from src.main.python.model.web_resource import WebDocument
from src.main.python.persistence.redis_access import RedisAccess


class TextAndLabelLoader(Loggable):
    """
    Load a set of training and validation texts and labels, randomly from database, to feed training ML model.
    """

    def __init__(self):
        super().__init__()
        self._redis_access = RedisAccess()
        self._training_texts = []
        self._training_labels = []
        self._validation_texts = []
        self._validation_labels = []

    def load_texts_and_labels(self):
        """
        Load training and validation subsets of data (texts and labels) from database, to feed training ML model.
        The subsets are shuffled.
        :return: a tuple of 4 lists : training texts, training labels, validation texts, validation labels
        """
        self.log_info('Starts loading data')

        self._training_texts, self._training_labels = self.load_texts_and_labels_for_subset_type(DataSubsetType.TRAINING)
        self._validation_texts, self._validation_labels = self.load_texts_and_labels_for_subset_type(DataSubsetType.VALIDATION)

        return self._training_texts, self._training_labels, self._validation_texts, self._validation_labels

    def load_texts_and_labels_for_subset_type(self, subset_type: DataSubsetType):
        keys = self._redis_access.search_aggregate_keys_by_attribute_value(WebDocument, 'subset_type', subset_type)
        random.shuffle(keys)
        web_documents = [self._redis_access.get_aggregate(WebDocument, key) for key in keys]
        texts = [web_document.text_content for web_document in web_documents]
        labels = [web_document.classified_as_official_report.to_int() for web_document in web_documents]
        return texts, labels
