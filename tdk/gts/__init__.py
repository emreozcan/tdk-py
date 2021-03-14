import json
import urllib.request

from . import remote_paths
from .parsers import parse_index
from ..exceptions import TdkIdLookupErrorException, TdkIdLookupUnexpectedResponseException, \
    TdkSearchUnexpectedResponseException, TdkSearchErrorException


def get_index() -> list:
    with urllib.request.urlopen(url=remote_paths.autocomplete_index()) as response:
        autocomplete_index = json.loads(response.read())
        return parse_index(autocomplete_index)


def search(query: str) -> list:
    with urllib.request.urlopen(url=remote_paths.general_search(query)) as response:
        words = json.loads(response.read())
        if not isinstance(words, list):
            if "error" in words:
                raise TdkSearchErrorException(f'{words["error"]} ({query})')
            else:
                raise TdkSearchUnexpectedResponseException(json.dumps(words))
        else:
            return words


def get_with_id(_id: int) -> dict:
    with urllib.request.urlopen(url=remote_paths.get_with_id(_id)) as response:
        word = json.loads(response.read())
        if not isinstance(word, list):
            if "error" in word:
                raise TdkIdLookupErrorException(f'{word["error"]} ({_id})')
            else:
                raise TdkIdLookupUnexpectedResponseException(json.dumps(word))
        else:
            return word[0]


def get_suggestions(query: str) -> list:
    with urllib.request.urlopen(url=remote_paths.suggest(query)) as response:
        index = json.loads(response.read())
        return parse_index(index)
