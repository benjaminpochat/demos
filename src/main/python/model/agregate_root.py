class AggregateRoot:
    '''Define an agregate root of a domain model'''

    def get_id(self):
        raise AttributeError(repr(self) + " has no id implemented")