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

The following subpackages and submodules are available as aliases in the
top-level package:

```{autodoc2-summary}
:renderer: myst

tdk.dictionaries
tdk.alphabet
tdk.enums
tdk.home
tdk.tools
```

The public APIs they expose are all also available as aliases in the top-level
package.
For example,

```python
import tdk
tdk.search_gts_sync("kedi")
tdk.dictionaries.search_gts_sync("kedi")
tdk.dictionaries.gts.search_gts_sync("kedi")
from tdk import dictionaries
dictionaries.search_gts_sync("kedi")
dictionaries.gts.search_gts_sync("kedi")
from tdk.dictionaries import gts
gts.search_gts_sync("kedi")
```

Function names have been designed not to conflict with each other when imported
to the namespace as star-imports expose all public APIs below their level:

```python
from tdk import *
search_gts_sync("kedi")  # [GTSEntry(...)]
search_spelling_sync("kedi")  # [SpellingEntry(...)]
```
"""

from . import (
    dictionaries,
    alphabet,
    enums,
    home,
    tools,
)
from .dictionaries import *
from .alphabet import *
from .enums import *
from .home import *
from .tools import *

__version__ = "0.0.0"
"""At runtime, holds the human-readable version of the installed version."""
__version_tuple__ = (0, 0, 0)
"""At runtime, holds the version of the installed package as a tuple of ints."""
