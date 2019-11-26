import requests as requests

from commons.boolean_enum import Boolean
from commons.configuration import Configuration
from commons.loggable import Loggable
from model.classification import Classification
from process.abstract_pdf_classifier import AbstractClassifier
from process.operational_text_vectorizer import OperationalTextVectorizer


class RestClientPdfClassifier(AbstractClassifier, Loggable):

    def classify(self, text_content: str):
        if text_content is None:
            classification = Classification()
            classification.classified_as_official_council_report = Boolean.FALSE
            return classification
        vectorized_text = OperationalTextVectorizer().vectorize(text_content)  # csr_matrix (scipy)
        array_text = vectorized_text.toarray()  # ndarray (NumPy)
        tensorflow_serving_host = Configuration().get_tensorflow_serving_host()
        tensorflow_serving_port = Configuration().get_tensorflow_serving_port()
        url = 'http://' + tensorflow_serving_host + ':' + tensorflow_serving_port + '/v1/models/demos:predict'
        tensorflow_input = {"instances": array_text.tolist()}
        tensorflow_output = self._do_request_tensorflow_serving(tensorflow_input, url)
        class_predictions = tensorflow_output['predictions'][0]
        classifications = self.convert_predictions_as_classifications(class_predictions=class_predictions)
        return classifications[0]

    def _do_request_tensorflow_serving(self, tensorflow_input, url):
        response = requests.post(url=url, json=tensorflow_input)
        if response.status_code != 200:
            self.log_error('POST ' + url + ' status : {}'.format(response.status_code))
            self.log_error('POST ' + url + ' response : {}'.format(response.json()))
        else:
            self.log_debug('POST ' + url + ' status : {}'.format(response.status_code))
            self.log_debug('POST ' + url + ' response : {}'.format(response.json()))
        tensorflow_output = response.json()
        return tensorflow_output
