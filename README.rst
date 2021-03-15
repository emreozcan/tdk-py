tdk-py
######
Python API for the Turkish Language Foundation

tdk-py is a Python package that allows for simple access to `Turkish dictionaries`_ made available by the TDK_, the Turkish Language Society.
tdk-py aims to be easy to use and internally queries the TDK and parses its response into easy to use Python class objects.

.. _Turkish dictionaries: https://sozluk.gov.tr
.. _TDK: https://www.tdk.gov.tr

Sample usage
============
``tdk.gts`` is used to access TDK's GTS, the up-to-date Turkish dictionary (Güncel Türkçe Sözlük).

>>> import tdk.gts
>>> tdk.gts.search("merkeziyetçilik")
[<Entry 41635 (merkeziyetçilik)>]

``tsk.gts.search`` returns a list because it is possible for there to be more than one word with the exact same spelling.

>>> for number, entry in enumerate(tdk.gts.search("bar")):
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
>>> # 5 different words! One of them (#2) has multiple meanings!

You can query suggestions for misspelt words or for other similar words.

>>> tdk.gts.get_suggestions("feldispat")
['feldspat', 'felekiyat', 'ispat']
>>> tdk.gts.get_suggestions("feldspat")
['espas', 'felah', 'felaket', 'felekiyat', 'fellah', 'felsefe', 'felsefi']

You can perform complex analyses very easily.
Let's see the distribution of entries by the number of maximum consecutive consonants.

>>> from tdk.tools import max_streak
>>> from tdk.alphabet import CONSONANTS
>>> annotated_list = [max_streak(word=x, targets=CONSONANTS) for x in tdk.gts.get_index()]
>>> for i in set(annotated_list):
...     print(i, annotated_list.count(i))
...
0 19
1 15199
2 73511
3 3605
4 68
5 5

License
=======
tdk-py's source code is provided under the `MIT License`_.

Copyright © 2021 Emre Özcan

.. _MIT License: LICENSE
