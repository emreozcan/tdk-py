from enum import Enum, IntEnum
from typing import Annotated

from pydantic import BaseModel, Field, AliasChoices, WrapValidator


class PropertyKind(IntEnum):
    FIELD = 1
    PART_OF_SPEECH = 3
    TONE = 4


class PropertyData(BaseModel):
    id: int = Field(validation_alias=AliasChoices("id", "ozellik_id"))
    kind: PropertyKind = Field(validation_alias=AliasChoices("kind", "tur"))
    full_name: str = Field(validation_alias=AliasChoices("full_name", "tam_adi"))
    short_name: str = Field(validation_alias=AliasChoices("short_name", "kisa_adi"))
    number: int = Field(validation_alias=AliasChoices("number", "ekno"))


class MeaningProperty(Enum):
    EXCLAMATION = PropertyData(id=18, kind=PropertyKind.PART_OF_SPEECH, full_name="ünlem", short_name="ünl.", number=29)
    NOUN = PropertyData(id=19, kind=PropertyKind.PART_OF_SPEECH, full_name="isim", short_name="a.", number=30)
    ADJECTIVE = PropertyData(id=20, kind=PropertyKind.PART_OF_SPEECH, full_name="sıfat", short_name="sf.", number=31)
    DATIVE = PropertyData(id=21, kind=PropertyKind.PART_OF_SPEECH, full_name="-e", short_name="-e", number=32)
    ACCUSATIVE = PropertyData(id=22, kind=PropertyKind.PART_OF_SPEECH, full_name="-i", short_name="-i", number=33)
    INTRANSITIVE = PropertyData(id=23, kind=PropertyKind.PART_OF_SPEECH, full_name="nesnesiz", short_name="nsz.", number=34)
    ADVERB = PropertyData(id=24, kind=PropertyKind.PART_OF_SPEECH, full_name="zarf", short_name="zf.", number=35)
    BY = PropertyData(id=25, kind=PropertyKind.PART_OF_SPEECH, full_name="-le", short_name="-le", number=36)
    ABLATIVE = PropertyData(id=26, kind=PropertyKind.PART_OF_SPEECH, full_name="-den", short_name="-den", number=37)
    PARTICLE = PropertyData(id=27, kind=PropertyKind.PART_OF_SPEECH, full_name="edat", short_name="e.", number=38)
    CONJUNCTION = PropertyData(id=28, kind=PropertyKind.PART_OF_SPEECH, full_name="bağlaç", short_name="bağ.", number=39)
    PRONOUN = PropertyData(id=29, kind=PropertyKind.PART_OF_SPEECH, full_name="zamir", short_name="zm.", number=40)
    SLANG = PropertyData(id=30, kind=PropertyKind.TONE, full_name="argo", short_name="argo", number=41)
    OBSOLETE = PropertyData(id=31, kind=PropertyKind.TONE, full_name="eskimiş", short_name="esk.", number=42)
    METAPHOR = PropertyData(id=32, kind=PropertyKind.TONE, full_name="mecaz", short_name="mec.", number=43)
    LAY = PropertyData(id=33, kind=PropertyKind.TONE, full_name="halk ağzında", short_name="hlk.", number=44)
    COLLOQUIAL = PropertyData(id=34, kind=PropertyKind.TONE, full_name="teklifsiz konuşmada", short_name="tkz.", number=45)
    SATIRIC = PropertyData(id=35, kind=PropertyKind.TONE, full_name="alay yollu", short_name="alay", number=46)
    VULGAR = PropertyData(id=36, kind=PropertyKind.TONE, full_name="kaba konuşmada", short_name="kaba", number=47)
    JOCULAR = PropertyData(id=37, kind=PropertyKind.TONE, full_name="şaka yollu", short_name="şaka", number=48)
    INVECTIVE = PropertyData(id=38, kind=PropertyKind.TONE, full_name="hakaret yollu", short_name="hkr.", number=49)
    MUSIC = PropertyData(id=39, kind=PropertyKind.FIELD, full_name="müzik", short_name="müz.", number=88)
    SPORTS = PropertyData(id=40, kind=PropertyKind.FIELD, full_name="spor", short_name="sp.", number=89)
    BOTANY = PropertyData(id=41, kind=PropertyKind.FIELD, full_name="bitki bilimi", short_name="bit. b.", number=90)
    NAVAL = PropertyData(id=42, kind=PropertyKind.FIELD, full_name="denizcilik", short_name="den.", number=91)
    HISTORY = PropertyData(id=43, kind=PropertyKind.FIELD, full_name="tarih", short_name="tar.", number=92)
    ASTRONOMY = PropertyData(id=44, kind=PropertyKind.FIELD, full_name="gök bilimi", short_name="gök b.", number=93)
    GEOGRAPHY = PropertyData(id=45, kind=PropertyKind.FIELD, full_name="coğrafya", short_name="coğ.", number=94)
    GRAMMAR = PropertyData(id=46, kind=PropertyKind.FIELD, full_name="dil bilgisi", short_name="db.", number=95)
    PSYCHOLOGY = PropertyData(id=47, kind=PropertyKind.FIELD, full_name="ruh bilimi", short_name="ruh b.", number=96)
    CHEMISTRY = PropertyData(id=48, kind=PropertyKind.FIELD, full_name="kimya", short_name="kim.", number=97)
    ANATOMY = PropertyData(id=49, kind=PropertyKind.FIELD, full_name="anatomi", short_name="anat.", number=98)
    COMMERCE = PropertyData(id=50, kind=PropertyKind.FIELD, full_name="ticaret", short_name="tic.", number=99)
    LAW = PropertyData(id=51, kind=PropertyKind.FIELD, full_name="hukuk", short_name="huk.", number=100)
    MATHEMATICS = PropertyData(id=52, kind=PropertyKind.FIELD, full_name="matematik", short_name="mat.", number=101)
    ZOOLOGY = PropertyData(id=53, kind=PropertyKind.FIELD, full_name="hayvan bilimi", short_name="hay. b.", number=102)
    LITERATURE = PropertyData(id=54, kind=PropertyKind.FIELD, full_name="edebiyat", short_name="ed.", number=103)
    CINEMA = PropertyData(id=55, kind=PropertyKind.FIELD, full_name="sinema", short_name="sin.", number=104)
    BIOLOGY = PropertyData(id=56, kind=PropertyKind.FIELD, full_name="biyoloji", short_name="biy.", number=105)
    PHILOSOPHY = PropertyData(id=57, kind=PropertyKind.FIELD, full_name="felsefe", short_name="fel.", number=106)
    PHYSICS = PropertyData(id=58, kind=PropertyKind.FIELD, full_name="fizik", short_name="fiz.", number=108)
    THEATRICAL = PropertyData(id=59, kind=PropertyKind.FIELD, full_name="tiyatro", short_name="tiy.", number=109)
    GEOLOGY = PropertyData(id=60, kind=PropertyKind.FIELD, full_name="jeoloji", short_name="jeol.", number=110)
    TECHNICAL = PropertyData(id=61, kind=PropertyKind.FIELD, full_name="teknik", short_name="tek.", number=112)
    SOCIOLOGY = PropertyData(id=62, kind=PropertyKind.FIELD, full_name="toplum bilimi", short_name="top. b.", number=113)
    PHYSIOLOGY = PropertyData(id=63, kind=PropertyKind.FIELD, full_name="fizyoloji", short_name="fizy.", number=114)
    METEOROLOGY = PropertyData(id=64, kind=PropertyKind.FIELD, full_name="meteoroloji", short_name="meteor.", number=115)
    LOGIC = PropertyData(id=65, kind=PropertyKind.FIELD, full_name="mantık", short_name="man.", number=116)
    ECONOMY = PropertyData(id=66, kind=PropertyKind.FIELD, full_name="ekonomi", short_name="ekon.", number=117)
    ARCHITECTURE = PropertyData(id=67, kind=PropertyKind.FIELD, full_name="mimarlık", short_name="mim.", number=118)
    MINERALOGY = PropertyData(id=68, kind=PropertyKind.FIELD, full_name="mineraloji", short_name="min.", number=119)
    PEDAGOGY = PropertyData(id=69, kind=PropertyKind.FIELD, full_name="eğitim bilimi", short_name="eğt.", number=120)
    MILITARY = PropertyData(id=73, kind=PropertyKind.FIELD, full_name="askerlik", short_name="ask.", number=124)
    GEOMETRY = PropertyData(id=80, kind=PropertyKind.FIELD, full_name="geometri", short_name="geom.", number=253)
    TECHNOLOGY = PropertyData(id=81, kind=PropertyKind.FIELD, full_name="teknoloji", short_name="tekno.", number=264)
    AUXILIARY_VERB = PropertyData(id=82, kind=PropertyKind.PART_OF_SPEECH, full_name="yardımcı  fiil", short_name="yar.", number=271)
    LOCATIVE = PropertyData(id=83, kind=PropertyKind.PART_OF_SPEECH, full_name="-de", short_name="-de", number=274)
    LINGUISTICS = PropertyData(id=84, kind=PropertyKind.FIELD, full_name="dil bilimi", short_name="dil b.", number=289)
    MEDICINE = PropertyData(id=85, kind=PropertyKind.FIELD, full_name="tıp", short_name="tıp", number=307)
    TELEVISION = PropertyData(id=87, kind=PropertyKind.FIELD, full_name="televizyon", short_name="TV", number=325)
    RELIGION = PropertyData(id=88, kind=PropertyKind.FIELD, full_name="din bilgisi", short_name="din b.", number=326)
    MINING = PropertyData(id=96, kind=PropertyKind.FIELD, full_name="madencilik", short_name="mdn.", number=364)
    I_T = PropertyData(id=98, kind=PropertyKind.FIELD, full_name="bilişim", short_name="bl.", number=368)
    MYTHOLOGY = PropertyData(id=99, kind=PropertyKind.FIELD, full_name="mit.", short_name="mit.", number=376)
    ANTHROPOLOGY = PropertyData(id=105, kind=PropertyKind.FIELD, full_name="antropoloji", short_name="ant.", number=404)

    @staticmethod
    def get(arg):
        if isinstance(arg, dict):
            return _lookup_table[int(arg["ozellik_id"])]
        return _lookup_table[arg]


def _validate_property(v, handler):
    if isinstance(v, MeaningProperty):
        return v
    return handler(MeaningProperty.get(v))


ValidatedProperty = Annotated[MeaningProperty, WrapValidator(_validate_property)]


_lookup_table = {}


for enum_value in MeaningProperty:
    _lookup_table = {
        **_lookup_table,
        enum_value.value.id: enum_value,
        enum_value.value.full_name: enum_value,
        enum_value.value.short_name: enum_value,
    }
