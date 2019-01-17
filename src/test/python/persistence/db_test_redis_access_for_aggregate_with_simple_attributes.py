import json
import unittest

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.aggregate_root import AggregateRoot
from src.main.python.commons.boolean_enum import Boolean

from src.test.python.persistence.db_test_redis_access_utils import AbstractTestRedisAccessForAggregate, VerySimpleAggregateRoot


class SimpleAggregateRoot(AggregateRoot):

    def __init__(self,
                 id: str = '1',
                 str_attribute: str = 'Message in a bottle',
                 int_attribute: int = 1,
                 bool_attribute: bool = False,
                 enum_attribute: Boolean = Boolean.TRUE,
                 aggregate_root_attribute: VerySimpleAggregateRoot = VerySimpleAggregateRoot()):
        self.id = id
        self.str_attribute = str_attribute
        self.int_attribute = int_attribute
        self.bool_attribute = bool_attribute
        self.enum_attribute = enum_attribute
        self.none_attribute = None
        self.aggregate_root_attribute = aggregate_root_attribute

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id


class TestRedisAccessForAggregateRootWithSimpleAttributes(AbstractTestRedisAccessForAggregate):

    def get_aggregate_root_class(self):
        return SimpleAggregateRoot

    def test_store_simple_aggregate_root_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRoot()
        aggregate_root.aggregate_root_attribute = VerySimpleAggregateRoot('1')

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRoot:1').__len__() == 1)
        self.assertEquals(self._redis.hget('SimpleAggregateRoot:1', 'str_attribute').decode(), 'Message in a bottle')
        self.assertEquals(int(self._redis.hget('SimpleAggregateRoot:1', 'int_attribute').decode()), 1)
        self.assertEquals(self._redis.hget('SimpleAggregateRoot:1', 'bool_attribute').decode(), 'False')
        self.assertEquals(self._redis.hget('SimpleAggregateRoot:1', 'enum_attribute').decode(), 'Boolean.TRUE')

    def test_get_aggregate_should_load_data_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root_1 = SimpleAggregateRoot(aggregate_root_attribute=VerySimpleAggregateRoot('1'))
        redis_access.store_aggregate(aggregate_root_1)

        # when
        aggregate_root = redis_access.get_aggregate(SimpleAggregateRoot, '1')

        # then
        self._check_simple_aggregate_root(aggregate_root,
                                          expected_str='Message in a bottle',
                                          expected_int=1,
                                          expected_bool=False,
                                          expected_enum=Boolean.TRUE,
                                          expected_aggregate_root=VerySimpleAggregateRoot('1'))

    def test_get_random_aggregate_should_return_data_loaded(self):
        # given
        redis_access = RedisAccess()
        aggregate_root_1 = SimpleAggregateRoot(id='11')
        aggregate_root_2 = SimpleAggregateRoot(id='12')
        redis_access.store_aggregate(aggregate_root_1)
        redis_access.store_aggregate(aggregate_root_2)

        # when
        aggregate_root = redis_access.get_random_aggregate(SimpleAggregateRoot)

        # then
        self.assertTrue(aggregate_root.str_attribute is not None)
        self.assertTrue(aggregate_root.int_attribute is not None)
        self.assertTrue(aggregate_root.bool_attribute is not None)
        self.assertTrue(aggregate_root.enum_attribute is not None)

    def test_list_simple_aggregate_root_should_load_data_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root_1 = SimpleAggregateRoot(id='11',
                                               aggregate_root_attribute=VerySimpleAggregateRoot('1'))
        aggregate_root_2 = SimpleAggregateRoot(id='12',
                                               str_attribute='We all live on a Yellow submarine',
                                               int_attribute=314,
                                               bool_attribute=True,
                                               enum_attribute=Boolean.UNKNOWN,
                                               aggregate_root_attribute=VerySimpleAggregateRoot('2'))
        redis_access.store_aggregate(aggregate_root_1)
        redis_access.store_aggregate(aggregate_root_2)

        # when
        aggregate_roots = redis_access.list_aggregates(SimpleAggregateRoot, '1*')

        # then
        self.assertEquals(aggregate_roots.__len__(), 2)
        aggregate_root_1_found = False
        aggregate_root_2_found = False
        for aggregate_root in aggregate_roots:
            if aggregate_root.get_id() == '11':
                self._check_simple_aggregate_root(aggregate_root,
                                                  expected_str='Message in a bottle',
                                                  expected_int=1,
                                                  expected_bool=False,
                                                  expected_enum=Boolean.TRUE,
                                                  expected_aggregate_root=VerySimpleAggregateRoot(id='1'))
                aggregate_root_1_found = True
            elif aggregate_root.get_id() == '12':
                self._check_simple_aggregate_root(aggregate_root,
                                                  expected_str='We all live on a Yellow submarine',
                                                  expected_int=314,
                                                  expected_bool=True,
                                                  expected_enum=Boolean.UNKNOWN,
                                                  expected_aggregate_root=VerySimpleAggregateRoot(id='2'))
                aggregate_root_2_found = True
        self.assertTrue(aggregate_root_1_found and aggregate_root_2_found, 'some aggregate roots are missing')

    def _check_simple_aggregate_root(self,
                                     aggregate_root,
                                     expected_str: str,
                                     expected_int: int,
                                     expected_bool: bool,
                                     expected_enum: Boolean,
                                     expected_aggregate_root: AggregateRoot):
        self.assertEquals(aggregate_root.str_attribute, expected_str)
        self.assertEquals(aggregate_root.int_attribute, expected_int)
        self.assertEquals(aggregate_root.bool_attribute, expected_bool)
        self.assertEquals(aggregate_root.enum_attribute, expected_enum)
        self.assertEquals(aggregate_root.none_attribute, None)
        self.assertEquals(aggregate_root.aggregate_root_attribute.get_id(), expected_aggregate_root.get_id())


if __name__ == '__main__':
    unittest.main()
