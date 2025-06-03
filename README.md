# tdk-py

*Python API for the Turkish Language Foundation*

[![Latest version on PyPI](https://img.shields.io/pypi/v/tdk-py)](https://pypi.org/project/tdk-py/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/tdk-py)](https://pypi.org/project/tdk-py/)

[![Codacy Grade Badge](https://app.codacy.com/project/badge/Grade/5d4a5bd343274970b04ab86e05be1b29)](https://app.codacy.com/gh/EmreOzcan/tdk-py/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Coverage Badge](https://app.codacy.com/project/badge/Coverage/5d4a5bd343274970b04ab86e05be1b29)](https://app.codacy.com/gh/EmreOzcan/tdk-py/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![checks/master](https://img.shields.io/github/check-runs/emreozcan/tdk-py/master?logo=github&label=checks%2Fmaster)](https://github.com/emreozcan/tdk-py/actions/workflows/test.yml)
[![docs](https://readthedocs.org/projects/tdk-py/badge/?version=latest)](https://tdk-py.readthedocs.io/en/latest/?badge=latest)

---

tdk-py is a Python package allowing access to
[Turkish dictionaries] of the [TDK], the Turkish Language Association.

tdk-py provides both synchronous and asynchronous interfaces to the TDK's
APIs and parses their responses into Python class objects based on Pydantic,
so you can do things like
[`.model_dump_json()`][model_dump_json]
them, or use them in your API endpoints and generate beautiful schemas.

[Turkish dictionaries]: https://sozluk.gov.tr
[TDK]: https://www.tdk.gov.tr
[model_dump_json]: https://docs.pydantic.dev/2.9/api/base_model/#pydantic.BaseModel.model_dump_json

## Quick start

tdk-py is supported on Python 3.10+.
First, make sure you have a Python environment set up.

```bash
# in the shell
poetry add tdk-py      # if using python-poetry.org (recommended)
pipenv install tdk-py  # if using pipenv.pypa.io
pip install tdk-py     # straight pip.pypa.io
```

```python
# in Python
import tdk
```

## Examples

```python
import tdk

results = tdk.search_gts_sync("merkeziyetçilik")
print(results[0].meanings[0].meaning)
```
```{code-block}
Otoritenin ve işin tek bir merkezde toplanmasını amaçlayan görüş; merkeziyet, merkezcilik
```

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
0 19
1 15199
2 73511
3 3605
4 68
5 5
```

## License

tdk-py's source code is provided under the [MIT License]

[MIT License]: https://github.com/EmreOzcan/tdk-py/blob/master/LICENSE

Copyright © 2021-2025 Emre Özcan
