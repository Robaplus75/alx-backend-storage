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
