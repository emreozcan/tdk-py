from typing import List

from ..tools import dictionary_order


def parse_index(raw_index) -> List[str]:
    return sorted([entry["madde"] for entry in raw_index], key=dictionary_order)
