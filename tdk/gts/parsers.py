from ..tools import alphabetic_radix


def parse_index(raw_index):
    def distinct(seq) -> list:
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    return distinct(
        sorted(
            [entry["madde"] for entry in raw_index],
            key=alphabetic_radix)
    )
