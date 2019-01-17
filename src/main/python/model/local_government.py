from src.main.python.model.aggregate_root import AggregateRoot


class LocalGovernment(AggregateRoot):

    def __init__(self,
                 ident: str = '',
                 name: str = '',
                 national_typology: dict = {},
                 domain_name: str = '',
                 domain_searched: bool = False,
                 official_council_reports: set = set()):
        self.id = ident
        self.name = name
        self.national_typology = national_typology
        self.domain_name = domain_name
        self.domain_searched = domain_searched
        self.official_council_reports = official_council_reports

    def get_id(self):
        return self.id

    def set_id(self, ident: str):
        self.id = ident
