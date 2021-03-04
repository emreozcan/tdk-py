REMOTE_AUTOCOMPLETE_INDEX = "autocomplete.json"

REMOTE_GENERAL_SEARCH = "gts"
REMOTE_GENERAL_SEARCH_PARAMETER_MEDIATOR = "?ara="

HOST = "https://sozluk.gov.tr/"


def autocomplete_index():
    return f"{HOST}" \
           f"{REMOTE_AUTOCOMPLETE_INDEX}"


def general_search(term: str):
    import urllib.parse
    return f"{HOST}" \
           f"{REMOTE_GENERAL_SEARCH}" \
           f"{REMOTE_GENERAL_SEARCH_PARAMETER_MEDIATOR}" \
           f"{urllib.parse.quote(term)}"
