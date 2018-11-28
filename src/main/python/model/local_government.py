from src.main.python.model.agregate_root import AggregateRoot


class LocalGovernment(AggregateRoot):

    def __init__(self, id: str = '', name: str = '', national_typology: dict = {}, domain_name: str = ''):
        self.id = id
        self.name = name
        self.national_typology = national_typology
        self.domain_name = domain_name

    def get_id(self):
        return self.id
