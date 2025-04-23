import asyncio
import datetime
from enum import StrEnum
from typing import AsyncGenerator

import aiohttp
import dateutil.parser
from yarl import URL

from jellycat_notify.utils.page import Page, PageMeta


jellycat_site_url = URL("https://jellycat.com/shop-all")
jellycat_search_url = URL("https://d3slzq.a.searchspring.io/api/search/search.json?siteId=d3slzq&resultsFormat=native&page=1&domain=https%3A%2F%2Fjellycat.com%2Fshop-all")


class ProductStatus(StrEnum):
    Live = "Live"
    OutOfStock = "Out of Stock"
    ComingSoon = "Coming Soon"


class Jellycat:
    __slots__ = ("_raw",)

    def __init__(self, raw: dict[str, object]):
        self._raw = raw

    def __eq__(self, other):
        if not isinstance(other, Jellycat):
            return False
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)

    @property
    def name(self) -> str:
        return self._raw["name"]

    @property
    def id(self) -> str:
        return self._raw["id"]

    @property
    def uid(self) -> int:
        return int(self._raw["uid"])

    @property
    def slug(self) -> str:
        relative_url = self._raw["url"]
        assert isinstance(relative_url, str)
        return relative_url.strip("/")

    @property
    def url(self) -> URL:
        return URL(jellycat_site_url.with_path(f"{self.slug}/"))

    @property
    def image_url(self) -> URL:
        return URL(self._raw["imageUrl"])

    @property
    def alt_image_url(self) -> URL:
        return URL(self._raw["ss_image_hover"])

    @property
    def badge_title(self) -> str | None:
        return self._raw.get("ss_badge_title", None)

    @property
    def in_stock(self) -> bool:
        return self._raw["ss_in_stock"] == "1"

    @property
    def is_retired(self) -> bool:
        return self._raw["ss_is_retired"] == "1"

    @property
    def product_status(self) -> ProductStatus:
        raw_product_status = self._raw.get("ss_product_status", None)
        if raw_product_status is None:
            return ProductStatus.OutOfStock
        return ProductStatus(raw_product_status)

    @property
    def available_date(self) -> datetime.date | None:
        if self.badge_title is None: return None
        if not self.badge_title.startswith("Available "): return None
        available_date_string = self.badge_title[10:]
        try:
            available_datetime = dateutil.parser.parse(available_date_string)
        except dateutil.parser.ParserError:
            return None
        return available_datetime.date()

    @property
    def is_available(self):
        return self.product_status == ProductStatus.Live and self.in_stock

    def __repr__(self):
        return f"Jellycat(name={self.name!r}, slug={self.slug!r})"


async def fetch_page_of_jellycats(session: aiohttp.ClientSession, query: dict[str, str]) -> Page[Jellycat]:
    response = await session.get(jellycat_search_url % query)
    body = await response.json()

    pagination_meta_raw = body["pagination"]
    pagination_meta = PageMeta(
        total_items=pagination_meta_raw["totalResults"],
        begin=pagination_meta_raw["begin"],
        end=pagination_meta_raw["end"],
        current_page=pagination_meta_raw["currentPage"],
        total_pages=pagination_meta_raw["totalPages"],
        per_page=pagination_meta_raw["perPage"],
    )

    items = tuple(Jellycat(raw_item) for raw_item in body["results"])
    return Page(
        pagination=pagination_meta,
        items=items,
    )


async def fetch_all_jellycats(session: aiohttp.ClientSession) -> AsyncGenerator[Jellycat]:
    page_cursor = 1
    total_pages = 1
    while page_cursor <= total_pages:
        current_page = await fetch_page_of_jellycats(session, { "page": page_cursor })
        total_pages = current_page.pagination.total_pages
        for item in current_page.items:
            yield item
        page_cursor += 1


async def fetch_one_jellycat(session: aiohttp.ClientSession, slug: str) -> Jellycat:
    page = await fetch_page_of_jellycats(session, { "bgfilter.custom_url": f"/{slug}/" })
    assert len(page.items) == 1
    return page.items[0]


__all__ = (
    "Jellycat",
    "ProductStatus",
    "fetch_all_jellycats",
    "fetch_one_jellycat",
    "fetch_page_of_jellycats",
)


async def main():
    async with aiohttp.ClientSession() as session:
        async for jellycat in fetch_all_jellycats(session):
            print(jellycat)


if __name__ == "__main__":
    asyncio.run(main())
