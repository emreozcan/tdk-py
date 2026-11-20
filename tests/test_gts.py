from tdk.dictionaries.gts import GTSEntry, _normalize_query

NEW_STYLE_ENTRY = {
    "kac": 0,
    "madde": "örnek",
    "madde_id": 1,
    "lisan": None,
    "lisanKoken": None,
    "lisanKodu": 0,
    "telaffuz": None,
    "heceleme": "ör-nek",
    "fonemik": None,
    "taki": None,
    "cogulMu": False,
    "ozelMi": False,
    "egikMi": False,
    "seskod": "o1",
    "anlamlarListe": [
        {
            "anlam_id": 10,
            "anlam": "Örnek tanım cümlesi.",
            "orneklerListe": [
                {
                    "ornek_id": 100,
                    "ornek": None,
                    "yazar": [
                        {
                            "yazar_id": 5,
                            "tam_adi": "Örnek Yazar",
                            "kisa_adi": "Ö. Yazar",
                        }
                    ],
                }
            ],
            "ozelliklerListe": [
                {
                    "ozellik_id": 19,
                    "tur": 3,
                    "tam_adi": "isim",
                    "kisa_adi": "a.",
                    "ekno": 30,
                }
            ],
            "sozcukTuru": "fiil",
            "anlamEsAnlam": [
                {
                    "anlam_id": 10,
                    "sira": 1,
                    "deger": "örnek eş anlamlı",
                    "hedef_madde_id": 2,
                }
            ],
            "anlamKarsitAnlam": [],
            "anlamReferans": [],
        }
    ],
    "anlamGruplari": [
        {
            "tur": "fiil",
            "anlamlar": [
                {
                    "anlam_id": 10,
                    "anlam": "Örnek tanım cümlesi.",
                    "orneklerListe": [],
                    "ozelliklerListe": [],
                    "sozcukTuru": "fiil",
                    "anlamEsAnlam": [],
                    "anlamKarsitAnlam": [],
                    "anlamReferans": [],
                }
            ],
        }
    ],
    "birlesikKelimeler": [{"madde_id": 3, "madde": "örnek birleşik"}],
    "atasozleri": [{"madde_id": 4, "madde": "örnek atasözü"}],
}


OLD_STYLE_ENTRY = {
    "madde_id": "1",
    "kac": "0",
    "madde": "örnek",
    "cogul_mu": "0",
    "ozel_mi": "0",
    "lisan_kodu": "11",
    "lisan": "\\11 örnek",
    "madde_duz": "örnek",
    "telaffuz": "örnek",
    "taki": "ğü",
    "birlesikler": "örnek birleşik, örnek tamlama",
    "anlamlarListe": [
        {
            "anlam_id": "10",
            "anlam": "Örnek tanım cümlesi.",
            "anlam_sira": "1",
            "fiil": "0",
            "madde_id": "1",
            "orneklerListe": [
                {
                    "ornek_id": "100",
                    "anlam_id": "10",
                    "ornek_sira": "1",
                    "ornek": "Örnek kullanım cümlesi.",
                    "yazar": [
                        {
                            "yazar_id": "5",
                            "tam_adi": "Örnek Yazar",
                            "kisa_adi": "Ö. Yazar",
                        }
                    ],
                }
            ],
            "ozelliklerListe": [],
        }
    ],
    "atasozu": [{"madde_id": "4", "madde": "örnek atasözü"}],
}


def test_new_style_entry():
    entry = GTSEntry.model_validate(NEW_STYLE_ENTRY)

    assert entry.entry == "örnek"
    assert entry.syllabification == "ör-nek"
    assert entry.sound_code == "o1"
    assert entry.compound_words[0].entry == "örnek birleşik"
    assert entry.proverbs[0].proverb == "örnek atasözü"

    meaning = entry.meanings[0]
    assert meaning.meaning == "Örnek tanım cümlesi."
    assert meaning.word_type == "fiil"
    assert meaning.is_verb
    assert meaning.order == 1
    assert meaning.entry_id == entry.tdk_id
    assert meaning.examples[0].example is None
    assert meaning.examples[0].meaning_id == meaning.tdk_id
    assert meaning.examples[0].order == 1
    assert meaning.synonyms[0].entry == "örnek eş anlamlı"


def test_old_style_entry():
    entry = GTSEntry.model_validate(OLD_STYLE_ENTRY)

    assert entry.entry == "örnek"
    assert entry.original == "\\11 örnek"
    assert entry.entry_normalized == "örnek"
    assert entry.meanings[0].order == 1
    assert entry.meanings[0].entry_id == entry.tdk_id
    assert entry.meanings[0].examples[0].example == "Örnek kullanım cümlesi."
    assert entry.proverbs[0].proverb == "örnek atasözü"
    assert [word.entry for word in entry.compound_words] == [
        "örnek birleşik",
        "örnek tamlama",
    ]


class TestNormalizeQuery:
    def test_lowercases(self):
        assert _normalize_query("  ÖRNEK  ") == "örnek"

    def test_preserves_circumflex(self):
        assert _normalize_query("ÖRNEKÂ") == "örnekâ"

    def test_strips_punctuation(self):
        assert _normalize_query("örnek.") == "örnek"

    def test_collapses_whitespace(self):
        assert _normalize_query("örnek  sözcük") == "örnek sözcük"

    def test_preserves_internal_apostrophe(self):
        assert _normalize_query("Örnek'an") == "örnek'an"
