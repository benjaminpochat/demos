import requests as requests

from src.main.python.commons.configuration import Configuration
from src.main.python.commons.loggable import Loggable
from src.main.python.process.archiving.abstract_pdf_classifier import AbstractClassifier
from src.main.python.process.archiving.operational_text_vectorizer import OperationalTextVectorizer


class RestClientPdfClassifier(AbstractClassifier, Loggable):
    #TODO : utiliser ce classifier (avec l'option -tfs) avec le web crawler
    #TODO : optimiser les import pout faire une petite image Docker du client

    def classify(self, text_content: str):
        vectorized_text = OperationalTextVectorizer().vectorize(text_content)  # csr_matrix (scipy)
        array_text = vectorized_text.toarray()  # ndarray (NumPy)
        tensorflow_serving_host = Configuration().get_tensortflow_serving_host()
        tensorflow_serving_port = Configuration().get_tensortflow_serving_port()
        url = 'http://' + tensorflow_serving_host + ':' + tensorflow_serving_port + '/v1/models/demos:predict'
        tensorflow_input = {"instances": array_text.tolist()}
        tensorflow_output = self.do_request_tensorflow_serving(tensorflow_input, url)
        class_predictions = tensorflow_output['predictions'][0]
        classifications = self.convert_predictions_as_classifications(class_predictions=class_predictions)
        return classifications[0]

    def do_request_tensorflow_serving(self, tensorflow_input, url):
        response = requests.post(url=url,
                                 json=tensorflow_input)
        if response.status_code != 200:
            self.log_error('POST ' + url + ' status : {}'.format(response.status_code))
            self.log_error('POST ' + url + ' response : {}'.format(response.json()))
        else:
            self.log_debug('POST ' + url + ' status : {}'.format(response.status_code))
            self.log_debug('POST ' + url + ' response : {}'.format(response.json()))
        tensorflow_output = response.json()
        return tensorflow_output
