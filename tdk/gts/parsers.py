from ..tools import dictionary_order


def parse_index(raw_index) -> list:
    return sorted([entry["madde"] for entry in raw_index], key=dictionary_order)
