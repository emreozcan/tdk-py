import json
import urllib.request
from typing import List

from . import remote_paths
from .parsers import parse_index
from ..exceptions import TdkIdLookupErrorException, TdkIdLookupUnexpectedResponseException, \
    TdkSearchUnexpectedResponseException, TdkSearchErrorException
from ..models import Entry
from ..tools import lowercase


def index() -> List[str]:
    with urllib.request.urlopen(url=remote_paths.autocomplete_index()) as response:
        autocomplete_index = json.loads(response.read())
        return parse_index(autocomplete_index)


def search(query: str) -> List[Entry]:
    query = lowercase(query, remove_unknown_characters=False)
    with urllib.request.urlopen(url=remote_paths.general_search(query)) as response:
        words = json.loads(response.read())
        if not isinstance(words, list):
            if "error" in words:
                raise TdkSearchErrorException(f'{words["error"]} ({query})')
            else:
                raise TdkSearchUnexpectedResponseException(json.dumps(words))
        else:
            entry_parser = Entry.parse
            return list(map(entry_parser, words))


def get(_id: int) -> Entry:
    with urllib.request.urlopen(url=remote_paths.get_with_id(_id)) as response:
        word = json.loads(response.read())
        if not isinstance(word, list):
            if "error" in word:
                raise TdkIdLookupErrorException(f'{word["error"]} ({_id})')
            else:
                raise TdkIdLookupUnexpectedResponseException(json.dumps(word))
        else:
            entry_parser = Entry.parse
            return list(map(entry_parser, word))[0]


def suggest(query: str) -> List[str]:
    with urllib.request.urlopen(url=remote_paths.suggest(query)) as response:
        index = json.loads(response.read())
        return parse_index(index)
