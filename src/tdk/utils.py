import asyncio
from functools import wraps


def make_sync(func_to_be_cloned):
    def decorator(_unused_func):
        @wraps(func_to_be_cloned)
        def new_func(*args, **kwargs):
            return asyncio.run(func_to_be_cloned(*args, **kwargs))
        return new_func
    return decorator
