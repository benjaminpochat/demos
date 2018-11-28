from src.main.python.model.agregate_root import AggregateRoot

import redis
import json


class RedisAccess:
    ''' Access data persisted in Redis
    #TODO : use hset instead of set redis command
    #TODO : check if the connexion should be closed properly
    '''

    def __init__(self, host: str = 'localhost', port: int = '6379', db: int = 0):
        self._redis = redis.Redis(host, port, db)

    def _get_agregate_key(self, agregate_root: AggregateRoot):
        return agregate_root.__class__.__name__ + ':' + agregate_root.get_id()

    def store_agregate(self, agregate_root: AggregateRoot):
        self._redis.set(self._get_agregate_key(agregate_root), json.dumps(agregate_root.__dict__))
