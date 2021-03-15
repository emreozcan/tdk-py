import urllib.parse

REMOTE_AUTOCOMPLETE_INDEX = "autocomplete.json"
REMOTE_UPDATED_TURKISH_DICTIONARY = "gts"
REMOTE_UPDATED_TURKISH_DICTIONARY_ID_ENDPOINT = "gts_id"
REMOTE_SUGGESTIONS_DICTIONARY = "oneri"
REMOTE_GENERAL_SEARCH_PARAMETER_MEDIATOR = "?ara="
REMOTE_SUGGESTIONS_SEARCH_PARAMETER_MEDIATOR = "?soz="
REMOTE_ID_MEDIATOR = "?id="

HOST = "https://sozluk.gov.tr/"


def autocomplete_index():
    return f"{HOST}" \
           f"{REMOTE_AUTOCOMPLETE_INDEX}"


def general_search(term: str):
    return f"{HOST}" \
           f"{REMOTE_UPDATED_TURKISH_DICTIONARY}" \
           f"{REMOTE_GENERAL_SEARCH_PARAMETER_MEDIATOR}" \
           f"{urllib.parse.quote(term)}"


def suggest(term: str):
    return f"{HOST}" \
           f"{REMOTE_SUGGESTIONS_DICTIONARY}" \
           f"{REMOTE_SUGGESTIONS_SEARCH_PARAMETER_MEDIATOR}" \
           f"{urllib.parse.quote(term)}"


def get_with_id(_id: int):
    return f"{HOST}" \
           f"{REMOTE_UPDATED_TURKISH_DICTIONARY_ID_ENDPOINT}" \
           f"{REMOTE_ID_MEDIATOR}" \
           f"{_id}"
