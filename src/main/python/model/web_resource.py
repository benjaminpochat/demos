import hashlib

from src.main.python.model.aggregate_root import AggregateRoot
from src.main.python.model.local_government import LocalGovernment
from src.main.python.commons.boolean_enum import Boolean


class WebDocument(AggregateRoot):
    """
    An object that represents a document found on the web.
    """
    def __init__(self, text_content: str = '', url: str = '', local_government: LocalGovernment = LocalGovernment()):
        self.text_content = text_content
        self.url = url
        self.local_government = local_government
        self.classified_as_official_report = Boolean.UNKNOWN

    def get_id(self):
        sha1_process = hashlib.sha1()
        sha1_process.update(bytes(self.text_content, 'utf-8'))
        return sha1_process.hexdigest()


