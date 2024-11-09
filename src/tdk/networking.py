import aiohttp

_http_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://sozluk.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.51 "
                  "Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def session_maker() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(headers=_http_headers)
