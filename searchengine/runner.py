from searchengine import cli, indexer


def run():
    indexer.index_pages()

    cli.handle_user()
