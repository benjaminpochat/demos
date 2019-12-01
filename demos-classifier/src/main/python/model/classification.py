from model.web_document import WebDocument
from commons.boolean_enum import Boolean


class Classification:
    """
    A class to represent a WebDocument's classification, i.e. the result of the classification process.
    """
    def __init__(self, web_document: WebDocument=None, class_prediction=None):
        self.web_document = web_document
        self.classified_as_official_council_report = Boolean.UNKNOWN
        self.class_prediction = class_prediction

    def isOfficialCouncilReport(self):
        return self.classified_as_official_council_report == Boolean.TRUE
