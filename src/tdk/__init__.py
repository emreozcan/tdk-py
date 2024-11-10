"""
`tdk` is the top-level package that forms the collection of modules that provide
access to various dictionaries from the Turkish Language Association (TDK)
and tools about the Turkish language.

Each submodule provides access to a different dictionary from the
Turkish Language Association (TDK).

If you do not care about niche dictionaries, you probably want the
{py:mod}`tdk.gts` module, which provides access to the
Güncel Türkçe Sözlük[^gts].

[^gts]: Updated Turkish Dictionary

Each function comes with a synchronous and an asynchronous version.
An async function `foo` has a synchronous counterpart `foo_sync`.
Each function can optionally take an `http_session` parameter to use
an existing [](<inv:#aiohttp.ClientSession>) for the HTTP requests.
If not provided, a new session is created and managed by the function using
[](<#session_maker>).
"""

__version__ = "0.0.0"
"""At runtime, holds the human-readable version of the installed version."""
__version_tuple__ = (0, 0, 0)
"""At runtime, holds the version of the installed package as a tuple of ints."""
