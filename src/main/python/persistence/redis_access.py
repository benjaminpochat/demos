from numpy.f2py.auxfuncs import throw_error

from src.main.python.model.aggregate_root import AggregateRoot

import redis
import json


class RedisAccess:
    """
    Access data persisted in Redis
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
            elif type(attribute_value) is bool:
                self._store_simple_attribute(aggregate_root, attribute_key, str(aggregate_root.__dict__[attribute_key]))

    def _store_simple_attribute(self, aggregate_root: AggregateRoot, attribute_key: str, attribute_value):
        self._redis.hset(
            self._get_aggregate_key(aggregate_root),
            attribute_key,
            attribute_value)

    def _store_dict_attribute(self, aggregate_root: AggregateRoot, attribute_key: str, attribute_value: dict):
        self._redis.hset(
            self._get_aggregate_key(aggregate_root),
            attribute_key,
            json.dumps(attribute_value))

    def list_aggregates(self, the_class: type, pattern: str= '*'):
        instances = []
        key_iterator = self._redis.scan_iter(the_class.__name__ + ':' + pattern)
        for key in key_iterator:
            key_as_str = key.decode()
            instance = the_class()
            aggregate_root_id = key_as_str[the_class.__name__.__len__() + 1:]
            for attribute_name in instance.__dict__.keys():
                if attribute_name == 'id':
                    attribute_value = aggregate_root_id
                else:
                    attribute_value = getattr(instance, attribute_name)
                    if attribute_value.__class__ == str:
                        attribute_value = self._redis.hget(key, attribute_name).decode()
                    elif attribute_value.__class__ == dict:
                        attribute_value = json.loads(self._redis.hget(key, attribute_name).decode())
                    elif attribute_value.__class__ == bool:
                        if self._redis.hget(key, attribute_name) is None:
                            attribute_value = False
                        elif self._redis.hget(key, attribute_name).decode().lower() == 'true':
                            attribute_value = True
                        else:
                            attribute_value = False
                setattr(instance, attribute_name, attribute_value)

            instances.append(instance)

        return instances

    def get_aggregate(self, the_class, aggregate_id):
        return self.list_aggregates(the_class=the_class, pattern=aggregate_id)[0]

    def get_random_aggregate(self, the_class: type):
        key = self._redis.randomkey()
        while not key.decode().startswith(the_class.__name__):
            key = self._redis.randomkey()
        aggregate_id = key.decode()[the_class.__name__.__len__() + 1:]
        return self.get_aggregate(the_class=the_class, aggregate_id=aggregate_id)
