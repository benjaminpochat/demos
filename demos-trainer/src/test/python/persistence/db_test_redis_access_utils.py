import unittest

from redis import Redis

from src.main.python.model.aggregate_root import AggregateRoot
from src.main.python.commons.configuration import Configuration


class VerySimpleAggregateRoot(AggregateRoot):
    def __init__(self, id: str = ''):
        self.id = id

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id


class AbstractTestRedisAccessForAggregate(unittest.TestCase):
    """
    An abstract unittest abstract class that should be implemented
    to test RedisAccess with specific AggregateRoot objects
    """
    def setUp(self):
        configuration = Configuration()
        self._redis = Redis(host=configuration.get_database_host(), port= configuration.get_database_port())
        self._reset_database()

    def tearDown(self):
        self._reset_database()

    def _reset_database(self):
        keys = self._redis.keys(self.get_aggregate_root_class().__name__ + ':*')
        if keys.__len__() > 0:
            self._redis.delete(*keys)

    def get_aggregate_root_class(self):
        raise AttributeError(repr(self) + " has no get_aggregate_root_class() implemented")