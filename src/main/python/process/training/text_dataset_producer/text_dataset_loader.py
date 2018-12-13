from src.main.python.commons.loggable import Loggable
from src.main.python.commons.boolean_enum import Boolean
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
        self._label_dict = {}
        self._label_index = 0

    def load_texts_and_labels(self, training_size: int, validation_size: int):
        """
        Load a set of training and validation texts and labels, randomly from database, to feed training ML model.
        :param training_size: the size of the training data set (texts and labels)
        :param validation_size: the size of the validation data set (texts and labels)
        :return: a tuple of 4 lists : training texts, training labels, validation texts, validation labels
        """
        self.log_info('Starts loading data')

        self._training_texts = []
        self._training_labels = []
        self._validation_texts = []
        self._validation_labels = []
        i = 0

        for web_document in self._get_random_web_documents_generator(training_size + validation_size):
            self.log_info('Loads web_document #' + str(i+1) + ' with id ' + web_document.id + ' (' + web_document.url + ')')
            if i < training_size:
                self._training_texts.append(web_document.text_content)
                self._training_labels.append(web_document.classified_as_official_report.to_int())
            else:
                self._validation_texts.append(web_document.text_content)
                self._validation_labels.append(web_document.classified_as_official_report.to_int())
            i += 1

        return self._training_texts, self._training_labels, self._validation_texts, self._validation_labels

    def _get_random_web_documents_generator(self, number_of_web_documents: int = 1):
        i = 0
        selected_web_documents = set()
        while i < number_of_web_documents:
            web_document = self._find_randomly_new_classified_web_document(selected_web_documents)
            yield web_document
            selected_web_documents.add(web_document)
            i += 1

    def _find_randomly_new_classified_web_document(self, selected_web_documents):
        web_document = self._redis_access.get_random_aggregate(WebDocument)
        while not self.is_random_web_document_acceptable(web_document, selected_web_documents):
            web_document = self._redis_access.get_random_aggregate(WebDocument)
        return web_document

    def is_random_web_document_acceptable(self, web_document: WebDocument, selected_web_documents: set):
        acceptable = web_document.classified_as_official_report == Boolean.TRUE
        acceptable = acceptable or web_document.classified_as_official_report == Boolean.FALSE
        acceptable = acceptable and not selected_web_documents.__contains__(web_document)
        return acceptable
