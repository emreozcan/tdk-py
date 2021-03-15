from tdk.tools import hecele, lowercase, dictionary_order, counter, simplify, streaks, annotate, distinct


class TestHecele:
    def test_basic(self):
        assert hecele("baceçıdi") == ["ba", "ce", "çı", "di"]

    def test_two_consecutive_vowels(self):
        assert hecele("baeç") == ["ba", "eç"]

    def test_two_consecutive_consonants(self):
        assert hecele("bacçe") == ["bac", "çe"]

    def test_three_consecutive_consonants(self):
        assert hecele("bacçde") == ["bacç", "de"]

    def test_two_consecutive_vowels_and_two_consecutive_consonants(self):
        assert hecele("baecçı") == ["ba", "ec", "çı"]
        assert hecele("bacçıe") == ["bac", "çı", "e"]
        assert hecele("abceı") == ["ab", "ce", "ı"]

    def test_correct_whitespace_and_punctuation_position(self):
        assert hecele("a, e") == ["a, ", "e"]
        assert hecele("a'bec") == ["a'", "bec"]

    def test_single_vowel_syllables(self):
        assert hecele("abceıçid") == ["ab", "ce", "ı", "çid"]

    def test_consecutive_single_vowel_syllables(self):
        assert hecele("aeıioöuü") == ["a", "e", "ı", "i", "o", "ö", "u", "ü"]

    def test_words_with_cvccccvc_pattern(self):
        assert hecele("bacçdfeg") == ["bacçd", "feg"]

    def test_words_with_cvcccvc_pattern(self):
        assert hecele("bacçdef") == ["bacç", "def"]

    def test_words_with_cvccvc_pattern(self):
        assert hecele("bacçed") == ["bac", "çed"]


class TestLowercase:
    def test_lowercasing(self):
        assert lowercase("ABCÇDEF") == "abcçdef"

    def test_romanization(self):
        assert lowercase("âîû") == "aiu"

    def test_romanization_and_lowercasing(self):
        assert lowercase("ÂÎÛ") == "aiu"

    def test_punctuation(self):
        assert lowercase("subh'u dem") == "subhudem"

    def test_circumflex_e_rejection(self):
        assert lowercase("ê") == ""
        assert lowercase("Ê") == ""

    def test_circumflex_o_rejection(self):
        assert lowercase("ô") == ""
        assert lowercase("Ô") == ""


def test_dictionary_order():
    assert dictionary_order("algarina") < dictionary_order("zamansızlık")
    assert dictionary_order("beşik") < dictionary_order("yumuşaklık")


class TestCounter:
    def test_basic(self):
        assert counter(word="abbccc", targets="a") == 1
        assert counter(word="abbccc", targets="b") == 2
        assert counter(word="abbccc", targets="c") == 3
        assert counter(word="abbccc", targets="ab") == 3
        assert counter(word="abbccc", targets="ac") == 4
        assert counter(word="abbccc", targets="bc") == 5
        assert counter(word="abbccc", targets="abc") == 6

    def test_lowercasing(self):
        assert counter(word="A", targets="a") == 1

    def test_not_lowercasing_targets(self):
        assert counter(word="a", targets="A") == 0


class TestSimplify:
    def test_type(self):
        assert type(simplify(word="", targets="")) is map

    def test_basic(self):
        assert list(simplify(word="abacç", targets="a")) == list(map(lambda x: x == 1, [1, 0, 1, 0, 0]))
        assert list(simplify(word="abacç", targets="b")) == list(map(lambda x: x == 1, [0, 1, 0, 0, 0]))
        assert list(simplify(word="abacç", targets="c")) == list(map(lambda x: x == 1, [0, 0, 0, 1, 0]))
        assert list(simplify(word="abacç", targets="ç")) == list(map(lambda x: x == 1, [0, 0, 0, 0, 1]))

    def test_lowercasing(self):
        assert list(simplify(word="ABacç", targets="a")) == list(map(lambda x: x == 1, [1, 0, 1, 0, 0]))

    def test_not_lowercasing_targets(self):
        assert list(simplify(word="ABacç", targets="A")) == [*[False] * 5]


class TestStreaks:
    def test_max_of_one(self):
        assert streaks("abecıçi") == [0, 1, 1, 1, 0]
        assert streaks("abecıç") == [0, 1, 1, 1]
        assert streaks("baceç") == [1, 1, 1]

    def test_max_of_two(self):
        assert streaks("bacçedfıg") == [1, 2, 2, 1]
        assert streaks("bacçedfıgi") == [1, 2, 2, 1, 0]
        assert streaks("abecçıdfigo") == [0, 1, 2, 2, 1, 0]

    def test_max_of_three(self):
        assert streaks("abecçıdfgiğhojö") == [0, 1, 2, 3, 2, 1, 0]
        assert streaks("bacçedfgığhijo") == [1, 2, 3, 2, 1, 0]
        assert streaks("bacçedfgığhij") == [1, 2, 3, 2, 1]

    def test_lone_letters(self):
        assert streaks("a") == [0, 0]
        assert streaks("ab") == [0, 1]
        assert streaks("ba") == [1, 0]

        assert streaks("ae") == [0, 0, 0]
        assert streaks("bae") == [1, 0, 0]
        assert streaks("abe") == [0, 1, 0]
        assert streaks("aeb") == [0, 0, 1]

        assert streaks("aeı") == [0, 0, 0, 0]
        assert streaks("baeı") == [1, 0, 0, 0]
        assert streaks("abeı") == [0, 1, 0, 0]
        assert streaks("aebı") == [0, 0, 1, 0]
        assert streaks("aeıb") == [0, 0, 0, 1]


def test_annotation():
    example_list = [1, 2, 3, 4]
    assert {1: 1, 2: 4, 3: 9, 4: 16} == annotate(example_list, fn=lambda x: x**2, reverse=False)


def test_dictinct():
    example_list = [1, 2, 3, 1, 4, 5, 6, 2, 7, 8, 9, 3, 10]
    assert [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] == distinct(example_list)
