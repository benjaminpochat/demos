from src.main.python.model.aggregate_root import AggregateRoot

import redis
import json


class RedisAccess:
    """
    Access data persisted in Redis
    #TODO : use hset instead of set redis command
    #TODO : check if the connexion should be closed properly
    """

    def __init__(self, host: str = 'localhost', port: int = '6379', db: int = 0):
        self._redis = redis.Redis(host, port, db)

    def _get_aggregate_key(self, aggregate_root: AggregateRoot):
        return aggregate_root.__class__.__name__ + ':' + aggregate_root.get_id()

    def store_aggregate(self, aggregate_root: AggregateRoot):
        """
        Stores an aggregate root and the whole aggregate beneath in a Redis database
        :param aggregate_root:
        :return:
        """
        for attribute_key in aggregate_root.__dict__.keys():
            attribute_value = aggregate_root.__dict__[attribute_key]
            if type(attribute_value) is str:
                self._store_simple_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif type(attribute_value) is int:
                self._store_simple_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif type(attribute_value) is dict:
                self._store_dict_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])

    def _store_simple_attribute(self, aggregate_root, attribute_key, attribute_value):
        self._redis.hset(
            self._get_aggregate_key(aggregate_root),
            attribute_key,
            attribute_value)

    def _store_dict_attribute(self, aggregate_root, attribute_key, attribute_value):
        self._redis.hset(
            self._get_aggregate_key(aggregate_root),
            attribute_key,
            json.dumps(attribute_value))
