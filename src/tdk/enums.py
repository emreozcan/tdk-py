"""
Enums and data classes used in the package.
"""

from __future__ import annotations

from enum import Enum, IntEnum

from pydantic import BaseModel, Field, AliasChoices


__all__ = [
    "LetterType",
    "SyllableType",
    "OriginLanguage",
    "PropertyKind",
    "PropertyData",
    "MeaningProperty",
]


class LetterType(Enum):
    """Letter types for Turkish alphabet."""
    SHORT_VOWEL = 0
    """The letter is contained in [](VOWELS)."""
    LONG_VOWEL = 1
    """The letter is contained in [](LONG_VOWELS)."""
    CONSONANT = 2
    """The letter is contained in [](CONSONANTS)."""


class SyllableType(Enum):
    """Syllable types according to aruz prosody rules."""
    OPEN = 0
    """The syllable ends with a vowel."""
    CLOSED = 1
    """The syllable ends with a consonant."""
    MEDLI = 2
    """The syllable has a long vowel or has two consecutive consonants."""


class OriginLanguage(IntEnum):
    """Languages that the words from {py:mod}`tdk.gts` can be from.

    Numbers are the IDs of the languages as seen in the TDK database.
    """

    ORIGINAL = 0
    """The word is originally Turkish."""
    COMPOUND = 19
    """The word is a compound word with parts from more than one language."""

    ARABIC = 11
    PERSIAN = 12
    FRENCH = 13
    ITALIAN = 14
    GREEK = 15
    LATIN = 16
    ENGLISH = 18
    SPANISH = 20
    ARMENIAN = 21
    RUSSIAN = 22
    GERMAN = 23
    SLAVIC = 24
    HEBREW = 25
    HUNGARIAN = 26
    BULGARIAN = 27
    PORTUGUESE = 28
    JAPANESE = 346
    ALBANIAN = 348

    MONGOLIAN = 354
    """Mongolian language."""
    MONGOLIAN_2 = 153
    """Also Mongolian language.

    There are two IDs for the same language in the TDK database.
    """

    FINNISH = 392
    ROMAIC = 393
    SOGDIAN = 395
    SERBIAN = 486
    KOREAN = 420


class PropertyKind(IntEnum):
    """Kinds of properties that can be assigned to a word meaning."""
    FIELD = 1
    """The property is a field of study."""
    PART_OF_SPEECH = 3
    """The property is a part of speech."""
    TONE = 4
    """The property is a tone or style of speech."""


class PropertyData(BaseModel):
    """Data class for properties of word meanings."""
    id: int = Field(validation_alias=AliasChoices("id", "ozellik_id"))
    """The ID of the property in the TDK database."""
    kind: PropertyKind = Field(validation_alias=AliasChoices("kind", "tur"))
    """The kind of the property."""
    full_name: str = Field(
        validation_alias=AliasChoices("full_name", "tam_adi")
    )
    """The full name of the property."""
    short_name: str = Field(
        validation_alias=AliasChoices("short_name", "kisa_adi")
    )
    """The short name of the property."""
    number: int = Field(validation_alias=AliasChoices("number", "ekno"))
    """The additional number of the property in the TDK database (`ekno`)."""


class MeaningProperty(Enum):
    """List of properties seen in the TDK database."""

    @staticmethod
    def get(arg: int | str) -> MeaningProperty:
        """Get a [](MeaningProperty) from its ID, full or short name.

        :param arg: The ID, full or short name of the property.
        :returns: The property, as a [](MeaningProperty) enum member.
        """
        if isinstance(arg, dict):
            return _property_table[int(arg["ozellik_id"])]
        return _property_table[arg]

    # region Members
    EXCLAMATION = PropertyData(
        id=18,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="ünlem",
        short_name="ünl.",
        number=29,
    )
    """
    :param id: `18`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"ünlem"`
    :param short_name: `"ünl."`
    :param number: `29`
    """
    NOUN = PropertyData(
        id=19,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="isim",
        short_name="a.",
        number=30,
    )
    """
    :param id: `19`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"isim"`
    :param short_name: `"a."`
    :param number: `30`
    """
    ADJECTIVE = PropertyData(
        id=20,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="sıfat",
        short_name="sf.",
        number=31,
    )
    """
    :param id: `20`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"sıfat"`
    :param short_name: `"sf."`
    :param number: `31`
    """
    DATIVE = PropertyData(
        id=21,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="-e",
        short_name="-e",
        number=32,
    )
    """
    :param id: `21`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"-e"`
    :param short_name: `"-e"`
    :param number: `32`
    """
    ACCUSATIVE = PropertyData(
        id=22,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="-i",
        short_name="-i",
        number=33,
    )
    """
    :param id: `22`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"-i"`
    :param short_name: `"-i"`
    :param number: `33`
    """
    INTRANSITIVE = PropertyData(
        id=23,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="nesnesiz",
        short_name="nsz.",
        number=34,
    )
    """
    :param id: `23`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"nesnesiz"`
    :param short_name: `"nsz."`
    :param number: `34`
    """
    ADVERB = PropertyData(
        id=24,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="zarf",
        short_name="zf.",
        number=35,
    )
    """
    :param id: `24`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"zarf"`
    :param short_name: `"zf."`
    :param number: `35`
    """
    BY = PropertyData(
        id=25,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="-le",
        short_name="-le",
        number=36,
    )
    """
    :param id: `25`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"-le"`
    :param short_name: `"-le"`
    :param number: `36`
    """
    ABLATIVE = PropertyData(
        id=26,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="-den",
        short_name="-den",
        number=37,
    )
    """
    :param id: `26`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"-den"`
    :param short_name: `"-den"`
    :param number: `37`
    """
    PARTICLE = PropertyData(
        id=27,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="edat",
        short_name="e.",
        number=38,
    )
    """
    :param id: `27`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"edat"`
    :param short_name: `"e."`
    :param number: `38`
    """
    CONJUNCTION = PropertyData(
        id=28,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="bağlaç",
        short_name="bağ.",
        number=39,
    )
    """
    :param id: `28`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"bağlaç"`
    :param short_name: `"bağ."`
    :param number: `39`
    """
    PRONOUN = PropertyData(
        id=29,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="zamir",
        short_name="zm.",
        number=40,
    )
    """
    :param id: `29`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"zamir"`
    :param short_name: `"zm."`
    :param number: `40`
    """
    SLANG = PropertyData(
        id=30,
        kind=PropertyKind.TONE,
        full_name="argo",
        short_name="argo",
        number=41,
    )
    """
    :param id: `30`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"argo"`
    :param short_name: `"argo"`
    :param number: `41`
    """
    OBSOLETE = PropertyData(
        id=31,
        kind=PropertyKind.TONE,
        full_name="eskimiş",
        short_name="esk.",
        number=42,
    )
    """
    :param id: `31`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"eskimiş"`
    :param short_name: `"esk."`
    :param number: `42`
    """
    METAPHOR = PropertyData(
        id=32,
        kind=PropertyKind.TONE,
        full_name="mecaz",
        short_name="mec.",
        number=43,
    )
    """
    :param id: `32`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"mecaz"`
    :param short_name: `"mec."`
    :param number: `43`
    """
    LAY = PropertyData(
        id=33,
        kind=PropertyKind.TONE,
        full_name="halk ağzında",
        short_name="hlk.",
        number=44,
    )
    """
    :param id: `33`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"halk ağzında"`
    :param short_name: `"hlk."`
    :param number: `44`
    """
    COLLOQUIAL = PropertyData(
        id=34,
        kind=PropertyKind.TONE,
        full_name="teklifsiz konuşmada",
        short_name="tkz.",
        number=45,
    )
    """
    :param id: `34`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"teklifsiz konuşmada"`
    :param short_name: `"tkz."`
    :param number: `45`
    """
    SATIRIC = PropertyData(
        id=35,
        kind=PropertyKind.TONE,
        full_name="alay yollu",
        short_name="alay",
        number=46,
    )
    """
    :param id: `35`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"alay yollu"`
    :param short_name: `"alay"`
    :param number: `46`
    """
    VULGAR = PropertyData(
        id=36,
        kind=PropertyKind.TONE,
        full_name="kaba konuşmada",
        short_name="kaba",
        number=47,
    )
    """
    :param id: `36`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"kaba konuşmada"`
    :param short_name: `"kaba"`
    :param number: `47`
    """
    JOCULAR = PropertyData(
        id=37,
        kind=PropertyKind.TONE,
        full_name="şaka yollu",
        short_name="şaka",
        number=48,
    )
    """
    :param id: `37`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"şaka yollu"`
    :param short_name: `"şaka"`
    :param number: `48`
    """
    INVECTIVE = PropertyData(
        id=38,
        kind=PropertyKind.TONE,
        full_name="hakaret yollu",
        short_name="hkr.",
        number=49,
    )
    """
    :param id: `38`
    :param kind: [`TONE`](PropertyKind.TONE)
    :param full_name: `"hakaret yollu"`
    :param short_name: `"hkr."`
    :param number: `49`
    """
    MUSIC = PropertyData(
        id=39,
        kind=PropertyKind.FIELD,
        full_name="müzik",
        short_name="müz.",
        number=88,
    )
    """
    :param id: `39`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"müzik"`
    :param short_name: `"müz."`
    :param number: `88`
    """
    SPORTS = PropertyData(
        id=40,
        kind=PropertyKind.FIELD,
        full_name="spor",
        short_name="sp.",
        number=89,
    )
    """
    :param id: `40`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"spor"`
    :param short_name: `"sp."`
    :param number: `89`
    """
    BOTANY = PropertyData(
        id=41,
        kind=PropertyKind.FIELD,
        full_name="bitki bilimi",
        short_name="bit. b.",
        number=90,
    )
    """
    :param id: `41`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"bitki bilimi"`
    :param short_name: `"bit. b."`
    :param number: `90`
    """
    NAVAL = PropertyData(
        id=42,
        kind=PropertyKind.FIELD,
        full_name="denizcilik",
        short_name="den.",
        number=91,
    )
    """
    :param id: `42`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"denizcilik"`
    :param short_name: `"den."`
    :param number: `91`
    """
    HISTORY = PropertyData(
        id=43,
        kind=PropertyKind.FIELD,
        full_name="tarih",
        short_name="tar.",
        number=92,
    )
    """
    :param id: `43`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"tarih"`
    :param short_name: `"tar."`
    :param number: `92`
    """
    ASTRONOMY = PropertyData(
        id=44,
        kind=PropertyKind.FIELD,
        full_name="gök bilimi",
        short_name="gök b.",
        number=93,
    )
    """
    :param id: `44`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"gök bilimi"`
    :param short_name: `"gök b."`
    :param number: `93`
    """
    GEOGRAPHY = PropertyData(
        id=45,
        kind=PropertyKind.FIELD,
        full_name="coğrafya",
        short_name="coğ.",
        number=94,
    )
    """
    :param id: `45`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"coğrafya"`
    :param short_name: `"coğ."`
    :param number: `94`
    """
    GRAMMAR = PropertyData(
        id=46,
        kind=PropertyKind.FIELD,
        full_name="dil bilgisi",
        short_name="db.",
        number=95,
    )
    """
    :param id: `46`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"dil bilgisi"`
    :param short_name: `"db."`
    :param number: `95`
    """
    PSYCHOLOGY = PropertyData(
        id=47,
        kind=PropertyKind.FIELD,
        full_name="ruh bilimi",
        short_name="ruh b.",
        number=96,
    )
    """
    :param id: `47`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"ruh bilimi"`
    :param short_name: `"ruh b."`
    :param number: `96`
    """
    CHEMISTRY = PropertyData(
        id=48,
        kind=PropertyKind.FIELD,
        full_name="kimya",
        short_name="kim.",
        number=97,
    )
    """
    :param id: `48`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"kimya"`
    :param short_name: `"kim."`
    :param number: `97`
    """
    ANATOMY = PropertyData(
        id=49,
        kind=PropertyKind.FIELD,
        full_name="anatomi",
        short_name="anat.",
        number=98,
    )
    """
    :param id: `49`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"anatomi"`
    :param short_name: `"anat."`
    :param number: `98`
    """
    COMMERCE = PropertyData(
        id=50,
        kind=PropertyKind.FIELD,
        full_name="ticaret",
        short_name="tic.",
        number=99,
    )
    """
    :param id: `50`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"ticaret"`
    :param short_name: `"tic."`
    :param number: `99`
    """
    LAW = PropertyData(
        id=51,
        kind=PropertyKind.FIELD,
        full_name="hukuk",
        short_name="huk.",
        number=100,
    )
    """
    :param id: `51`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"hukuk"`
    :param short_name: `"huk."`
    :param number: `100`
    """
    MATHEMATICS = PropertyData(
        id=52,
        kind=PropertyKind.FIELD,
        full_name="matematik",
        short_name="mat.",
        number=101,
    )
    """
    :param id: `52`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"matematik"`
    :param short_name: `"mat."`
    :param number: `101`
    """
    ZOOLOGY = PropertyData(
        id=53,
        kind=PropertyKind.FIELD,
        full_name="hayvan bilimi",
        short_name="hay. b.",
        number=102,
    )
    """
    :param id: `53`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"hayvan bilimi"`
    :param short_name: `"hay. b."`
    :param number: `102`
    """
    LITERATURE = PropertyData(
        id=54,
        kind=PropertyKind.FIELD,
        full_name="edebiyat",
        short_name="ed.",
        number=103,
    )
    """
    :param id: `54`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"edebiyat"`
    :param short_name: `"ed."`
    :param number: `103`
    """
    CINEMA = PropertyData(
        id=55,
        kind=PropertyKind.FIELD,
        full_name="sinema",
        short_name="sin.",
        number=104,
    )
    """
    :param id: `55`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"sinema"`
    :param short_name: `"sin."`
    :param number: `104`
    """
    BIOLOGY = PropertyData(
        id=56,
        kind=PropertyKind.FIELD,
        full_name="biyoloji",
        short_name="biy.",
        number=105,
    )
    """
    :param id: `56`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"biyoloji"`
    :param short_name: `"biy."`
    :param number: `105`
    """
    PHILOSOPHY = PropertyData(
        id=57,
        kind=PropertyKind.FIELD,
        full_name="felsefe",
        short_name="fel.",
        number=106,
    )
    """
    :param id: `57`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"felsefe"`
    :param short_name: `"fel."`
    :param number: `106`
    """
    PHYSICS = PropertyData(
        id=58,
        kind=PropertyKind.FIELD,
        full_name="fizik",
        short_name="fiz.",
        number=108,
    )
    """
    :param id: `58`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"fizik"`
    :param short_name: `"fiz."`
    :param number: `108`
    """
    THEATRICAL = PropertyData(
        id=59,
        kind=PropertyKind.FIELD,
        full_name="tiyatro",
        short_name="tiy.",
        number=109,
    )
    """
    :param id: `59`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"tiyatro"`
    :param short_name: `"tiy."`
    :param number: `109`
    """
    GEOLOGY = PropertyData(
        id=60,
        kind=PropertyKind.FIELD,
        full_name="jeoloji",
        short_name="jeol.",
        number=110,
    )
    """
    :param id: `60`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"jeoloji"`
    :param short_name: `"jeol."`
    :param number: `110`
    """
    TECHNICAL = PropertyData(
        id=61,
        kind=PropertyKind.FIELD,
        full_name="teknik",
        short_name="tek.",
        number=112,
    )
    """
    :param id: `61`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"teknik"`
    :param short_name: `"tek."`
    :param number: `112`
    """
    SOCIOLOGY = PropertyData(
        id=62,
        kind=PropertyKind.FIELD,
        full_name="toplum bilimi",
        short_name="top. b.",
        number=113,
    )
    """
    :param id: `62`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"toplum bilimi"`
    :param short_name: `"top. b."`
    :param number: `113`
    """
    PHYSIOLOGY = PropertyData(
        id=63,
        kind=PropertyKind.FIELD,
        full_name="fizyoloji",
        short_name="fizy.",
        number=114,
    )
    """
    :param id: `63`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"fizyoloji"`
    :param short_name: `"fizy."`
    :param number: `114`
    """
    METEOROLOGY = PropertyData(
        id=64,
        kind=PropertyKind.FIELD,
        full_name="meteoroloji",
        short_name="meteor.",
        number=115,
    )
    """
    :param id: `64`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"meteoroloji"`
    :param short_name: `"meteor."`
    :param number: `115`
    """
    LOGIC = PropertyData(
        id=65,
        kind=PropertyKind.FIELD,
        full_name="mantık",
        short_name="man.",
        number=116,
    )
    """
    :param id: `65`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"mantık"`
    :param short_name: `"man."`
    :param number: `116`
    """
    ECONOMY = PropertyData(
        id=66,
        kind=PropertyKind.FIELD,
        full_name="ekonomi",
        short_name="ekon.",
        number=117,
    )
    """
    :param id: `66`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"ekonomi"`
    :param short_name: `"ekon."`
    :param number: `117`
    """
    ARCHITECTURE = PropertyData(
        id=67,
        kind=PropertyKind.FIELD,
        full_name="mimarlık",
        short_name="mim.",
        number=118,
    )
    """
    :param id: `67`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"mimarlık"`
    :param short_name: `"mim."`
    :param number: `118`
    """
    MINERALOGY = PropertyData(
        id=68,
        kind=PropertyKind.FIELD,
        full_name="mineraloji",
        short_name="min.",
        number=119,
    )
    """
    :param id: `68`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"mineraloji"`
    :param short_name: `"min."`
    :param number: `119`
    """
    PEDAGOGY = PropertyData(
        id=69,
        kind=PropertyKind.FIELD,
        full_name="eğitim bilimi",
        short_name="eğt.",
        number=120,
    )
    """
    :param id: `69`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"eğitim bilimi"`
    :param short_name: `"eğt."`
    :param number: `120`
    """
    MILITARY = PropertyData(
        id=73,
        kind=PropertyKind.FIELD,
        full_name="askerlik",
        short_name="ask.",
        number=124,
    )
    """
    :param id: `73`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"askerlik"`
    :param short_name: `"ask."`
    :param number: `124`
    """
    GEOMETRY = PropertyData(
        id=80,
        kind=PropertyKind.FIELD,
        full_name="geometri",
        short_name="geom.",
        number=253,
    )
    """
    :param id: `80`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"geometri"`
    :param short_name: `"geom."`
    :param number: `253`
    """
    TECHNOLOGY = PropertyData(
        id=81,
        kind=PropertyKind.FIELD,
        full_name="teknoloji",
        short_name="tekno.",
        number=264,
    )
    """
    :param id: `81`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"teknoloji"`
    :param short_name: `"tekno."`
    :param number: `264`
    """
    AUXILIARY_VERB = PropertyData(
        id=82,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="yardımcı  fiil",
        short_name="yar.",
        number=271,
    )
    """
    :param id: `82`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"yardımcı  fiil"`
    :param short_name: `"yar."`
    :param number: `271`
    """
    LOCATIVE = PropertyData(
        id=83,
        kind=PropertyKind.PART_OF_SPEECH,
        full_name="-de",
        short_name="-de",
        number=274,
    )
    """
    :param id: `83`
    :param kind: [`PART_OF_SPEECH`](PropertyKind.PART_OF_SPEECH)
    :param full_name: `"-de"`
    :param short_name: `"-de"`
    :param number: `274`
    """
    LINGUISTICS = PropertyData(
        id=84,
        kind=PropertyKind.FIELD,
        full_name="dil bilimi",
        short_name="dil b.",
        number=289,
    )
    """
    :param id: `84`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"dil bilimi"`
    :param short_name: `"dil b."`
    :param number: `289`
    """
    MEDICINE = PropertyData(
        id=85,
        kind=PropertyKind.FIELD,
        full_name="tıp",
        short_name="tıp",
        number=307,
    )
    """
    :param id: `85`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"tıp"`
    :param short_name: `"tıp"`
    :param number: `307`
    """
    TELEVISION = PropertyData(
        id=87,
        kind=PropertyKind.FIELD,
        full_name="televizyon",
        short_name="TV",
        number=325,
    )
    """
    :param id: `87`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"televizyon"`
    :param short_name: `"TV"`
    :param number: `325`
    """
    RELIGION = PropertyData(
        id=88,
        kind=PropertyKind.FIELD,
        full_name="din bilgisi",
        short_name="din b.",
        number=326,
    )
    """
    :param id: `88`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"din bilgisi"`
    :param short_name: `"din b."`
    :param number: `326`
    """
    MINING = PropertyData(
        id=96,
        kind=PropertyKind.FIELD,
        full_name="madencilik",
        short_name="mdn.",
        number=364,
    )
    """
    :param id: `96`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"madencilik"`
    :param short_name: `"mdn."`
    :param number: `364`
    """
    I_T = PropertyData(
        id=98,
        kind=PropertyKind.FIELD,
        full_name="bilişim",
        short_name="bl.",
        number=368,
    )
    """
    :param id: `98`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"bilişim"`
    :param short_name: `"bl."`
    :param number: `368`
    """
    MYTHOLOGY = PropertyData(
        id=99,
        kind=PropertyKind.FIELD,
        full_name="mit.",
        short_name="mit.",
        number=376,
    )
    """
    :param id: `99`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"mit."`
    :param short_name: `"mit."`
    :param number: `376`
    """
    ANTHROPOLOGY = PropertyData(
        id=105,
        kind=PropertyKind.FIELD,
        full_name="antropoloji",
        short_name="ant.",
        number=404,
    )
    """
    :param id: `105`
    :param kind: [`FIELD`](PropertyKind.FIELD)
    :param full_name: `"antropoloji"`
    :param short_name: `"ant."`
    :param number: `404`
    """
    # endregion


_property_table: dict[int | str, MeaningProperty] = {}

for enum_value in MeaningProperty:
    _property_table = {
        **_property_table,
        enum_value.value.id: enum_value,
        enum_value.value.full_name: enum_value,
        enum_value.value.short_name: enum_value,
    }
