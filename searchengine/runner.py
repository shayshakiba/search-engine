from searchengine import gui, indexer


def run():
    indexer.index_pages()

    app = gui.App()
    app.mainloop()
