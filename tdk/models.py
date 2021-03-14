from typing import List

from .classifications import OriginLanguage
from .classifications.meaning_properties import MeaningProperties


class Writer:
    tdk_id: int
    full_name: str
    short_name: str

    def __init__(self, tdk_id: int, full_name: str, short_name: str, number: int):
        self.tdk_id = tdk_id
        self.full_name = full_name
        self.short_name = short_name
        self.number = number

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"<Writer {self.tdk_id} ({self.full_name})>"


class MeaningExample:
    tdk_id: int
    meaning_id: int
    order: int
    example: str
    writer: Writer

    def __init__(self, tdk_id: int, meaning_id: int, order: int, example: str, amount: int, writer: Writer):
        self.tdk_id = tdk_id
        self.meaning_id = meaning_id
        self.order = order
        self.example = example
        self.amount = amount
        self.writer = writer

    def __str__(self):
        return self.example

    def __repr__(self):
        return f"<MeaningExample for {self.meaning_id}: {self.tdk_id} ({self.example} - {self.writer.full_name})>"


class Proverb:
    tdk_id: int
    proverb: str
    prefix: str or None

    def __str__(self):
        return self.proverb

    def __repr__(self):
        return f"<Proverb {self.tdk_id} ({self.proverb})>"


class Meaning:
    meaning: str
    tdk_id: int
    order: int
    is_verb: bool
    entry_id: int
    examples: List[MeaningExample]
    properties: List[MeaningProperties]

    def __init__(self, meaning: str, tdk_id: int, order: int, is_verb: bool, gos: int, entry_id: int,
                 examples: List[MeaningExample], properties: List[MeaningProperties], tipkes: int):
        self.meaning = meaning
        self.tdk_id = tdk_id
        self.order = order
        self.is_verb = is_verb
        self.gos = gos
        self.entry_id = entry_id
        self.examples = examples
        self.properties = properties
        self.tipkes = tipkes

    def __str__(self):
        return self.meaning

    def __repr__(self):
        return f"<Meaning for {self.entry_id}: {self.tdk_id} ({self.meaning})>"


class Entry:
    tdk_id: int
    entry: str
    plural: bool
    proper: bool
    origin_language: OriginLanguage
    original: str
    entry_normalized: str or None
    pronunciation: str or None
    prefix: str or None
    suffix: str or None

    def __init__(self, tdk_id: int, entry: str, plural: bool, proper: bool, origin_language: OriginLanguage,
                 original: str, entry_normalized: str or None, pronunciation: str or None, prefix: str or None,
                 suffix: str or None):
        self.tdk_id = tdk_id
        self.entry = entry
        self.plural = plural
        self.proper = proper
        self.origin_language = origin_language
        self.original = original
        self.entry_normalized = entry_normalized
        self.pronunciation = pronunciation
        self.prefix = prefix
        self.suffix = suffix

    def __str__(self):
        return self.entry

    def __repr__(self):
        return f"<Entry {self.tdk_id} ({self.entry})>"
