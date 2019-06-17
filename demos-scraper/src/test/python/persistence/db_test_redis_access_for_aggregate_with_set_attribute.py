import unittest

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.aggregate_root import AggregateRoot
from src.test.python.persistence.db_test_redis_access_utils import AbstractTestRedisAccessForAggregate


class SimpleAggregateRootWithSetAttribute(AggregateRoot):

    def __init__(self,
                 id: str = '1',
                 set_attribute: set = set()):
        self.id = id
        self.set_attribute = set_attribute

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id


class TestRedisAccessForAggregateRootWithSetAttribute(AbstractTestRedisAccessForAggregate):
    def get_aggregate_root_class(self):
        return SimpleAggregateRootWithSetAttribute

    def test_store_simple_aggregate_root_with_empty_set_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithSetAttribute()

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRootWithSetAttribute:1').__len__() == 1)
        self.assertEqual(self._redis.hget('SimpleAggregateRootWithSetAttribute:1', 'set_attribute').decode(), '')

    def test_store_simple_aggregate_root_with_non_empty_set_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithSetAttribute()
        aggregate_root.set_attribute = {'1', 'A'}

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRootWithSetAttribute:1').__len__() == 1)
        self.assertTrue(self._redis.hget('SimpleAggregateRootWithSetAttribute:1', 'set_attribute').decode().split(';').__len__() == 2)
        self.assertTrue(self._redis.hget('SimpleAggregateRootWithSetAttribute:1', 'set_attribute').decode().split(';').__contains__('1'))
        self.assertTrue(self._redis.hget('SimpleAggregateRootWithSetAttribute:1', 'set_attribute').decode().split(';').__contains__('A'))


    def test_get_aggregate_should_load_aggregate_root_with_non_empty_set_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithSetAttribute()
        aggregate_root.set_attribute = {'1', 'A'}
        redis_access.store_aggregate(aggregate_root)

        # when
        aggregate_root_read = redis_access.get_aggregate(SimpleAggregateRootWithSetAttribute, '1')

        # then
        self.assertEquals(aggregate_root_read.set_attribute, {'1', 'A'})

    def test_get_aggregate_should_load_aggregate_root_with_empty_set_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithSetAttribute(set_attribute=set())
        redis_access.store_aggregate(aggregate_root)

        # when
        aggregate_root_read = redis_access.get_aggregate(SimpleAggregateRootWithSetAttribute, '1')

        # then
        self.assertEquals(aggregate_root_read.set_attribute, set())

    def test_list_simple_aggregate_root_should_load_data_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root_1 = SimpleAggregateRootWithSetAttribute(
            id='11',
            set_attribute={'KLJH', 'VGHJV'})
        aggregate_root_2 = SimpleAggregateRootWithSetAttribute(
            id='12',
            set_attribute={'9876897', '5856023'})
        redis_access.store_aggregate(aggregate_root_1)
        redis_access.store_aggregate(aggregate_root_2)

        # when
        aggregate_roots = redis_access.list_aggregates(SimpleAggregateRootWithSetAttribute, '1*')

        # then
        self.assertEquals(aggregate_roots.__len__(), 2)
        aggregate_root_1_found = False
        aggregate_root_2_found = False
        for aggregate_root in aggregate_roots:
            if aggregate_root.get_id() == '11':
                self.assertEquals(aggregate_root.set_attribute, {'KLJH', 'VGHJV'})
                aggregate_root_1_found = True
            elif aggregate_root.get_id() == '12':
                self.assertEquals(aggregate_root.set_attribute, {'9876897', '5856023'})
                aggregate_root_2_found = True
        self.assertTrue(aggregate_root_1_found and aggregate_root_2_found, 'some aggregate roots are missing')


if __name__ == '__main__':
    unittest.main()
