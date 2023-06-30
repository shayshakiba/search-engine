from searchengine.page import Page


Posting = set[int]
Index = dict[str, Posting]

_title_index: Index = {}
_body_index: Index = {}


def index_page(page: Page) -> None:
    _index_title(page)
    _index_body(page)


def get_title_posting(term: str) -> Posting:
    if term not in _title_index:
        return set()

    return _title_index[term]


def get_body_posting(term: str) -> Posting:
    if term not in _body_index:
        return set()

    return _body_index[term]


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
