import hashlib

from model.aggregate_root import AggregateRoot
from model.local_government import LocalGovernment
from commons.boolean_enum import Boolean


class WebDocument(AggregateRoot):
    """
    An object that represents a document found on the web.
    """
    def __init__(self, ident: str = '', text_content: str = '', url: str = '', local_government: LocalGovernment = LocalGovernment()):
        self.id = ident
        self.text_content = text_content
        self.url = url
        self.local_government = local_government
        self.classified_as_official_report = Boolean.UNKNOWN

    def get_id(self):
        return self.id

    def set_id(self, ident: str):
        self.id = ident

    def generate_id(self):
        sha1_process = hashlib.sha1()
        sha1_process.update(bytes(self.text_content, 'utf-8'))
        return sha1_process.hexdigest()
