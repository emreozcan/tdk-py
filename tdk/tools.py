from typing import List, Iterator
from string import punctuation

from .alphabet import VOWELS, ALPHABET, CONSONANTS


def hecele(text: str) -> List[str]:
    """Syllabifies the specified text.

    >>> hecele("merhaba")
    ["mer", "ha", ba"]
    >>> hecele("ortaokul")
    ["or", "ta", "o", "kul"]
    """

    def next_vowel(text: str, cur: int) -> int:
        index = cur
        while True:
            if index + 1 >= len(text):
                return cur
            if text[index + 1] in VOWELS:
                return index + 1
            index += 1

    def are_there_letters_between(text, start, end, alphabet=ALPHABET):
        part = text[start + 1: end]
        for character in part:
            if character in alphabet:
                return True
        return False

    def previous_letter(text, end, stop_characters=f"{ALPHABET}{punctuation}"):
        index = end - 1
        while True:
            if text[index] in stop_characters:
                break
            index -= 1
            if index <= 0:
                break
        return index

    current_vowel_index = next_vowel(text, -1)
    syllables = []
    last_syllable_index = 0
    while True:
        next_vowel_index = next_vowel(text, current_vowel_index)
        if next_vowel_index == current_vowel_index:  # This is the last vowel
            syllables.append(text[last_syllable_index:])
            break
        elif (
                not are_there_letters_between(text, current_vowel_index,
                                              next_vowel_index)):  # There are two neighbor vowels (sa/at)
            syllable_stop_index = next_vowel_index
        else:
            syllable_stop_index = previous_letter(text, next_vowel_index)

        syllables.append(text[last_syllable_index:syllable_stop_index])
        last_syllable_index = syllable_stop_index

        current_vowel_index = next_vowel_index

    return syllables


def lowercase(word: str, alphabet: str = ALPHABET, remove_unknown_characters=True) -> str:
    """Removes all whitespace and punctuation from word and lowercase it.

    >>> lowercase("geçti Bor'un pazarı (sür eşeğini Niğde'ye)")
    "geçtiborunpazarısüreşeğininiğdeye"

    :return: A lowercase string without any whitespace or punctuation.
    """
    reconstructed_word = ""
    for letter in word:
        lower_letter = letter.lower()
        if letter == "I":
            reconstructed_word = f"{reconstructed_word}ı"
        elif letter == "İ":
            reconstructed_word = f"{reconstructed_word}i"
        elif letter in ["â", "Â"]:
            reconstructed_word = f"{reconstructed_word}a"
        elif letter in ["î", "Î"]:
            reconstructed_word = f"{reconstructed_word}i"
        elif letter in ["û", "Û"]:
            reconstructed_word = f"{reconstructed_word}u"
        elif lower_letter in alphabet or not remove_unknown_characters:
            reconstructed_word = f"{reconstructed_word}{lower_letter}"
    return reconstructed_word


def dictionary_order(word: str, alphabet=ALPHABET) -> list:
    """
    >>> dictionary_order("algarina") < dictionary_order("zamansızlık")
    True
    >>> dictionary_order("yumuşaklık") < dictionary_order("beşik")
    False
    """
    return list(map(alphabet.index, lowercase(word)))


def counter(word: str, targets=VOWELS) -> int:
    """
    >>> counter(word="aaaaaBBBc", targets="c")
    1
    >>> counter(word="aaaaaBBBc", targets="b")
    3
    >>> counter(word="aaaaaBBBc", targets="cb")
    4

    The word is sanitized using `lowercase()`.

    >>> counter(word="aaaaaBBBc", targets="B")
    0

    :return: The total number of occurrences of each element in targets.
    """
    safe_word = lowercase(word)
    return sum(safe_word.count(x) for x in targets)


def simplify(word: str, targets=VOWELS) -> Iterator[bool]:
    """Search each letter of a string in a list.

    >>> list(simplify("aaaaaBBBc", targets="a"))
    [True, True, True, True, True, False, False, False, False]
    >>> list(simplify("aaaaaBBBc", targets="ab"))
    [True, True, True, True, True, True, True, True, False]
    >>> list(simplify("aaaaaBBBc", targets="bc"))
    [False, False, False, False, False, True, True, True, True]

    The word is sanitized using `lowercase()`.

    >>> list(simplify(word="aaaaaBBBc", targets="B"))
    [False, False, False, False, False, False, False, False, False]

    :param word: The string to search through
    :param targets: List to check against
    """
    return map(lambda x: x in targets, lowercase(word))


def streaks(word: str, targets=CONSONANTS) -> List[int]:
    """
    Accumulate the number of characters in word which are also in targets.
    When a character in word isn't in targets, break the streak and append it to the return list.
    (Even if the current streak is 0.)

    >>> streaks("anapara")
    [0, 1, 1, 1, 0]  # /a N /a P /a R /a /
    >>> streaks("zorlanmak")
    [1, 2, 2, 1]     # Z /o RL /a NM /a K /
    >>> streaks("çözümlemek")
    [1, 1, 2, 1, 1]  # Ç /ö Z /ü ML /e M /e K /
    >>> streaks("tasdikletmek")
    [1, 2, 2, 2, 1]  # T /a SD /i KL /e TM /e K /
    """
    streaks_found = []
    accumulator = 0
    for letter in lowercase(word):
        if letter in targets:
            accumulator += 1
        else:
            streaks_found.append(accumulator)
            accumulator = 0
    else:
        streaks_found.append(accumulator)
    if len(streaks_found) == 0:
        return []
    return streaks_found


def max_streak(word: str, targets=CONSONANTS) -> int:
    """:return: The maximum combo of consecutive characters that are also in targets, in word."""
    return max(streaks(word=word, targets=targets))


def annotate(items, fn, sort_fn=None, reverse=True):
    """Return a dict with elements of items as keys and their values under fn as their values,
    sorted by their values under sort_fn. If sort_fn isn't specified, use fn by default.


    >>> annotate([4, 3, 2, 1], fn=lambda x: x**2, sort_fn=lambda x: (-2)**x, reverse=False)
    {3: 9, 1: 1, 2: 4, 4: 16}  # Sorted by odd numbers decreasing, then even numbers increasing.
    """
    if sort_fn is None:
        sort_fn = fn
    return {k: fn(k) for k in sorted(items, key=sort_fn, reverse=reverse)}


def distinct(seq) -> list:
    """Returns the sequence with each element appearing once without creating a set (and thus preserving order)."""
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
