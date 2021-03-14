from enum import Enum
from collections import namedtuple


MeaningProperties = namedtuple("MeaningProperties", ["id", "kind", "full_name", "short_name", "number"])

_lookup_table = {}


class MeaningProperty(Enum):
    EXCLAMATION = MeaningProperties(18, 3, "ünlem", "ünl.", 29)
    NOUN = MeaningProperties(19, 3, "isim", "a.", 30)
    ADJECTIVE = MeaningProperties(20, 3, "sıfat", "sf.", 31)
    DATIVE = MeaningProperties(21, 3, "-e", "-e", 32)
    ACCUSATIVE = MeaningProperties(22, 3, "-i", "-i", 33)
    INTRANSITIVE = MeaningProperties(23, 3, "nesnesiz", "nsz.", 34)
    ADVERB = MeaningProperties(24, 3, "zarf", "zf.", 35)
    BY = MeaningProperties(25, 3, "-le", "-le", 36)
    ABLATIVE = MeaningProperties(26, 3, "-den", "-den", 37)
    PARTICLE = MeaningProperties(27, 3, "edat", "e.", 38)
    CONJUNCTION = MeaningProperties(28, 3, "bağlaç", "bağ.", 39)
    PRONOUN = MeaningProperties(29, 3, "zamir", "zm.", 40)
    SLANG = MeaningProperties(30, 4, "argo", "argo", 41)
    OBSOLETE = MeaningProperties(31, 4, "eskimiş", "esk.", 42)
    METAPHOR = MeaningProperties(32, 4, "mecaz", "mec.", 43)
    LAY = MeaningProperties(33, 4, "halk ağzında", "hlk.", 44)
    COLLOQUIAL = MeaningProperties(34, 4, "teklifsiz konuşmada", "tkz.", 45)
    SATIRIC = MeaningProperties(35, 4, "alay yollu", "alay", 46)
    VULGAR = MeaningProperties(36, 4, "kaba konuşmada", "kaba", 47)
    JOCULAR = MeaningProperties(37, 4, "şaka yollu", "şaka", 48)
    INVECTIVE = MeaningProperties(38, 4, "hakaret yollu", "hkr.", 49)
    MUSIC = MeaningProperties(39, 1, "müzik", "müz.", 88)
    SPORTS = MeaningProperties(40, 1, "spor", "sp.", 89)
    BOTANY = MeaningProperties(41, 1, "bitki bilimi", "bit. b.", 90)
    NAVAL = MeaningProperties(42, 1, "denizcilik", "den.", 91)
    HISTORY = MeaningProperties(43, 1, "tarih", "tar.", 92)
    ASTRONOMY = MeaningProperties(44, 1, "gök bilimi", "gök b.", 93)
    GEOGRAPHY = MeaningProperties(45, 1, "coğrafya", "coğ.", 94)
    GRAMMAR = MeaningProperties(46, 1, "dil bilgisi", "db.", 95)
    PSYCHOLOGY = MeaningProperties(47, 1, "ruh bilimi", "ruh b.", 96)
    CHEMISTRY = MeaningProperties(48, 1, "kimya", "kim.", 97)
    ANATOMY = MeaningProperties(49, 1, "anatomi", "anat.", 98)
    COMMERCE = MeaningProperties(50, 1, "ticaret", "tic.", 99)
    LAW = MeaningProperties(51, 1, "hukuk", "huk.", 100)
    MATHEMATICS = MeaningProperties(52, 1, "matematik", "mat.", 101)
    ZOOLOGY = MeaningProperties(53, 1, "hayvan bilimi", "hay. b.", 102)
    LITERATURE = MeaningProperties(54, 1, "edebiyat", "ed.", 103)
    CINEMA = MeaningProperties(55, 1, "sinema", "sin.", 104)
    BIOLOGY = MeaningProperties(56, 1, "biyoloji", "biy.", 105)
    PHILOSOPHY = MeaningProperties(57, 1, "felsefe", "fel.", 106)
    PHYSICS = MeaningProperties(58, 1, "fizik", "fiz.", 108)
    THEATRICAL = MeaningProperties(59, 1, "tiyatro", "tiy.", 109)
    GEOLOGY = MeaningProperties(60, 1, "jeoloji", "jeol.", 110)
    TECHNICAL = MeaningProperties(61, 1, "teknik", "tek.", 112)
    SOCIOLOGY = MeaningProperties(62, 1, "toplum bilimi", "top. b.", 113)
    PHYSIOLOGY = MeaningProperties(63, 1, "fizyoloji", "fizy.", 114)
    METEOROLOGY = MeaningProperties(64, 1, "meteoroloji", "meteor.", 115)
    LOGIC = MeaningProperties(65, 1, "mantık", "man.", 116)
    ECONOMY = MeaningProperties(66, 1, "ekonomi", "ekon.", 117)
    ARCHITECTURE = MeaningProperties(67, 1, "mimarlık", "mim.", 118)
    MINERALOGY = MeaningProperties(68, 1, "mineraloji", "min.", 119)
    PEDAGOGY = MeaningProperties(69, 1, "eğitim bilimi", "eğt.", 120)
    MILITARY = MeaningProperties(73, 1, "askerlik", "ask.", 124)
    GEOMETRY = MeaningProperties(80, 1, "geometri", "geom.", 253)
    TECHNOLOGY = MeaningProperties(81, 1, "teknoloji", "tekno.", 264)
    AUXILIARY_VERB = MeaningProperties(82, 3, "yardımcı  fiil", "yar.", 271)
    LOCATIVE = MeaningProperties(83, 3, "-de", "-de", 274)
    LINGUISTICS = MeaningProperties(84, 1, "dil bilimi", "dil b.", 289)
    MEDICINE = MeaningProperties(85, 1, "tıp", "tıp", 307)
    TELEVISION = MeaningProperties(87, 1, "televizyon", "TV", 325)
    RELIGION = MeaningProperties(88, 1, "din bilgisi", "din b.", 326)
    MINING = MeaningProperties(96, 1, "madencilik", "mdn.", 364)
    IT = MeaningProperties(98, 1, "bilişim", "bl.", 368)
    MYTHOLOGY = MeaningProperties(99, 1, "mit.", "mit.", 376)
    ANTHROPOLOGY = MeaningProperties(105, 1, "antropoloji", "ant.", 404)

    @staticmethod
    def get(arg):
        return _lookup_table[arg]


for enum_value in MeaningProperty:
    _lookup_table = {
        **_lookup_table,
        enum_value.value.id: enum_value,
        enum_value.value.full_name: enum_value,
        enum_value.value.short_name: enum_value,
    }
