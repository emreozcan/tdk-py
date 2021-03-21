from enum import Enum
from typing import List

from .classifications import OriginLanguage
from .classifications.meaning_properties import MeaningProperty


class TdkModel:
    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

    def as_dict(self):
        def serialize(obj):
            if isinstance(obj, list):
                if len(obj) == 0:
                    return []
                return list(map(serialize, obj))
            elif isinstance(obj, TdkModel):
                return serialize(obj.as_dict())
            elif isinstance(obj, MeaningProperty):
                return serialize(obj.value.id)
            elif isinstance(obj, Enum):
                return serialize(obj.value)
            return obj
        return {k: serialize(v) for k, v in self.__dict__.items()}


class Writer(TdkModel):
    tdk_id: int
    full_name: str
    short_name: str

    def __init__(self, tdk_id: int, full_name: str, short_name: str):
        self.tdk_id = tdk_id
        self.full_name = full_name
        self.short_name = short_name

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"<Writer {self.tdk_id} ({self.full_name})>"

    @staticmethod
    def parse(writer: dict) -> "Writer":
        return Writer(
            tdk_id=int(writer["yazar_id"]),
            full_name=writer["tam_adi"],
            short_name=writer["kisa_adi"],
        )


class MeaningExample(TdkModel):
    tdk_id: int
    meaning_id: int
    order: int
    example: str
    writer: Writer or None

    def __init__(self, tdk_id: int, meaning_id: int, order: int, example: str, writer: Writer or None = None):
        self.tdk_id = tdk_id
        self.meaning_id = meaning_id
        self.order = order
        self.example = example
        self.writer = writer

    def __str__(self):
        return self.example

    def __repr__(self):
        return f"<MeaningExample for {self.meaning_id}: {self.tdk_id} ({self.example})>"

    @staticmethod
    def parse(example: dict) -> "MeaningExample":
        writer_parser = Writer.parse
        return MeaningExample(
            tdk_id=int(example["ornek_id"]),
            meaning_id=int(example["anlam_id"]),
            order=int(example["ornek_sira"]),
            example=example["ornek"],
            writer=writer_parser(example["yazar"][0]) if "yazar" in example else None,
        )


class Proverb(TdkModel):
    tdk_id: int
    proverb: str
    prefix: str or None

    def __init__(self, tdk_id: int, proverb: str, prefix: str or None = None):
        self.tdk_id = tdk_id
        self.proverb = proverb
        self.prefix = prefix

    def __str__(self):
        return self.proverb

    def __repr__(self):
        return f"<Proverb {self.tdk_id} ({self.proverb})>"

    @staticmethod
    def parse(proverb: dict) -> "Proverb":
        return Proverb(
            tdk_id=int(proverb["madde_id"]),
            proverb=proverb["madde"],
            prefix=proverb["on_taki"],
        )


class Meaning(TdkModel):
    meaning: str
    tdk_id: int
    order: int
    is_verb: bool
    entry_id: int
    examples: List[MeaningExample]
    properties: List[MeaningProperty]

    def __init__(self, meaning: str, tdk_id: int, order: int, is_verb: bool, entry_id: int,
                 examples: List[MeaningExample], properties: List[MeaningProperty]):
        self.meaning = meaning
        self.tdk_id = tdk_id
        self.order = order
        self.is_verb = is_verb
        self.entry_id = entry_id
        self.examples = examples
        self.properties = properties

    def __str__(self):
        return self.meaning

    def __repr__(self):
        return f"<Meaning for {self.entry_id}: {self.tdk_id} ({self.meaning})>"

    @staticmethod
    def parse(meaning: dict) -> "Meaning":
        example_parser = MeaningExample.parse
        example_property_parser = MeaningProperty.get
        return Meaning(
            meaning=meaning["anlam"],
            tdk_id=int(meaning["anlam_id"]),
            order=int(meaning["anlam_sira"]),
            is_verb=bool(int(meaning["fiil"])),
            entry_id=int(meaning["madde_id"]),
            examples=list(map(example_parser, meaning.get("orneklerListe", []))),
            properties=list(map(example_property_parser, meaning.get("ozelliklerListe", []))),
        )


class Entry(TdkModel):
    tdk_id: int
    order: int
    entry: str
    plural: bool
    proper: bool
    origin_language: OriginLanguage
    original: str
    entry_normalized: str or None
    meanings: List[Meaning]
    proverbs: List[Proverb]
    pronunciation: str or None
    prefix: str or None
    suffix: str or None

    def __init__(self, tdk_id: int, order: int, entry: str, plural: bool, proper: bool, origin_language: OriginLanguage,
                 original: str, entry_normalized: str or None = None, meanings=None,
                 proverbs=None, pronunciation: str or None = None, prefix: str or None = None,
                 suffix: str or None = None):
        if meanings is None:
            meanings = []
        if proverbs is None:
            proverbs = []
        self.tdk_id = tdk_id
        self.order = order
        self.entry = entry
        self.plural = plural
        self.proper = proper
        self.origin_language = origin_language
        self.original = original
        self.entry_normalized = entry_normalized
        self.meanings = meanings
        self.proverbs = proverbs
        self.pronunciation = pronunciation
        self.prefix = prefix
        self.suffix = suffix

    def __str__(self):
        return self.entry

    def __repr__(self):
        return f"<Entry {self.tdk_id} ({self.entry})>"

    @staticmethod
    def parse(entry: dict) -> "Entry":
        meaning_parser = Meaning.parse
        proverb_parser = Proverb.parse
        return Entry(
            tdk_id=int(entry["madde_id"]),
            order=int(entry["kac"]),
            entry=entry["madde"],
            plural=bool(int(entry["cogul_mu"])),
            proper=bool(int(entry["ozel_mi"])),
            origin_language=OriginLanguage(int(entry["lisan_kodu"])),
            original=entry["lisan"],
            entry_normalized=entry["madde_duz"],
            meanings=list(map(meaning_parser, entry.get("anlamlarListe", []))),
            proverbs=list(map(proverb_parser, entry.get("atasozu", []))),
            pronunciation=entry["telaffuz"],
            prefix=entry["on_taki"],
            suffix=entry["taki"],
        )
