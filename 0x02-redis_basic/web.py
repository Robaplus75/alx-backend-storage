#!/usr/bin/env python3
"""
tarker for the webcache
"""
import redis
import requests
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """ counts number of times the url is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)

        store.expire(cached_key, 10)
        return html
    return wrapper

def project_info():
    ''' returns the projcet info '''
    return "Web file"


@count_url_access
def get_page(url: str) -> str:
    """ returns the html """
    res = requests.get(url)
    return res.text
