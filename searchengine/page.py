from dataclasses import dataclass
from typing import NamedTuple


class ParsedContent(NamedTuple):
    title: str
    body: str


@dataclass
class Page:
    id: int
    url: str
    parsed_content: ParsedContent
