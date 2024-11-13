"""
Various tools for working with Turkish text.
"""

from collections.abc import Sequence
from io import StringIO, SEEK_SET
from typing import TypeVar
from string import punctuation

from tdk.alphabet import VOWELS, ALPHABET, CONSONANTS, LONG_VOWELS
from tdk.enums import LetterType as _Ltr, SyllableType

__all__ = [
    "hecele",
    "get_syllable_type",
    "get_letter_type",
    "lowercase",
    "dictionary_order",
    "counter",
    "streaks",
    "max_streak",
    "distinct",
]


def _next_vowel_index(text: str, cur: int) -> int:
    """Find the next vowel index in the text."""
    index = cur
    while True:
        if index + 1 >= len(text):
            return cur
        if text[index + 1] in f"{VOWELS}{LONG_VOWELS}":
            return index + 1
        index += 1


def _are_there_letters_between(
        text: str, start: int, end: int, alphabet=ALPHABET
) -> bool:
    """Check if there are any letters between the start and end indices."""
    return any(character in alphabet for character in text[start + 1: end])


def _previous_letter(text, end, stop_characters=f"{ALPHABET}{punctuation}"):
    """Find the previous letter index in text."""
    index = end - 1
    while True:
        if text[index] in stop_characters:
            break
        index -= 1
        if index <= 0:
            break
    return index


def hecele(text: str, /) -> list[str]:
    """Split text into syllables.

    ```pycon
    >>> hecele("merhaba")
    ["mer", "ha", ba"]
    >>> hecele("ortaokul")
    ["or", "ta", "o", "kul"]
    ```
    """

    current_vowel_index = _next_vowel_index(text, -1)
    syllables = []
    last_syllable_index = 0
    while True:
        next_vowel_index = _next_vowel_index(text, current_vowel_index)
        if next_vowel_index == current_vowel_index:  # This is the last vowel
            syllables.append(text[last_syllable_index:])
            break
        elif not _are_there_letters_between(
                text, current_vowel_index, next_vowel_index
        ):  # There are two neighbor vowels (sa/at)
            syllable_stop_index = next_vowel_index
        else:
            syllable_stop_index = _previous_letter(text, next_vowel_index)

        syllables.append(text[last_syllable_index:syllable_stop_index])
        last_syllable_index = syllable_stop_index

        current_vowel_index = next_vowel_index

    return syllables


_MEDLI_PATTERNS = (
    (_Ltr.LONG_VOWEL, _Ltr.CONSONANT),
    (_Ltr.CONSONANT, _Ltr.LONG_VOWEL, _Ltr.CONSONANT),
    (_Ltr.SHORT_VOWEL, _Ltr.CONSONANT, _Ltr.CONSONANT),
    (_Ltr.CONSONANT, _Ltr.SHORT_VOWEL, _Ltr.CONSONANT, _Ltr.CONSONANT),
)
"""Look-up table for medli syllable patterns.

Used by [](get_syllable_type) when determining if the syllable is medli.
"""


def get_syllable_type(syllable: str, /) -> SyllableType:
    """Determine the type of a syllable according to aruz prosody rules.

    The type of the syllable is defined as follows,
    where `C` is a consonant, `V` is a short vowel, and `L` is a long vowel:

    *   If the syllable is of the form `LC`, `CLC`, `VCC`, or `CVCC`; it is
        [](SyllableType.MEDLI).
    *   If the syllable ends with a short vowel, it is
        [](SyllableType.OPEN).
    *   Otherwise, it is [](SyllableType.CLOSED).
    """
    letters = lowercase(syllable, remove_hats=False)
    cv_map = tuple(get_letter_type(letter) for letter in letters)

    if cv_map in _MEDLI_PATTERNS:
        return SyllableType.MEDLI
    elif cv_map[-1] == _Ltr.SHORT_VOWEL:
        return SyllableType.OPEN
    else:
        return SyllableType.CLOSED


def get_letter_type(letter: str, /) -> _Ltr:
    """Determine the type of a letter.

    *   If the letter is a vowel without a circumflex, it is a
        [](LetterType.SHORT_VOWEL).
    *   If the letter is a vowel with a circumflex, it is a
        [](LetterType.LONG_VOWEL).
    *   If the letter is a consonant, it is a [](LetterType.CONSONANT).

    :raises ValueError: If the letter is not a valid letter in
                        [](VOWELS), [](LONG_VOWELS), or [](CONSONANTS).
    """
    ch = lowercase(letter, remove_hats=False)
    if not ch:
        raise ValueError("Empty string is not a valid letter.")
    if len(ch) != 1:
        raise ValueError(f"Expected a single character, got {len(ch)}.")
    if ch in VOWELS:
        return _Ltr.SHORT_VOWEL
    elif ch in LONG_VOWELS:
        return _Ltr.LONG_VOWEL
    elif ch in CONSONANTS:
        return _Ltr.CONSONANT
    raise ValueError(f"Unknown letter {ch!r}")


def lowercase(
        text: str,
        /,
        *,
        keep_nonletters: bool = False,
        remove_hats: bool = True,
) -> str:
    """Remove all whitespace and punctuation from text and lowercase it.

    :param text:
        The text to be lowercased.
    :param keep_nonletters:
        If a truthy value,
        characters that are not in the Turkish alphabet will be kept.
        This includes whitespace and punctuation.
        ```pycon
        >>> lowercase("geçti Bor'un pazarı (sür eşeğini Niğde'ye)",
        ...           keep_nonletters=False)  # The default
        "geçtiborunpazarısüreşeğininiğdeye"
        >>> lowercase("geçti Bor'un pazarı (sür eşeğini Niğde'ye)",
        ...           keep_nonletters=True)
        "geçti bor'un pazarı (sür eşeğini niğde'ye)"
        ```
    :param remove_hats:
        If a truthy value, characters with circumflexes will be replaced with
        their non-circumflexed counterparts.
        (e.g. "â" will be replaced with "a".)
        ```pycon
        >>> lowercase("İKAMETGÂH", remove_hats=True)
        "ikametgah"
        >>> lowercase("İKAMETGÂH", remove_hats=False)
        "ikametgâh"
        ```

    :returns: A lowercase string.
    """
    if remove_hats is None:
        remove_hats = not keep_nonletters

    a_circumflex_replacement = "a" if remove_hats else "â"
    i_circumflex_replacement = "i" if remove_hats else "î"
    u_circumflex_replacement = "u" if remove_hats else "û"

    with StringIO() as word_io:
        for letter in text:
            lower_letter = letter.lower()
            if letter == "I":
                word_io.write("ı")
            elif letter == "İ":
                word_io.write("i")
            elif letter in ["â", "Â"]:
                word_io.write(a_circumflex_replacement)
            elif letter in ["î", "Î"]:
                word_io.write(i_circumflex_replacement)
            elif letter in ["û", "Û"]:
                word_io.write(u_circumflex_replacement)
            elif lower_letter in ALPHABET or keep_nonletters:
                word_io.write(lower_letter)
        word_io.seek(0, SEEK_SET)
        return word_io.read()


def dictionary_order(word: str, /) \
        -> tuple[int, ...]:
    """Get a tuple of indices that can be used as orthographic order.

    :returns: A tuple of numbers suitable to be used as a dictionary order.

    ```python
    assert dictionary_order("algarina") < dictionary_order("zamansızlık")
    assert dictionary_order("yumuşaklık") > dictionary_order("beşik")
    ```

    :::{admonition} Invariant
    :class: tip

    If `B` comes after `A` in the dictionary,
    `dictionary_order(B) > dictionary_order(A)`.
    :::
    """
    return tuple(ALPHABET.index(letter) for letter in lowercase(word))


def counter(word: str, *, targets: str = VOWELS) -> int:
    """Find total number of occurrences of each element in targets.
    ```pycon
    >>> counter(word="aaaaaBBBc", targets="c")
    1
    >>> counter(word="aaaaaBBBc", targets="b")
    3
    >>> counter(word="aaaaaBBBc", targets="cb")
    4
    ```

    `word` is sanitized using `lowercase()`.

    ```pycon
    >>> counter(word="aaaaaBBBc", targets="B")
    0
    ```
    """
    word = lowercase(word)
    return sum(word.count(x) for x in targets)


def streaks(text: str, /, *, targets: str = CONSONANTS) -> list[int]:
    """Find streaks of consecutive targets in text

    ```pycon
    >>> streaks("anapara")
    [0, 1, 1, 1, 0]  # /a N /a P /a R /a /
    >>> streaks("zorlanmak")
    [1, 2, 2, 1]     # Z /o RL /a NM /a K /
    >>> streaks("çözümlemek")
    [1, 1, 2, 1, 1]  # Ç /ö Z /ü ML /e M /e K /
    >>> streaks("tasdikletmek")
    [1, 2, 2, 2, 1]  # T /a SD /i KL /e TM /e K /
    ```
    """
    streaks_found = []
    accumulator = 0
    for letter in lowercase(text):
        if letter in targets:
            accumulator += 1
        else:
            streaks_found.append(accumulator)
            accumulator = 0
    streaks_found.append(accumulator)
    if len(streaks_found) == 0:
        return []
    return streaks_found


def max_streak(word: str, *, targets: str = CONSONANTS) -> int:
    """Find the maximum consecutive targets in word."""
    return max(streaks(word, targets=targets))


_T = TypeVar("_T")


def distinct(seq: Sequence[_T]) -> Sequence[_T]:
    """
    Get a copy of the sequence with each element appearing once in input order.
    """
    seen: set[_T] = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
