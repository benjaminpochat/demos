from model.aggregate_root import AggregateRoot


class LocalGovernment(AggregateRoot):

    def __init__(self,
                 ident: str = '',
                 name: str = '',
                 domain_name: str = '',
                 official_council_reports: set = set()):
        self.id = ident
        self.name = name
        self.domain_name = domain_name
        self.official_council_reports = official_council_reports

    def get_id(self):
        return self.id

    def set_id(self, ident: str):
        self.id = ident
