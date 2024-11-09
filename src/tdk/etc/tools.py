from collections.abc import Sequence
from io import StringIO, SEEK_SET
from typing import TypeVar
from string import punctuation

from tdk.etc.alphabet import VOWELS, ALPHABET, CONSONANTS, LONG_VOWELS
from tdk.etc.enums import LetterType as _Ltr, SyllableType


def _next_vowel_index(text: str, cur: int) -> int:
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
    return any(character in alphabet for character in text[start + 1 : end])


ALPHABET_PUNCTUATION = f"{ALPHABET}{punctuation}"


def _previous_letter(text, end, stop_characters=ALPHABET_PUNCTUATION):
    index = end - 1
    while True:
        if text[index] in stop_characters:
            break
        index -= 1
        if index <= 0:
            break
    return index


def hecele(text: str, /) -> list[str]:
    """Split the text into syllables.

    >>> hecele("merhaba")
    ["mer", "ha", ba"]
    >>> hecele("ortaokul")
    ["or", "ta", "o", "kul"]
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


def get_syllable_type(syllable: str, /) -> SyllableType:
    """Determine the type of the syllable.

    The type of the syllable is defined as follows,
    where C is a consonant, V is a short vowel, and L is a long vowel:

    * If the syllable is of the form LC, CLC, VCC, CVCC, it is MEDLI.
    * If the syllable ends with a short vowel, it is OPEN.
    * Otherwise, it is CLOSED.

    :param syllable:
    :return:
    """
    letters = lowercase(syllable, remove_circumflexes=False)
    cv_map = tuple(get_letter_type(letter) for letter in letters)

    if cv_map in _MEDLI_PATTERNS:
        return SyllableType.MEDLI
    elif cv_map[-1] == _Ltr.SHORT_VOWEL:
        return SyllableType.OPEN
    else:
        return SyllableType.CLOSED


def get_letter_type(letter: str, /) -> _Ltr:
    ch = lowercase(letter, remove_circumflexes=False)
    if not ch:
        raise ValueError(f"Empty string is not a valid letter.")
    if ch in VOWELS:
        return _Ltr.SHORT_VOWEL
    elif ch in LONG_VOWELS:
        return _Ltr.LONG_VOWEL
    elif ch in CONSONANTS:
        return _Ltr.CONSONANT
    raise ValueError(f"Unknown letter {ch!r}")


def lowercase(
    word: str,
    /,
    *,
    alphabet: str = ALPHABET,
    keep_unknown_characters=False,
    remove_circumflexes=True,
) -> str:
    """Removes all whitespace and punctuation from word and lowercase it.

    >>> lowercase("geçti Bor'un pazarı (sür eşeğini Niğde'ye)")
    "geçtiborunpazarısüreşeğininiğdeye"

    :return: A lowercase string without any whitespace or punctuation.
    """

    a_circumflex_replacement = "a" if remove_circumflexes else "â"
    i_circumflex_replacement = "i" if remove_circumflexes else "î"
    u_circumflex_replacement = "u" if remove_circumflexes else "û"

    with StringIO() as word_io:
        for letter in word:
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
            elif lower_letter in alphabet or keep_unknown_characters:
                word_io.write(lower_letter)
        word_io.seek(0, SEEK_SET)
        return word_io.read()


def dictionary_order(word: str, /, *, alphabet=ALPHABET) -> tuple[int]:
    """
    >>> dictionary_order("algarina") < dictionary_order("zamansızlık")
    True
    >>> dictionary_order("yumuşaklık") < dictionary_order("beşik")
    False
    """
    return tuple(alphabet.index(letter) for letter in lowercase(word))


def counter(word: str, *, targets=VOWELS) -> int:
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
    word = lowercase(word)
    return sum(word.count(x) for x in targets)


def streaks(word: str, *, targets=CONSONANTS) -> list[int]:
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


def max_streak(word: str, *, targets=CONSONANTS) -> int:
    """The maximum consecutive targets in word."""
    return max(streaks(word=word, targets=targets))


T = TypeVar("T")


def distinct(seq: Sequence[T]) -> list[T]:
    """Returns the sequence with each element appearing once with order."""
    seen: set[T] = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
