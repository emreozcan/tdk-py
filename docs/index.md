# tdk-py

*Python API for the Turkish Language Foundation*

---

`tdk-py` is a Python package allowing access to
[Turkish dictionaries] of the [TDK], the Turkish Language Society.

`tdk-py` provides both synchronous and asynchronous interfaces to the TDK's
APIs and parses their responses into Python class objects based on Pydantic,
so you can do things like
[`.model_dump_json()`](<inv:#pydantic.BaseModel.model_dump_json>)
them, or use them in your API endpoints and generate beautiful schemas.

[Turkish dictionaries]: https://sozluk.gov.tr
[TDK]: https://www.tdk.gov.tr

## Installation

tdk-py is supported on Python 3.10+.

:::{tab} poetry
```bash
poetry add tdk-py
```
:::
:::{tab} pipenv
```bash
pipenv install tdk-py
```
:::
:::{tab} pip
```bash
pip install tdk-py
```
:::

```python
# in Python
import tdk
```

## Examples

`tdk.gts` is used to access TDK's GTS, the up-to-date Turkish dictionary
(Güncel Türkçe Sözlük).

### Searching

```python
import tdk
results = tdk.gts.search_sync("merkeziyetçilik")
print(results[0].meanings[0].meaning)
```
```{code-block}
:caption: Output

Otoritenin ve işin tek bir merkezde toplanmasını amaçlayan görüş; merkeziyet, merkezcilik
```

`tsk.gts.search` (and its `search_sync` counterpart) returns a list because it
is possible for there to be more than one word with the exact same spelling.

```python
import tdk
for number, entry in enumerate(tdk.gts.search_sync("bar")):
    for meaning in entry.meanings:
        print(number+1, entry.entry, meaning.meaning)
```
```{code-block}
:caption: Output

1 bar Anadolu'nun doğu ve kuzey bölgesinde, en çok Artvin ve Erzurum yörelerinde el ele tutuşularak oynanan, ağır ritimli bir halk oyunu
2 bar Danslı, içkili eğlence yeri
2 bar Ayaküstü içki içilen eğlence yeri
2 bar ► Amerikan bar
3 bar Hava basıncı birimi
4 bar Ateşten, mide bozukluğundan, ağızda, dil ve dişlerde meydana gelen acılık; pas
4 bar Sirke, pekmez gibi sıvıların üzerinde sonradan oluşan köpük veya küf
4 bar Su kaplarında su etkisiyle oluşan tortu veya kir
5 bar Halter sporunda ağırlığı oluşturan kiloları birbirine bağlayan metal çubuk
```

5 different words! One of them (#2) has multiple meanings!
z
### Generating suggestions

You can query suggestions for misspelt words or for other similar words.

```python
from difflib import get_close_matches
import tdk

# Calculate suggestions locally using the index:
suggestions = get_close_matches("feldispat", tdk.gts.get_index_sync())
# assert suggestions == ['feldspat', 'ispat', 'fesat']

# Use the TDK API: (sometimes errors out)
suggestions = tdk.gts.get_suggestions_sync("feldispat")
# assert suggestions == ['feldspat', 'felekiyat', 'ispat']
```

### Performing complex analyses

You can perform complex analyses very easily. Let's see the distribution
of entries by the number of maximum consecutive consonants.

```python
import tdk
annotated_dict = {}
for entry in tdk.gts.get_index_sync():
    streaks = tdk.etc.tools.max_streak(entry)
    if streaks not in annotated_dict:
        annotated_dict[streaks] = [entry]
    else:
        annotated_dict[streaks].append(entry)
for i in set(annotated_dict):
    print(i, len(annotated_dict[i]))
```
```{code-block}
:caption: Output

0 19
1 15199
2 73511
3 3605
4 68
5 5
```

```{toctree}
:maxdepth: 2
:caption: Contents:

apidocs/index.rst
```
