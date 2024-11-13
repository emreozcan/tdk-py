"""Classes and functions to interact with TDK dictionaries.

This subpackage contains all the dictionaries available on the TDK website.
(Except {py:mod}`tdk.dictionaries.etj`, which is not fully released yet.)

Each dictionary is provided as a separate module
that contains objects necessary to interact with the relevant dictionary.

The dictionaries are:
```{autodoc2-summary}
:renderer: myst

tdk.dictionaries.ads
tdk.dictionaries.bati
tdk.dictionaries.bst
tdk.dictionaries.derleme
tdk.dictionaries.etj
tdk.dictionaries.etms
tdk.dictionaries.gts
tdk.dictionaries.kisi
tdk.dictionaries.lehce
tdk.dictionaries.sks
tdk.dictionaries.syyd
tdk.dictionaries.ts
tdk.dictionaries.yazim
tdk.dictionaries.ysk
```
"""

from . import (
    ads,
    bati,
    bst,
    derleme,
    etj,
    etms,
    gts,
    kisi,
    lehce,
    sks,
    syyd,
    ts,
    yazim,
    ysk,
)

from .ads import *
from .bati import *
from .bst import *
from .derleme import *
from .etj import *
from .etms import *
from .gts import *
from .kisi import *
from .lehce import *
from .sks import *
from .syyd import *
from .ts import *
from .yazim import *
from .ysk import *
