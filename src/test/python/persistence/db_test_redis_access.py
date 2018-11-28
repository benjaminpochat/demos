import unittest
import json
from src.main.python.persistence.redis_access import RedisAccess
from src.main.python.model.agregate_root import AggregateRoot


class SimpleAgregateRoot(AggregateRoot):
    def __init__(self):
        self._message = 'Message in a bottle'

    def get_id(self):
        return '1'


class TestRedisAccess(unittest.TestCase):
    def test_store_simple_agregate_root_should_run_without_error(self):
        #given

        redis_access = RedisAccess()
        agregate_root = SimpleAgregateRoot()

        #when
        redis_access.store_agregate(agregate_root)

        #then


if __name__ == '__main__':
    unittest.main()
