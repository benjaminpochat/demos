from builtins import isinstance

import redis
import json

from src.main.python.model.aggregate_root import AggregateRoot
from enum import Enum


class RedisAccess:
    """
    Access data stored in Redis database
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
            if attribute_value is None:
                self._remove_attribute(aggregate_root, attribute_key)
            elif type(attribute_value) is str:
                self._store_simple_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif type(attribute_value) is int:
                self._store_simple_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif type(attribute_value) is dict:
                self._store_dict_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif type(attribute_value) is bool:
                self._store_simple_attribute(aggregate_root, attribute_key, str(aggregate_root.__dict__[attribute_key]))
            elif isinstance(attribute_value, Enum):
                self._store_simple_attribute(aggregate_root, attribute_key, str(aggregate_root.__dict__[attribute_key]))
            elif isinstance(attribute_value, AggregateRoot):
                self._store_simple_attribute(aggregate_root, attribute_key, self._get_aggregate_key(attribute_value))

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
        """
        Returns a list of loaded aggregate roots, matching with a class and a identifier pattern
        :param the_class: the class of object that should be read from database. Must be a subclass of AggregateRoot
        :param pattern: the pattern that should match object ids
        :return: a list of aggregate roots, with data loaded
        """
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
                        attribute_value = self._load_str_attribute(attribute_name, key)
                    if attribute_value.__class__ == int:
                        attribute_value = self._load_int_attribute_value(attribute_name, key)
                    elif attribute_value.__class__ == dict:
                        attribute_value = self._load_dict_attribute_value(attribute_name, key)
                    elif attribute_value.__class__ == bool:
                        attribute_value = self._load_bool_attribute_value(attribute_name, key)
                    elif issubclass(attribute_value.__class__, Enum):
                        attribute_value = self._load_enum_attribute_value(attribute_name, attribute_value.__class__, key)
                    elif issubclass(attribute_value.__class__, AggregateRoot):
                        attribute_value = self._load_aggregate_root_attribute(attribute_name, attribute_value.__class__, key)
                setattr(instance, attribute_name, attribute_value)
            instances.append(instance)

        return instances

    def _load_bool_attribute_value(self, attribute_name, key):
        if self._load_str_attribute(attribute_name, key).lower() == 'true':
            attribute_value = True
        else:
            attribute_value = False
        return attribute_value

    def _load_dict_attribute_value(self, attribute_name, key):
        return json.loads(self._load_str_attribute(attribute_name, key))

    def _load_int_attribute_value(self, attribute_name, key):
        return int(self._load_str_attribute(attribute_name, key))

    def _load_str_attribute(self, attribute_name, key):
        return self._redis.hget(key, attribute_name).decode()

    def _load_enum_attribute_value(self, attribute_name, enum_class, key):
        enum_str_value = self._redis.hget(key, attribute_name)
        attribute_value = None
        if enum_str_value is not None:
            attribute_value = enum_class(enum_str_value.decode()[enum_class.__name__.__len__() + 1:])
        return attribute_value

    def _load_aggregate_root_attribute(self, attribute_name, aggregate_root_class, key):
        aggregate_root_id_str_value = self._redis.hget(key, attribute_name)
        attribute_value = None
        if aggregate_root_id_str_value is not None:
            attribute_value = aggregate_root_class()
            attribute_value.set_id(aggregate_root_id_str_value.decode()[len(aggregate_root_class.__name__) + 1:])
        return attribute_value

    def _remove_attribute(self, aggregate_root, attribute_key):
        self._redis.hdel(self._get_aggregate_key(aggregate_root), attribute_key)

    def get_aggregate(self, the_class, aggregate_id):
        """
        Gets one single aggregate root
        :param the_class: the class of the object to read. Must be a subclass of AggregateRoot
        :param aggregate_id: the id of the object to read
        :return: an instance of the given class
        """
        return self.list_aggregates(the_class=the_class, pattern=aggregate_id)[0]

    def get_random_aggregate(self, the_class: type):
        """
        Gets randomly an aggregate root from the database
        :param the_class: the class of the object to get. Must be a subclass of AggregateRoot
        :return: a random instance
        """
        key = self._redis.randomkey()
        while not key.decode().startswith(the_class.__name__):
            key = self._redis.randomkey()
        aggregate_id = key.decode()[the_class.__name__.__len__() + 1:]
        return self.get_aggregate(the_class=the_class, aggregate_id=aggregate_id)
