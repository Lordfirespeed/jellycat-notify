from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class PageMeta:
    total_items: int
    begin: int
    end: int
    current_page: int
    total_pages: int
    per_page: int


@dataclass(frozen=True)
class Page[T]:
    pagination: PageMeta
    items: Sequence[T]


__all__ = ("PageMeta", "Page")
