from typing import List
from string import punctuation

from alphabet import VOWELS, ALPHABET, CONSONANTS


def hecele(text):
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
            _returnUntil = next_vowel_index
        else:
            _returnUntil = previous_letter(text, next_vowel_index)

        syllables.append(text[last_syllable_index:_returnUntil])
        last_syllable_index = _returnUntil

        current_vowel_index = next_vowel_index

    return syllables


def next_vowel(text, cur):
    index = cur
    while True:
        if index + 1 >= len(text):
            return cur
        if is_vowel(text[index + 1]):
            return index + 1
        index += 1


def is_vowel(letter, vowels=VOWELS):
    return letter in vowels


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


def lowercase(word: str, alphabet=ALPHABET) -> str:
    reconstructed_word = ""
    for letter in word:
        if letter == "I":
            reconstructed_word = f"{reconstructed_word}ı"
        elif letter == "İ":
            reconstructed_word = f"{reconstructed_word}i"
        elif letter in ["â", "Â"]:
            reconstructed_word = f"{reconstructed_word}a"
        elif letter in ["î", "Î"]:
            reconstructed_word = f"{reconstructed_word}ı"
        elif letter in ["û", "Û"]:
            reconstructed_word = f"{reconstructed_word}u"
        elif (lower_letter := letter.lower()) in alphabet:
            reconstructed_word = f"{reconstructed_word}{lower_letter}"
    return reconstructed_word


def alphabetic_radix(word: str, alphabet=ALPHABET, alphabet_length=29) -> float:
    if alphabet_length is None:
        alphabet_length = len(alphabet)
    return sum(
        map(
            lambda x: alphabet_length ** -x[0] * (alphabet.index(x[1]) + 1),
            enumerate(lowercase(word))
        )
    )


def counter(word: str, targets=VOWELS) -> int:
    safe_word = lowercase(word)
    return sum(safe_word.count(x) for x in targets)


def simplify(word: str, targets=VOWELS):
    safe_word = lowercase(word)
    return map(lambda x: x in targets, safe_word)


def streaks(word: str, targets=CONSONANTS) -> List[int]:
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


def streak(word: str, targets=CONSONANTS) -> int:
    return max(streaks(word=word, targets=targets))


def annotate(items, fn, reverse=True):
    return {k: fn(k) for k in sorted(items, key=fn, reverse=reverse)}
