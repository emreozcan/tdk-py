import urllib.request

_http_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://sozluk.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.51 "
                  "Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def make_request(*args, **kwargs):
    """
    Helper function to add default headers to a urllib request.

    All arguments are passed down to urllib.request.Request,
    Default headers are added if the "headers" keyword argument is not given.
    """
    if "headers" not in kwargs:
        kwargs["headers"] = _http_headers
    return urllib.request.urlopen(urllib.request.Request(*args, **kwargs))
