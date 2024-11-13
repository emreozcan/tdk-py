"""
This module contains miscellaneous utilities for the library.
"""

from __future__ import annotations

import asyncio
from enum import Enum
from functools import wraps
from typing import Annotated, Any, Type

from pydantic import BeforeValidator, AfterValidator

from tdk.enums import MeaningProperty


def make_sync(func_to_be_cloned, /):
    """Make an async function run synchronously.

    Creates a decorator that runs the async function given as a parameter
    synchronously.

    :::{important}
    The wrapped function is discarded and not used.
    :::

    :::{admonition} Example usage
    :class: tip

    ```{code-block} python
    :emphasize-lines: 8,9

    from tdk.internal.utils import make_sync

    async def wait():
        from asyncio import sleep
        await sleep(1)
        return "Hello, world!"

    @make_sync(wait)
    def wait_sync(): ...

    print(wait_sync())  # Hello, world!
    ```
    """
    def decorator(_unused_func):
        @wraps(func_to_be_cloned)
        def new_func(*args, **kwargs):
            return asyncio.run(func_to_be_cloned(*args, **kwargs))

        return new_func

    return decorator


def int_or_none_as_str(value: str, /) -> int | None:
    """Convert a string to an [](int) or a [](None).

    Empty strings are converted to [](None),
    other strings are converted to type [](int).
    """
    if not value:
        return None
    return int(value)


IntOrNone = Annotated[int | None, BeforeValidator(int_or_none_as_str)]
"""[](pydantic.BeforeValidator) type hint for an integer or None.

Works using [](int_or_none_as_str).
"""


def str_or_none_as_str(value: str, /) -> str | None:
    """Convert a string to a [](str) or [](None).

    Empty strings are converted to [](None),
    other strings are converted to type [](str).
    """
    if not value:
        return None
    return value


StrOrNone = Annotated[str | None, BeforeValidator(str_or_none_as_str)]
"""[](pydantic.BeforeValidator) type hint for a string or None.

Works using [](str_or_none_as_str).
"""


def sound_url_validator(v: str, /) -> str:
    """Convert a sound code to a valid sound URL.

    Strings that do not start with `https://` are converted to
    `https://sozluk.gov.tr/ses/{}.wav`.
    """
    if not v.startswith("https://"):
        return f"https://sozluk.gov.tr/ses/{v}.wav"
    return v


SoundURL = Annotated[str, AfterValidator(sound_url_validator)]
"""[](pydantic.AfterValidator) type hint for a sound URL.

Works using [](sound_url_validator).
"""


def image_url_validator(v: str, /) -> str:
    """Convert an image code to a valid image URL.

    Strings that do not start with `https://` are converted to
    `https://sozluk.gov.tr/dosyalar/tarornek/{}.gif`.
    """
    if not v.startswith("https://"):
        return f"https://sozluk.gov.tr/dosyalar/tarornek/{v}.gif"
    return v


ImageURL = Annotated[str, AfterValidator(image_url_validator)]
"""[](pydantic.AfterValidator) type hint for an image URL.

Works using [](image_url_validator).
"""


def adapt_input_to_enum(input: Any, enum: Type[Enum]) -> Enum:
    """Get an enum member from an enum instance, value or name.

    ```pycon
    >>> from enum import Enum
    >>> class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    ...
    >>> adapt_input_to_enum(Color.RED, Color)
    <Color.RED: 1>
    >>> adapt_input_to_enum(2, Color)
    <Color.GREEN: 2>
    >>> adapt_input_to_enum("blue", Color)
    <Color.BLUE: 3>
    ```

    :raises ValueError: If `input` is not found in `enum`.
    """
    if isinstance(input, enum):
        return input
    for name, member in enum.__members__.items():
        if isinstance(input, str) and input.lower() == name.lower():
            return member
        if input == member.value:
            return member
    raise ValueError(f"Invalid input: {input!r}")


NOT_FOUND: dict = {"error": "Sonuç bulunamadı"}
"""The constant "not found" response of the API, decoded from JSON.

The TDK APIs always return this response when the requested data is not found.
"""


def assert_not_found(data: Any, /):
    """Assert that the data is a [](NOT_FOUND) response.

    :raises TypeError: If the data is not a dict.
    :raises ValueError: If the data is not a [](NOT_FOUND) response.
    """
    if not isinstance(data, dict):
        raise TypeError("Expected a dict")
    if data != NOT_FOUND:
        raise ValueError("Expected NOT_FOUND")


def validate_property(v: str | int | MeaningProperty, /):
    """Validate a meaning property.

    If the input is a [](MeaningProperty) instance, it is returned as is.
    Otherwise, [](MeaningProperty.get) is used to find the correct
    [](MeaningProperty) instance, and it is returned.
    """
    if isinstance(v, MeaningProperty):
        return v
    return MeaningProperty.get(v)


ValidatedProperty = Annotated[
    MeaningProperty,
    BeforeValidator(validate_property)
]
"""[](pydantic.BeforeValidator) type hint for a validated meaning property.

Works using [](validate_property).
"""
