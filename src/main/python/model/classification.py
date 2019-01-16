from src.main.python.model.web_resource import WebDocument
from src.main.python.commons.boolean_enum import Boolean


class Classification:
    """
    A class to represent a WebDocument's classification, i.e. the result of the classification process.
    """
    def __init__(self, web_document: WebDocument = None):
        self.web_document = web_document
        self.classified_as_official_council_report = Boolean.UNKNOWN

    def isOfficialCouncilReport(self):
        return self.classified_as_official_council_report == Boolean.TRUE
