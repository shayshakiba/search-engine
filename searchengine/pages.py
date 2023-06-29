from searchengine.page import Page, ParsedContent


_pages: list[Page] = []


def add(page: Page) -> None:
    _pages.append(page)


def get(page_id: int) -> Page | None:
    for page in _pages:
        if page.id == page_id:
            return page

    return None
