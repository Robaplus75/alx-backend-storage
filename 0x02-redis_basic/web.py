#!/usr/bin/env python3
""" Redis Module """

import redis
import requests
from functools import wraps
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ counts requestts """
    @wraps(method)
    def wrapper(url):
        """ wrapper func """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")

        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)

        redis_.psetex(f"cached:{url}", 10000, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ gets html content """
    req = requests.get(url)
    return req.text
