# tdk-py
Python API for the Turkish Language Foundation

tdk-py is a Python package that allows for simple access to [Turkish dictionaries](https://sozluk.gov.tr) made available by the [TDK](https://www.tdk.gov.tr), the Turkish Language Society.
tdk-py aims to be easy to use and internally queries the TDK and parses its response into easy to use Python class objects.

## Sample usage
`tdk.gts` is used to access TDK's GTS, the up-to-date Turkish dictionary (Güncel Türkçe Sözlük).
```python
>>> import tdk.gts
>>> list(tdk.gts.search("merkeziyetçilik"))
[<Entry 41635 (merkeziyetçilik)>]
```
tdk-py's querying functions return iterators. The query is made and its response is held in memory.
Then, its elements are parsed one-by-one when requested.
This makes sure that you don't wait for a long time to parse all search results at the start of a loop.
```python
>>> for number, entry in enumerate(tdk.gts.search("bar")):  # "bar" is searched, all responses are held in memory.
...     # They are parsed one by one.
...     for meaning in entry.meanings:
...         print(number+1, entry.entry, meaning.meaning)
...
1 bar Anadolu'nun doğu ve kuzey bölgesinde, en çok Artvin ve Erzurum yörelerinde el ele tutuşularak oynanan, ağır ritimli bir halk oyunu
2 bar Danslı, içkili eğlence yeri
2 bar Ayaküstü içki içilen eğlence yeri
2 bar Amerikan bar
3 bar Hava basıncı birimi
4 bar Ateşten, mide bozukluğundan, ağızda, dil ve dişlerde meydana gelen acılık, pas
5 bar Halter sporunda ağırlığı oluşturan kiloları birbirine bağlayan metal çubuk
```
You can query suggestions for misspelt words or for other similar words.
```python
>>> tdk.gts.get_suggestions("feldispat")
['feldspat', 'felekiyat', 'ispat']
>>> tdk.gts.get_suggestions("feldspat")
['espas', 'felah', 'felaket', 'felekiyat', 'fellah', 'felsefe', 'felsefi']
```
You can perform complex analyses very easily.
Let's see the distribution of entries by the number of maximum consecutive consonants.
```python
>>> from tdk.tools import max_streak
>>> from tdk.alphabet import CONSONANTS
>>> for i in range(6):
...     print(i, len(list(filter(lambda x: max_streak(word=x, targets=CONSONANTS)==i, tdk.gts.get_index()))))
0 19
1 15199
2 73511
3 3605
4 68
5 5
```

## License
tdk-py's source code is provided under the [MIT License](LICENSE).

Copyright ©, 2021, Emre Özcan
