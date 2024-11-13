# tdk-py

*Python API for the Turkish Language Foundation*

---

tdk-py is a Python package allowing access to
[Turkish dictionaries] of the [TDK], the Turkish Language Association.

tdk-py provides both synchronous and asynchronous interfaces to the TDK's
APIs and parses their responses into Python class objects based on
[](pydantic.BaseModel), so you can do things like
[`.model_dump_json()`](pydantic.BaseModel.model_dump_json)
them, or use them in your API endpoints and generate beautiful schemas.

[Turkish dictionaries]: https://sozluk.gov.tr
[TDK]: https://www.tdk.gov.tr

## Installation

tdk-py is supported on Python 3.10+.
First, make sure you have a Python environment set up.

:::{tab} poetry (recommended)
```bash
# in the shell
poetry add tdk-py
```
:::
:::{tab} pipenv
```bash
# in the shell
pipenv install tdk-py
```
:::
:::{tab} pip
```bash
# in the shell
pip install tdk-py
```
:::

```python
# in Python
import tdk
```

## Examples

[](tdk.dictionaries.gts) is used to access TDK's "GTS",
the up-to-date Turkish dictionary (Güncel Türkçe Sözlük).

Each function and class of its API is available as an alias in the namespace
of the top-level [](tdk) module.

### Searching

```python
import tdk

results = tdk.search_gts_sync("merkeziyetçilik")
print(results[0].meanings[0].meaning)
```
```{code-block}
:caption: Output

Otoritenin ve işin tek bir merkezde toplanmasını amaçlayan görüş; merkeziyet, merkezcilik
```

[](search_gts) (and its [](search_gts_sync) counterpart) returns a list because
it's possible for there to be more than one word with the exact same spelling.

```python
import tdk

for number, entry in enumerate(tdk.search_gts_sync("bar"), start=1):
    for meaning in entry.meanings:
        print(f"{entry.entry}({number}) {meaning.meaning}")
```
```{code-block}
:caption: Output

bar(1) Anadolu'nun doğu ve kuzey bölgesinde, en çok Artvin ve Erzurum yörelerinde el ele tutuşularak oynanan, ağır ritimli bir halk oyunu
bar(2) Danslı, içkili eğlence yeri
bar(2) Ayaküstü içki içilen eğlence yeri
bar(2) ► Amerikan bar
bar(3) Hava basıncı birimi
bar(4) Ateşten, mide bozukluğundan, ağızda, dil ve dişlerde meydana gelen acılık; pas
bar(4) Sirke, pekmez gibi sıvıların üzerinde sonradan oluşan köpük veya küf
bar(4) Su kaplarında su etkisiyle oluşan tortu veya kir
bar(5) Halter sporunda ağırlığı oluşturan kiloları birbirine bağlayan metal çubuk
```

5 different words! One of them (#2) has multiple meanings!

### Generating suggestions

You can query suggestions for misspelt words or for other similar words.

```python
from difflib import get_close_matches
import tdk

# Calculate suggestions locally using the index:
words = get_close_matches("feldispat", tdk.get_gts_index_sync())
assert words == ['feldspat', 'ispat', 'fesat']

# Use the TDK API: (sometimes errors out)
words = tdk.get_gts_suggestions_sync("feldispat")
assert words == ['feldspat', 'felekiyat', 'ispat']
```

### Performing complex analyses

You can perform complex analyses very easily. Let's see the distribution
of entries by the number of maximum consecutive consonants.

```python
import tdk

annotated_dict = {}
for entry in tdk.get_gts_index_sync():
    streaks = tdk.tools.max_streak(entry)
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
