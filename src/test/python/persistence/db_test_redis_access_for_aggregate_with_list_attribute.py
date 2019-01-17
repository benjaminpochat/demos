import unittest

from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.aggregate_root import AggregateRoot
from src.test.python.persistence.db_test_redis_access_utils import VerySimpleAggregateRoot, AbstractTestRedisAccessForAggregate


class SimpleAggregateRootWithListAttribute(AggregateRoot):
    """
    A simple AggregateRoot class with a list attribute
    """

    def __init__(self,
                 id: str = '1',
                 list_attribute: list = []):
        self.id = id
        self.list_attribute = list_attribute

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id


class TestRedisAccessForAggregateRootWithListAttribute(AbstractTestRedisAccessForAggregate):
    """
    A unittest class to test RedisAccess with AggregateRoot class that has a attribute of type "list"
    """

    def get_aggregate_root_class(self):
        return SimpleAggregateRootWithListAttribute

    def test_store_simple_aggregate_root_with_empty_list_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithListAttribute()

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRootWithListAttribute:1').__len__() == 1)
        self.assertEqual(self._redis.hget('SimpleAggregateRootWithListAttribute:1', 'list_attribute').decode(), '')

    def test_store_simple_aggregate_root_with_non_empty_list_should_be_saved_correctly(self):
        #given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithListAttribute()
        aggregate_root.list_attribute = ['one', 'two;three', 'fo\\ur']

        # when
        redis_access.store_aggregate(aggregate_root)

        # then
        self.assertTrue(self._redis.keys('SimpleAggregateRootWithListAttribute:1').__len__() == 1)
        self.assertEquals(self._redis.hget('SimpleAggregateRootWithListAttribute:1', 'list_attribute').decode(),
                          'one;two\\;three;fo\\\\ur')


    def test_get_aggregate_should_load_aggregate_root_with_non_empty_list_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithListAttribute()
        aggregate_root.list_attribute = ['one', 'two;three', 'fo\\ur']
        redis_access.store_aggregate(aggregate_root)

        # when
        aggregate_root_read = redis_access.get_aggregate(SimpleAggregateRootWithListAttribute, '1')

        # then
        self.assertEquals(aggregate_root_read.list_attribute, ['one', 'two;three', 'fo\\ur'])

    def test_get_aggregate_should_load_aggregate_root_with_empty_set_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root = SimpleAggregateRootWithListAttribute()
        aggregate_root.list_attribute = []
        redis_access.store_aggregate(aggregate_root)

        # when
        aggregate_root_read = redis_access.get_aggregate(SimpleAggregateRootWithListAttribute, '1')

        # then
        self.assertEquals(aggregate_root_read.list_attribute, [])

    def test_list_simple_aggregate_root_should_load_data_correctly(self):
        # given
        redis_access = RedisAccess()
        aggregate_root_1 = SimpleAggregateRootWithListAttribute(
            id='11',
            list_attribute=['one', 'two;three', 'fo\\ur'])
        aggregate_root_2 = SimpleAggregateRootWithListAttribute(
            id='12',
            list_attribute=[VerySimpleAggregateRoot(id='AZERTY'), VerySimpleAggregateRoot(id='QWERTY')])
        redis_access.store_aggregate(aggregate_root_1)
        redis_access.store_aggregate(aggregate_root_2)

        # when
        aggregate_roots = redis_access.list_aggregates(SimpleAggregateRootWithListAttribute, '1*')

        # then
        self.assertEquals(aggregate_roots.__len__(), 2)
        aggregate_root_1_found = False
        aggregate_root_2_found = False
        for aggregate_root in aggregate_roots:
            if aggregate_root.get_id() == '11':
                self.assertEquals(aggregate_root.list_attribute, ['one', 'two;three', 'fo\\ur'])
                aggregate_root_1_found = True
            elif aggregate_root.get_id() == '12':
                self.assertEquals(aggregate_root.list_attribute, ['AZERTY', 'QWERTY'])
                aggregate_root_2_found = True
        self.assertTrue(aggregate_root_1_found and aggregate_root_2_found, 'some aggregate roots are missing')


if __name__ == '__main__':
    unittest.main()
