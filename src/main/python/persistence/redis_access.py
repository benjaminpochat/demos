from builtins import isinstance

import redis
import json
import re

from src.main.python.model.aggregate_root import AggregateRoot
from src.main.python.commons.configuration import Configuration
from src.main.python.commons.loggable import Loggable
from enum import Enum


class RedisAccess(Loggable):
    """
    Access data stored in Redis database
    """

    def __init__(self):
        super().__init__()
        configuration = Configuration()
        self._redis = redis.Redis(configuration.get_database_host(), configuration.get_database_port())

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
            elif type(attribute_value) is list:
                self._store_list_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif type(attribute_value) is set:
                self._store_set_attribute(aggregate_root, attribute_key, aggregate_root.__dict__[attribute_key])
            elif isinstance(attribute_value, Enum):
                self._store_simple_attribute(aggregate_root, attribute_key, str(aggregate_root.__dict__[attribute_key]))
            elif isinstance(attribute_value, AggregateRoot):
                self._store_simple_attribute(aggregate_root, attribute_key, self._get_aggregate_key(attribute_value))

    def delete_aggregate(self, aggregate_root: AggregateRoot):
        """
        Deletes the aggregate
        :param aggregate_root: the aggregate to be deleted
        :return:
        """
        self._redis.delete(self._get_aggregate_key(aggregate_root))

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

    def _store_list_attribute(self, aggregate_root: AggregateRoot, attribute_key: str, attribute_value: list):
        #TODO : use list redis feature (lset)
        attribute_value_as_str = ';'
        attribute_value_as_str = attribute_value_as_str.join(self._convert_list_item_as_str(value) for value in attribute_value)
        self._redis.hset(
            self._get_aggregate_key(aggregate_root),
            attribute_key,
            attribute_value_as_str
        )

    def _convert_list_item_as_str(self, list_item):
        list_item_as_str = None
        if issubclass(list_item.__class__, AggregateRoot):
            list_item_as_str = list_item.get_id()
        else:
            list_item_as_str = str(list_item)
        return self._escape_spacial_characters_in_list_item(list_item_as_str)

    def _store_set_attribute(self, aggregate_root: AggregateRoot, attribute_key: str, attribute_value: set):
        # TODO : use list redis feature (lset)
        attribute_value_as_str = ';'
        attribute_value_as_str = attribute_value_as_str.join(self._convert_list_item_as_str(value) for value in attribute_value)
        self._redis.hset(
            self._get_aggregate_key(aggregate_root),
            attribute_key,
            attribute_value_as_str
        )

    def _escape_spacial_characters_in_list_item(self, list_item_as_str):
        return list_item_as_str.replace('\\', '\\\\').replace(';', '\;')

    def list_aggregates(self, the_class: type, pattern: str= '*'):
        """
        Returns a list of loaded aggregate roots, matching with a class and a identifier pattern
        :param the_class: the class of object that should be read from database. Must be a subclass of AggregateRoot
        :param pattern: the pattern that should match object ids
        :return: a list of aggregate roots, with data loaded
        """
        instances = []
        key_iterator = self._redis.keys(the_class.__name__ + ':' + pattern)
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
                    elif attribute_value.__class__ == int:
                        attribute_value = self._load_int_attribute_value(attribute_name, key)
                    elif attribute_value.__class__ == dict:
                        attribute_value = self._load_dict_attribute_value(attribute_name, key)
                    elif attribute_value.__class__ == bool:
                        attribute_value = self._load_bool_attribute_value(attribute_name, key)
                    elif attribute_value.__class__ == list:
                        attribute_value = self._load_list_attribute_value(attribute_name, key)
                    elif attribute_value.__class__ == set:
                        attribute_value = self._load_set_attribute_value(attribute_name, key)
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

    def _load_list_attribute_value(self, attribute_name, key):
        list_as_bytes = self._redis.hget(key, attribute_name)
        if list_as_bytes is None:
            return []
        list_as_str = list_as_bytes.decode()
        list_of_str = re.split('(?<!\\\\);', list_as_str)
        list_of_str_unescaped = []
        for item in list_of_str:
            unescaped_item = item.replace('\\;', ';').replace('\\\\', '\\')
            if unescaped_item.__len__() > 0:
                list_of_str_unescaped.append(unescaped_item)
        return list_of_str_unescaped

    def _load_set_attribute_value(self, attribute_name, key):
        set_as_bytes = self._redis.hget(key, attribute_name)
        if set_as_bytes is None:
            return set()
        set_as_str = set_as_bytes.decode()
        set_of_str = re.split('(?<!\\\\);', set_as_str)
        set_of_str_unescaped = set()
        for item in set_of_str:
            unescaped_item = item.replace('\\;', ';').replace('\\\\', '\\')
            if unescaped_item.__len__() > 0:
                set_of_str_unescaped.add(unescaped_item)
        return set_of_str_unescaped

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

    def get_aggregate(self, the_class: type, aggregate_id: str):
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
        while not key.decode().startswith(the_class.__name__ + ':'):
            key = self._redis.randomkey()
        aggregate_id = key.decode()[the_class.__name__.__len__() + 1:]
        return self.get_aggregate(the_class=the_class, aggregate_id=aggregate_id)

    def search_aggregate_keys_by_attribute_value(self, the_class: type, attribute_name: str, attribute_value: str):
        """
        Returns all the aggregates whose attribute matches with the value given as argument
        /!\ CAUTION : The index for the class and  attribute used must be up to date.
        :param the_class: the class or aggregates searched
        :param attribute_name: the name of the attribute
        :param attribute_value: the attribute's value that must be matched
        :return: a list of aggregates
        """
        keys = self._redis.lrange(the_class.__name__ + '#' + attribute_name + ':' + attribute_value.__str__(), 0, -1)
        keys_as_str = []
        for key in keys:
            keys_as_str.append(key.decode())
        return keys_as_str
