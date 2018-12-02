import hashlib

from src.main.python.model.aggregate_root import AggregateRoot

class WebResource(AggregateRoot):
    def __init__(self, text_content: str = '', url: str = ''):
        self.text_content = text_content
        self.url = url

    def get_id(self):
        sha1_process = hashlib.sha1()
        sha1_process.update(bytes(self.url))
        return sha1_process.hexdigest()


