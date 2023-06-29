from searchengine.page import Page


PostingList = set[int]
Index = dict[str, PostingList]

_title_index: Index = {}
_body_index: Index = {}


def index_page(page: Page) -> None:
    _index_title(page)
    _index_body(page)


def _index_title(page: Page) -> None:
    for term in page.parsed_content.title.split():
        if term not in _title_index:
            _title_index[term] = set()

        _title_index[term].add(page.id)


def _index_body(page: Page) -> None:
    for term in page.parsed_content.body.split():
        if term not in _body_index:
            _body_index[term] = set()

        _body_index[term].add(page.id)
