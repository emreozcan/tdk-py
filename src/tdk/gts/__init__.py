import json
from typing import List

from . import remote_paths
from .parsers import parse_index
from ..models import Entry
from ..networking import make_request
from ..tools import lowercase


def index() -> List[str]:
    with make_request(url=remote_paths.autocomplete_index()) as response:
        autocomplete_index = json.loads(response.read())
        return parse_index(autocomplete_index)


def search(query: str) -> List[Entry]:
    query = lowercase(query, remove_unknown_characters=False)
    with make_request(url=remote_paths.general_search(query)) as response:
        words = json.loads(response.read())
        if not isinstance(words, list):
            if "error" in words:
                raise RuntimeError(f'The server responded with an error: {words["error"]} ({query})')
            else:
                raise RuntimeError(f"Invalid response type {type(words).__name__} received. (expected list)")
        else:
            entry_parser = Entry.parse
            return list(map(entry_parser, words))


def get(_id: int) -> Entry:
    with make_request(url=remote_paths.get_with_id(_id)) as response:
        word = json.loads(response.read())
        if not isinstance(word, list):
            if isinstance(word, dict) and "error" in word:
                raise RuntimeError(f'The server responded with an error: {word["error"]} ({_id})')
            else:
                raise RuntimeError(f"Invalid response type {type(word).__name__} received. (expected list)")
        else:
            entry_parser = Entry.parse
            return list(map(entry_parser, word))[0]


def suggest(query: str) -> List[str]:
    with make_request(url=remote_paths.suggest(query)) as response:
        response_bytes = response.read()
        if not response_bytes:
            raise RuntimeError("The server returned an invalid response."
                               "\n    See https://github.com/emreozcan/tdk-py/issues/2#issuecomment-1153257967.")
        return parse_index(json.loads(response_bytes))
