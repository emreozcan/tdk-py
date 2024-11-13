"""Türk Lehçeleri Sözlüğü\\
Turkic Languages Dictionary
"""

from enum import IntEnum

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, assert_not_found


__all__ = [
    "Lehce",
    "LehceEntry",
    "search_lehce",
    "search_lehce_sync",
]


class Lehce(IntEnum):
    AZERBAIJAN_TURKISH = 4
    BASHKIR_TURKISH = 6
    KAZAKH_TURKISH = 2
    KYRGYZ_TURKISH = 9
    UZBEK_TURKISH = 3
    TATAR_TURKISH = 7
    TURKEY_TURKISH = 1
    TURKMEN_TURKISH = 8
    UYGHUR_TURKISH = 5
    # One of these is not like the other...
    RUSSIAN = 10


class LehceEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "lehce_id"))
    original: str = Field(validation_alias=AliasChoices("original", "asil"))
    turkish: str = Field(validation_alias=AliasChoices("turkish", "turkce"))
    azerbaijan_1: str = Field(
        validation_alias=AliasChoices("azerbaijan_1", "azerice1")
    )
    azerbaijan_2: str = Field(
        validation_alias=AliasChoices("azerbaijan_2", "azerice2")
    )
    azerbaijan_3: str = Field(
        validation_alias=AliasChoices("azerbaijan_3", "azerice3")
    )
    azerbaijan_4: str = Field(
        validation_alias=AliasChoices("azerbaijan_4", "azerice4")
    )
    bashkir_1: str = Field(
        validation_alias=AliasChoices("bashkir_1", "baskurtca1")
    )
    bashkir_2: str = Field(
        validation_alias=AliasChoices("bashkir_2", "baskurtca2")
    )
    bashkir_3: str = Field(
        validation_alias=AliasChoices("bashkir_3", "baskurtca3")
    )
    bashkir_4: str = Field(
        validation_alias=AliasChoices("bashkir_4", "baskurtca4")
    )
    kazakh_1: str = Field(validation_alias=AliasChoices("kazakh_1", "kazakca1"))
    kazakh_2: str = Field(validation_alias=AliasChoices("kazakh_2", "kazakca2"))
    kazakh_3: str = Field(validation_alias=AliasChoices("kazakh_3", "kazakca3"))
    kazakh_4: str = Field(validation_alias=AliasChoices("kazakh_4", "kazakca4"))
    kyrgyz_1: str = Field(
        validation_alias=AliasChoices("kyrgyz_1", "kirgizca1")
    )
    kyrgyz_2: str = Field(
        validation_alias=AliasChoices("kyrgyz_2", "kirgizca2")
    )
    kyrgyz_3: str = Field(
        validation_alias=AliasChoices("kyrgyz_3", "kirgizca3")
    )
    kyrgyz_4: str = Field(
        validation_alias=AliasChoices("kyrgyz_4", "kirgizca4")
    )
    uzbek_1: str = Field(validation_alias=AliasChoices("uzbek_1", "ozbekce1"))
    uzbek_2: str = Field(validation_alias=AliasChoices("uzbek_2", "ozbekce2"))
    uzbek_3: str = Field(validation_alias=AliasChoices("uzbek_3", "ozbekce3"))
    uzbek_4: str = Field(validation_alias=AliasChoices("uzbek_4", "ozbekce4"))
    tatar_1: str = Field(validation_alias=AliasChoices("tatar_1", "tatarca1"))
    tatar_2: str = Field(validation_alias=AliasChoices("tatar_2", "tatarca2"))
    tatar_3: str = Field(validation_alias=AliasChoices("tatar_3", "tatarca3"))
    tatar_4: str = Field(validation_alias=AliasChoices("tatar_4", "tatarca4"))
    turkmen_1: str = Field(
        validation_alias=AliasChoices("turkmen_1", "turkmence1")
    )
    turkmen_2: str = Field(
        validation_alias=AliasChoices("turkmen_2", "turkmence2")
    )
    turkmen_3: str = Field(
        validation_alias=AliasChoices("turkmen_3", "turkmence3")
    )
    turkmen_4: str = Field(
        validation_alias=AliasChoices("turkmen_4", "turkmence4")
    )
    uyghur_1: str = Field(validation_alias=AliasChoices("uyghur_1", "uygurca1"))
    uyghur_2: str = Field(validation_alias=AliasChoices("uyghur_2", "uygurca2"))
    uyghur_3: str = Field(validation_alias=AliasChoices("uyghur_3", "uygurca3"))
    uyghur_4: str = Field(validation_alias=AliasChoices("uyghur_4", "uygurca4"))
    russian_1: str = Field(validation_alias=AliasChoices("russian_1", "rusca1"))
    russian_2: str = Field(validation_alias=AliasChoices("russian_2", "rusca2"))
    russian_3: str = Field(validation_alias=AliasChoices("russian_3", "rusca3"))
    russian_4: str = Field(validation_alias=AliasChoices("russian_4", "rusca4"))


lehce_entry_list_adapter = TypeAdapter(list[LehceEntry])


@make_http_session_optional
async def search_lehce(
    lehce: Lehce, query: str, *, http_session: ClientSession
) -> list[LehceEntry]:
    async with http_session.get(
        f"https://sozluk.gov.tr/lehce?lehce={lehce}&ara={query}"
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            return lehce_entry_list_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_lehce)
def search_lehce_sync(): ...
