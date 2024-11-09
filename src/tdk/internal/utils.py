import asyncio
from enum import Enum
from functools import wraps
from typing import Annotated, Any, Type

from pydantic import BeforeValidator, AfterValidator


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


def sound_url_validator(v: str) -> str:
    if not v.startswith("https://"):
        return f"https://sozluk.gov.tr/ses/{v}.wav"
    return v


SoundURL = Annotated[str, AfterValidator(sound_url_validator)]


def adapt_input_to_enum(input: Any, enum: Type[Enum]) -> Enum:
    if isinstance(input, enum):
        return input
    for name, member in enum.__members__.items():
        if isinstance(input, str) and input.lower() == name.lower():
            return member
        if input == member.value:
            return member
    raise ValueError(f"Invalid input: {input!r}")


NOT_FOUND = {"error": "Sonuç bulunamadı"}


def assert_not_found(data: Any):
    if not isinstance(data, dict):
        raise TypeError("Expected a dict")
    if data != NOT_FOUND:
        raise ValueError("Expected NOT_FOUND")


def image_url_validator(v: str) -> str:
    if not v.startswith("https://"):
        return f"https://sozluk.gov.tr/dosyalar/tarornek/{v}.gif"
    return v


ImageURL = Annotated[str, AfterValidator(image_url_validator)]
