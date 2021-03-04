import json
import urllib.request

import remote_paths
from parsers import parse_autocomplete_index


def get_index() -> list:
    with urllib.request.urlopen(url=remote_paths.autocomplete_index()) as response:
        autocomplete_index = json.loads(response.read())
        return parse_autocomplete_index(autocomplete_index)
