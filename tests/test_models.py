from tdk.classifications import OriginLanguage
from tdk.classifications.meaning_properties import MeaningProperty
from tdk.models import Writer, Proverb, MeaningExample, Meaning, Entry, TdkModel


def test_tdkmodel_equality():
    model_1 = TdkModel()
    model_2 = TdkModel()

    model_1.point = "gibberish"
    model_2.point = "gibberish"

    assert model_1 == model_2

    model_2.point = "meaningful"

    assert model_1 != model_2

    model_1.point = "meaningful"

    assert model_1 == model_2


def test_writer_parser():
    standard_writer = Writer(
        tdk_id=1,
        full_name="Faili Meçhul",
        short_name="F. Meçh.",
    )
    serialized_writer = {
        "yazar_id": "1",
        "tam_adi": "Faili Meçhul",
        "kisa_adi": "F. Meçh.",
    }
    assert Writer.parse(serialized_writer) == standard_writer


def test_proverb_parser():
    standard_proverb = Proverb(
        tdk_id=1,
        proverb="Yapınız.",
        prefix=None,
    )
    serialized_proverb = {
        "madde_id": "1",
        "madde": "Yapınız.",
        "on_taki": None,
    }
    assert Proverb.parse(serialized_proverb) == standard_proverb


def test_meaning_example_parser():
    standard_meaning_example = MeaningExample(
        tdk_id=1,
        meaning_id=2,
        order=3,
        example="Ediniz.",
        writer=Writer(
            tdk_id=4,
            full_name="Sait Faik Abasıyanık",
            short_name="S. F. Abasıyanık",
        )
    )
    serialized_meaning_example = {
        "ornek_id": "1",
        "anlam_id": "2",
        "ornek_sira": "3",
        "ornek": "Ediniz.",
        "yazar": [
            {
                "yazar_id": "4",
                "tam_adi": "Sait Faik Abasıyanık",
                "kisa_adi": "S. F. Abasıyanık",
            }
        ]
    }
    assert MeaningExample.parse(serialized_meaning_example) == standard_meaning_example


def test_meaning_parser():
    standard_meaning = Meaning(
        tdk_id=1,
        meaning="Anlamıdır.",
        order=2,
        is_verb=True,
        entry_id=4,
        examples=[
            MeaningExample(
                tdk_id=5,
                meaning_id=6,
                order=7,
                example="Manasıdır.",
                writer=Writer(
                    tdk_id=8,
                    full_name="Reşat Nuri Güntekin",
                    short_name="R. N. Güntekin",
                )
            )
        ],
        properties=[
            MeaningProperty.NOUN,
            MeaningProperty.LINGUISTICS,
            MeaningProperty.LOGIC,
        ]
    )
    serialized_meaning = {
        "anlam_id": "1",
        "anlam": "Anlamıdır.",
        "anlam_sira": "2",
        "fiil": "1",
        "madde_id": "4",
        "orneklerListe": [
            {
                "ornek_id": "5",
                "anlam_id": "6",
                "ornek_sira": "7",
                "ornek": "Manasıdır.",
                "yazar": [
                    {
                        "yazar_id": "8",
                        "tam_adi": "Reşat Nuri Güntekin",
                        "kisa_adi": "R. N. Güntekin",
                    }
                ]
            }
        ],
        "ozelliklerListe": [
            {"ozellik_id": "19", "tur": "3", "tam_adi": "isim", "kisa_adi": "a.", "ekno": "30"},
            {"ozellik_id": "84", "tur": "1", "tam_adi": "dil bilimi", "kisa_adi": "dil b.", "ekno": "289"},
            {"ozellik_id": "65", "tur": "1", "tam_adi": "mantık", "kisa_adi": "man.", "ekno": "116"},
        ]
    }
    assert Meaning.parse(serialized_meaning) == standard_meaning


def test_entry_parser():
    standard_entry = Entry(
        tdk_id=1,
        entry="Girdi",
        plural=False,
        proper=True,
        origin_language=OriginLanguage.ORIGINAL,
        original="zaten orijinal!",
        entry_normalized="girdi",
        meanings=[
            Meaning("Girilen şey.", 2, 3, False, 4, [], []),
        ],
        proverbs=[
            Proverb(5, "Giren çıkar.", None),
        ],
        pronunciation="gir'di",
        prefix="önek-",
        suffix="-sonek",
    )
    serialized_entry = {
        "madde_id": "1",
        "madde": "Girdi",
        "cogul_mu": "0",
        "ozel_mi": "1",
        "lisan_kodu": "0",
        "lisan": "zaten orijinal!",
        "madde_duz": "girdi",
        "anlamlarListe": [
            {
                "anlam": "Girilen şey.",
                "anlam_id": "2",
                "anlam_sira": "3",
                "fiil": False,
                "madde_id": 4,
                "orneklerListe": [],
                "ozelliklerListe": [],
            },
        ],
        "atasozu": [
            {
                "madde_id": "5",
                "madde": "Giren çıkar.",
                "on_taki": None,
            },
        ],
        "telaffuz": "gir'di",
        "on_taki": "önek-",
        "taki": "-sonek",
    }
    assert Entry.parse(serialized_entry) == standard_entry
