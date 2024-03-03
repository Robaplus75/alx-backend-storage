#!/usr/bin/env python3
""" Cache Module """

import redis
import uuid
from typing import Union


class Cache:
    """ redis cache class """

    def __init__(self):
        """ INITIALIZATION """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data to redis """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get_str(self, key: str) -> str:
        '''for parametrizing Cache.get'''
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''for converting the data to the desired format'''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_int(self, key: str) -> int:
        '''for parametrizing Cache.get with correct conversion function'''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
