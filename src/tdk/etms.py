from aiohttp import ClientSession

from tdk.etc.tools import dictionary_order
from tdk.internal.http import with_http_session
from tdk.internal.utils import make_sync


@with_http_session
async def get_etms_index(query: str, /, *,
                         http_session: ClientSession) -> list[str]:
    async with http_session.get(
        "https://sozluk.gov.tr/etmsAutoComp.json",
        params={"ara": query}
    ) as response:
        return sorted(
            [
                entry["madde"]
                for entry in
                await response.json()
            ],
            key=dictionary_order
        )


@make_sync(get_etms_index)
def get_etms_index_sync(): ...
