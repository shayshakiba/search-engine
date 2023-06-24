from dataclasses import dataclass
from typing import NamedTuple


ParsedContent = NamedTuple('ParsedContent', [('title', str), ('body', str)])


@dataclass
class Page:
    page_id: int
    url: str
    parsed_content: ParsedContent
