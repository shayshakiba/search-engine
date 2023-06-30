from searchengine import query_engine
from searchengine.page import Page
import time


def handle_user() -> None:
    while True:
        query = input('Query: ').strip()
        if not query:
            continue
        elif query.lower() == 'exit':
            break

        _handle_query(query)


def _handle_query(query: str) -> None:
    start_time = time.perf_counter()
    results = query_engine.handle_query(query)
    finish_time = time.perf_counter()

    _handle_query_results(query, finish_time - start_time, results)


def _handle_query_results(query: str, response_time: float, results: list[Page]) -> None:
    if len(results) == 0:
        print('No results found!')
        return

    print(f'{len(results)} results found! ({response_time:0.3f} seconds)')
    print('-' * 50)

    for result in results[:1]:
        print(f'URL: {result.url}')
        print()

        print(f'Title: {result.parsed_content.title}')
        print()

        print(
            f'Body Abstract: {_get_body_snippet(query, result.parsed_content.body)}')
        print('-' * 50)


def _get_body_snippet(query: str, body: str) -> str:
    first_query_term = query.split()[0]
    body_terms = body.split()

    if first_query_term in body:
        query_index = body_terms.index(first_query_term)
    else:
        query_index = None

    if len(body_terms) < 100:
        snippet = ' '.join(body_terms)
    elif query_index is None or query_index < 50:
        snippet = f"{' '.join(body_terms[0:100])}..."
    elif len(body_terms) - query_index < 50:
        snippet = f"{' '.join(body_terms[-100:])}"
    else:
        snippet = f"...{' '.join(body_terms[query_index - 50:query_index + 50])}..."

    return snippet
