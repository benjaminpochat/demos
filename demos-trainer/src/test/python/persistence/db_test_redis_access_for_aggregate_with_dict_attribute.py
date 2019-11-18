import json
import unittest

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.aggregate_root import AggregateRoot
from src.test.python.persistence.db_test_redis_access_utils import AbstractTestRedisAccessForAggregate


class SimpleAggregateRootWithDictAttribute(AggregateRoot):
    """
    A simple AggregateRoot class with a dict attribute
    """

    def __init__(self,
                 id: str = '1',
                 dict_attribute: dict = {}):
        self.id = id
        self.dict_attribute = dict_attribute

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id


class TestRedisAccessForAggregateRootWithDictAttribute(AbstractTestRedisAccessForAggregate):
    """
    A unittest class to test RedisAccess with AggregateRoot class that has a attribute of type "dict"
    """

    def get_aggregate_root_class(self):
        return SimpleAggregateRootWithDictAttribute

    def test_store_simple_aggregate_root_with_empty_dict_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithDictAttribute()

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRootWithDictAttribute:1').__len__() == 1)
        self.assertEqual(self._redis.hget('SimpleAggregateRootWithDictAttribute:1', 'dict_attribute').decode(), '{}')

    def test_store_simple_aggregate_root_with_non_empty_dict_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithDictAttribute()
        aggregate_root.dict_attribute = {'field1': 1, 'field2': 'a'}

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRootWithDictAttribute:1').__len__() == 1)
        dict_value = json.loads(self._redis.hget('SimpleAggregateRootWithDictAttribute:1', 'dict_attribute').decode())
        self.assertEquals(dict_value['field1'], 1)
        self.assertEquals(dict_value['field2'], 'a')
        self.assertEquals(dict_value.__len__(), 2)

    def test_get_aggregate_should_load_aggregate_root_with_non_empty_dict_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithDictAttribute()
        aggregate_root.dict_attribute = {'field1': 1, 'field2': 'a'}
        redis_access.store_aggregate(aggregate_root)

        # when
        aggregate_root_read = redis_access.get_aggregate(SimpleAggregateRootWithDictAttribute, '1')

        # then
        self.assertEquals(aggregate_root_read.dict_attribute, {'field1': 1, 'field2': 'a'})

    def test_get_aggregate_should_load_aggregate_root_with_empty_dict_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithDictAttribute()
        aggregate_root.list_attribute = {}
        redis_access.store_aggregate(aggregate_root)

        # when
        aggregate_root_read = redis_access.get_aggregate(SimpleAggregateRootWithDictAttribute, '1')

        # then
        self.assertEquals(aggregate_root_read.dict_attribute, {})

    def test_list_simple_aggregate_root_should_load_data_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root_1 = SimpleAggregateRootWithDictAttribute(
            id='11',
            dict_attribute={'field1': 1, 'field2': 'a'})
        aggregate_root_2 = SimpleAggregateRootWithDictAttribute(
            id='12',
            dict_attribute={'fieldA': 1, 'fieldB': 2})
        redis_access.store_aggregate(aggregate_root_1)
        redis_access.store_aggregate(aggregate_root_2)

        # when
        aggregate_roots = redis_access.list_aggregates(SimpleAggregateRootWithDictAttribute, '1*')

        # then
        self.assertEquals(aggregate_roots.__len__(), 2)
        aggregate_root_1_found = False
        aggregate_root_2_found = False
        for aggregate_root in aggregate_roots:
            if aggregate_root.get_id() == '11':
                self.assertEquals(aggregate_root.dict_attribute, {'field1': 1, 'field2': 'a'})
                aggregate_root_1_found = True
            elif aggregate_root.get_id() == '12':
                self.assertEquals(aggregate_root.dict_attribute, {'fieldA': 1, 'fieldB': 2})
                aggregate_root_2_found = True
        self.assertTrue(aggregate_root_1_found and aggregate_root_2_found, 'some aggregate roots are missing')


if __name__ == '__main__':
    unittest.main()
