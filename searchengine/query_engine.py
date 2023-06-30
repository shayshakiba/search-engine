from searchengine import indexes, pages
from searchengine.indexes import Posting
from searchengine.page import Page


TITLE_OCCURRENCE_SCORE = 2
BODY_OCCURRENCE_SCORE = 1


def handle_query(query: str) -> list[Page]:
    terms = query.split()

    title_postings = _get_title_postings(terms)
    body_postings = _get_body_postings(terms)

    total_postings = _get_total_postings(title_postings, body_postings)

    merged_posting = _merge_postings_and(total_postings)

    if len(merged_posting) == 0:
        merged_posting = _merge_postings_or(total_postings)

    ranked_pages = _rank_pages(merged_posting, title_postings, body_postings)

    return pages.get_pages(ranked_pages)


def _get_title_postings(terms: list[str]) -> list[Posting]:
    return [indexes.get_title_posting(term) for term in terms]


def _get_body_postings(terms: list[str]) -> list[Posting]:
    return [indexes.get_body_posting(term) for term in terms]


def _get_total_postings(title_postings: list[Posting], body_postings: list[Posting]) -> list[Posting]:
    return [tp | bp for tp, bp in zip(title_postings, body_postings)]


def _merge_postings_and(postings: list[Posting]) -> Posting:
    return set.intersection(*postings)


def _merge_postings_or(postings: list[Posting]) -> Posting:
    return set.union(*postings)


def _rank_pages(posting: Posting, title_postings: list[Posting], body_postings: list[Posting]) -> list[int]:
    return sorted(posting, key=lambda p: _score_page(p, title_postings, body_postings), reverse=True)


def _score_page(page_id: int, title_postings: list[Posting], body_postings: list[Posting]) -> int:
    score = 0

    for posting in title_postings:
        if page_id in posting:
            score += TITLE_OCCURRENCE_SCORE

    for posting in body_postings:
        if page_id in posting:
            score += BODY_OCCURRENCE_SCORE

    return score
