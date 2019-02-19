import redis

from src.main.python.commons.loggable import Loggable
from src.main.python.commons.configuration import Configuration


class RedisIndexManager(Loggable):

    def __init__(self):
        super().__init__()
        configuration = Configuration()
        self._redis = redis.Redis(configuration.get_database_host(), configuration.get_database_port())

    def drop_index(self, the_class: type, attribute_name: str):
        for key in self._redis.keys(the_class.__name__ + '#' + attribute_name + ':*'):
            self._redis.delete(key)

    def create_index(self, the_class: type, attribute_name: str):
        for key in self._redis.keys(the_class.__name__ + ':*'):
            aggregate_id = key.decode()[the_class.__name__.__len__()+1:]
            attribute_value = self._redis.hget(key.decode(), attribute_name)
            if attribute_value is not None and attribute_value.decode().__len__() > 0 :
                self.log_debug('Adding the following value to the index ' + the_class.__name__ + '#' + attribute_name + ':' + attribute_value.decode() + ' : ' + aggregate_id)
                self._redis.rpush(the_class.__name__ + '#' + attribute_name + ':' + attribute_value.decode(), aggregate_id)
