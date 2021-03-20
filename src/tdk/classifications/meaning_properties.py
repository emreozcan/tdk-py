from enum import Enum
from collections import namedtuple


MeaningProperties = namedtuple("MeaningProperties", ["id", "kind", "full_name", "short_name", "number"])

_lookup_table = {}


class MeaningPropertyKind(Enum):
    FIELD = 1
    PART_OF_SPEECH = 3
    TONE = 4


class MeaningProperty(Enum):
    EXCLAMATION = MeaningProperties(18, MeaningPropertyKind.PART_OF_SPEECH, "ünlem", "ünl.", 29)
    NOUN = MeaningProperties(19, MeaningPropertyKind.PART_OF_SPEECH, "isim", "a.", 30)
    ADJECTIVE = MeaningProperties(20, MeaningPropertyKind.PART_OF_SPEECH, "sıfat", "sf.", 31)
    DATIVE = MeaningProperties(21, MeaningPropertyKind.PART_OF_SPEECH, "-e", "-e", 32)
    ACCUSATIVE = MeaningProperties(22, MeaningPropertyKind.PART_OF_SPEECH, "-i", "-i", 33)
    INTRANSITIVE = MeaningProperties(23, MeaningPropertyKind.PART_OF_SPEECH, "nesnesiz", "nsz.", 34)
    ADVERB = MeaningProperties(24, MeaningPropertyKind.PART_OF_SPEECH, "zarf", "zf.", 35)
    BY = MeaningProperties(25, MeaningPropertyKind.PART_OF_SPEECH, "-le", "-le", 36)
    ABLATIVE = MeaningProperties(26, MeaningPropertyKind.PART_OF_SPEECH, "-den", "-den", 37)
    PARTICLE = MeaningProperties(27, MeaningPropertyKind.PART_OF_SPEECH, "edat", "e.", 38)
    CONJUNCTION = MeaningProperties(28, MeaningPropertyKind.PART_OF_SPEECH, "bağlaç", "bağ.", 39)
    PRONOUN = MeaningProperties(29, MeaningPropertyKind.PART_OF_SPEECH, "zamir", "zm.", 40)
    SLANG = MeaningProperties(30, MeaningPropertyKind.TONE, "argo", "argo", 41)
    OBSOLETE = MeaningProperties(31, MeaningPropertyKind.TONE, "eskimiş", "esk.", 42)
    METAPHOR = MeaningProperties(32, MeaningPropertyKind.TONE, "mecaz", "mec.", 43)
    LAY = MeaningProperties(33, MeaningPropertyKind.TONE, "halk ağzında", "hlk.", 44)
    COLLOQUIAL = MeaningProperties(34, MeaningPropertyKind.TONE, "teklifsiz konuşmada", "tkz.", 45)
    SATIRIC = MeaningProperties(35, MeaningPropertyKind.TONE, "alay yollu", "alay", 46)
    VULGAR = MeaningProperties(36, MeaningPropertyKind.TONE, "kaba konuşmada", "kaba", 47)
    JOCULAR = MeaningProperties(37, MeaningPropertyKind.TONE, "şaka yollu", "şaka", 48)
    INVECTIVE = MeaningProperties(38, MeaningPropertyKind.TONE, "hakaret yollu", "hkr.", 49)
    MUSIC = MeaningProperties(39, MeaningPropertyKind.FIELD, "müzik", "müz.", 88)
    SPORTS = MeaningProperties(40, MeaningPropertyKind.FIELD, "spor", "sp.", 89)
    BOTANY = MeaningProperties(41, MeaningPropertyKind.FIELD, "bitki bilimi", "bit. b.", 90)
    NAVAL = MeaningProperties(42, MeaningPropertyKind.FIELD, "denizcilik", "den.", 91)
    HISTORY = MeaningProperties(43, MeaningPropertyKind.FIELD, "tarih", "tar.", 92)
    ASTRONOMY = MeaningProperties(44, MeaningPropertyKind.FIELD, "gök bilimi", "gök b.", 93)
    GEOGRAPHY = MeaningProperties(45, MeaningPropertyKind.FIELD, "coğrafya", "coğ.", 94)
    GRAMMAR = MeaningProperties(46, MeaningPropertyKind.FIELD, "dil bilgisi", "db.", 95)
    PSYCHOLOGY = MeaningProperties(47, MeaningPropertyKind.FIELD, "ruh bilimi", "ruh b.", 96)
    CHEMISTRY = MeaningProperties(48, MeaningPropertyKind.FIELD, "kimya", "kim.", 97)
    ANATOMY = MeaningProperties(49, MeaningPropertyKind.FIELD, "anatomi", "anat.", 98)
    COMMERCE = MeaningProperties(50, MeaningPropertyKind.FIELD, "ticaret", "tic.", 99)
    LAW = MeaningProperties(51, MeaningPropertyKind.FIELD, "hukuk", "huk.", 100)
    MATHEMATICS = MeaningProperties(52, MeaningPropertyKind.FIELD, "matematik", "mat.", 101)
    ZOOLOGY = MeaningProperties(53, MeaningPropertyKind.FIELD, "hayvan bilimi", "hay. b.", 102)
    LITERATURE = MeaningProperties(54, MeaningPropertyKind.FIELD, "edebiyat", "ed.", 103)
    CINEMA = MeaningProperties(55, MeaningPropertyKind.FIELD, "sinema", "sin.", 104)
    BIOLOGY = MeaningProperties(56, MeaningPropertyKind.FIELD, "biyoloji", "biy.", 105)
    PHILOSOPHY = MeaningProperties(57, MeaningPropertyKind.FIELD, "felsefe", "fel.", 106)
    PHYSICS = MeaningProperties(58, MeaningPropertyKind.FIELD, "fizik", "fiz.", 108)
    THEATRICAL = MeaningProperties(59, MeaningPropertyKind.FIELD, "tiyatro", "tiy.", 109)
    GEOLOGY = MeaningProperties(60, MeaningPropertyKind.FIELD, "jeoloji", "jeol.", 110)
    TECHNICAL = MeaningProperties(61, MeaningPropertyKind.FIELD, "teknik", "tek.", 112)
    SOCIOLOGY = MeaningProperties(62, MeaningPropertyKind.FIELD, "toplum bilimi", "top. b.", 113)
    PHYSIOLOGY = MeaningProperties(63, MeaningPropertyKind.FIELD, "fizyoloji", "fizy.", 114)
    METEOROLOGY = MeaningProperties(64, MeaningPropertyKind.FIELD, "meteoroloji", "meteor.", 115)
    LOGIC = MeaningProperties(65, MeaningPropertyKind.FIELD, "mantık", "man.", 116)
    ECONOMY = MeaningProperties(66, MeaningPropertyKind.FIELD, "ekonomi", "ekon.", 117)
    ARCHITECTURE = MeaningProperties(67, MeaningPropertyKind.FIELD, "mimarlık", "mim.", 118)
    MINERALOGY = MeaningProperties(68, MeaningPropertyKind.FIELD, "mineraloji", "min.", 119)
    PEDAGOGY = MeaningProperties(69, MeaningPropertyKind.FIELD, "eğitim bilimi", "eğt.", 120)
    MILITARY = MeaningProperties(73, MeaningPropertyKind.FIELD, "askerlik", "ask.", 124)
    GEOMETRY = MeaningProperties(80, MeaningPropertyKind.FIELD, "geometri", "geom.", 253)
    TECHNOLOGY = MeaningProperties(81, MeaningPropertyKind.FIELD, "teknoloji", "tekno.", 264)
    AUXILIARY_VERB = MeaningProperties(82, MeaningPropertyKind.PART_OF_SPEECH, "yardımcı  fiil", "yar.", 271)
    LOCATIVE = MeaningProperties(83, MeaningPropertyKind.PART_OF_SPEECH, "-de", "-de", 274)
    LINGUISTICS = MeaningProperties(84, MeaningPropertyKind.FIELD, "dil bilimi", "dil b.", 289)
    MEDICINE = MeaningProperties(85, MeaningPropertyKind.FIELD, "tıp", "tıp", 307)
    TELEVISION = MeaningProperties(87, MeaningPropertyKind.FIELD, "televizyon", "TV", 325)
    RELIGION = MeaningProperties(88, MeaningPropertyKind.FIELD, "din bilgisi", "din b.", 326)
    MINING = MeaningProperties(96, MeaningPropertyKind.FIELD, "madencilik", "mdn.", 364)
    I_T = MeaningProperties(98, MeaningPropertyKind.FIELD, "bilişim", "bl.", 368)
    MYTHOLOGY = MeaningProperties(99, MeaningPropertyKind.FIELD, "mit.", "mit.", 376)
    ANTHROPOLOGY = MeaningProperties(105, MeaningPropertyKind.FIELD, "antropoloji", "ant.", 404)

    @staticmethod
    def get(arg):
        if isinstance(arg, dict):
            return _lookup_table[int(arg["ozellik_id"])]
        return _lookup_table[arg]


for enum_value in MeaningProperty:
    _lookup_table = {
        **_lookup_table,
        enum_value.value.id: enum_value,
        enum_value.value.full_name: enum_value,
        enum_value.value.short_name: enum_value,
    }
