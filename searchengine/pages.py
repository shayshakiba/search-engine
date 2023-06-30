from searchengine.page import Page


_pages: list[Page] = []


def add(page: Page) -> None:
    _pages.append(page)


def get(page_id: int) -> Page | None:
    for page in _pages:
        if page.id == page_id:
            return page

    return None


def get_pages(page_ids: list[int]) -> list[Page]:
    return [get(page_id) for page_id in page_ids]
