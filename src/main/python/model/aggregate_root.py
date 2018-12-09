class AggregateRoot:
    """
    Define an aggregate root of a domain model
    """

    def get_id(self):
        raise AttributeError(repr(self) + " has no get_id() implemented")

    def set_id(self, id: str):
        raise AttributeError(repr(self) + " has no set_id() implemented")
