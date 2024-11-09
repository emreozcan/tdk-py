import asyncio
from functools import wraps
from typing import Annotated

from pydantic import BeforeValidator


def make_sync(func_to_be_cloned):
    def decorator(_unused_func):
        @wraps(func_to_be_cloned)
        def new_func(*args, **kwargs):
            return asyncio.run(func_to_be_cloned(*args, **kwargs))
        return new_func
    return decorator


def int_or_none_as_str(value: str) -> int | None:
    if not value:
        return None
    return int(value)


IntOrNone = Annotated[int | None, BeforeValidator(int_or_none_as_str)]


def str_or_none_as_str(value: str) -> str | None:
    if not value:
        return None
    return value


StrOrNone = Annotated[str | None, BeforeValidator(str_or_none_as_str)]
