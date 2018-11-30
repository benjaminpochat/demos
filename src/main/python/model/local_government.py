from src.main.python.model.aggregate_root import AggregateRoot


class LocalGovernment(AggregateRoot):

    def __init__(self, id: str = None, name: str = None, national_typology: dict = {}, domain_name: str = None):
        self.id = id
        self.name = name
        self.national_typology = national_typology
        self.domain_name = domain_name

    def get_id(self):
        return self.id
