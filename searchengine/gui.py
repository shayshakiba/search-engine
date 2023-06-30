from searchengine import query_engine
from searchengine.page import Page
import customtkinter as ctk
import math
import time


class ResultWindow(ctk.CTkToplevel):
    def __init__(self, query: str, response_time: float, results: list[Page]):
        super().__init__()
        self.query = query
        self.response_time = response_time
        self.results = results
        self.number_of_results = len(self.results)

        self.current_page_number = 0
        self.max_page_number = math.ceil(self.number_of_results / 3) - 1

        self.title('Results')

        self.bind('<Left>', lambda event: self._display_previous_page())
        self.bind('<Right>', lambda event: self._display_next_page())

        self._display_results_window()

    def _display_results_window(self):
        self.minsize(900, 900)
        self.maxsize(900, 900)

        self.columnconfigure(0, weight=1)

        if self.number_of_results == 0:
            self.no_results_label = ctk.CTkLabel(self, text="No results found!").grid(
                row=0, column=0, padx=0, pady=10)
            return

        self.results_label = ctk.CTkLabel(self, text=f'{self.number_of_results} results found! ({self.response_time:0.3f} seconds) Page {self.current_page_number + 1}', padx=10, pady=10).grid(
            row=0, column=0, padx=10, pady=10, sticky='ew')

        self.widgets = []
        last_unused_row = 1

        for result in self._get_next_three_results():
            title_label = ctk.CTkLabel(self, text=f'{result.parsed_content.title}', justify='left', wraplength=800, font=(
                'Ariel', 13, 'bold'), bg_color='#1f6ba6')
            title_label.grid(row=last_unused_row, column=0,
                             padx=10, pady=10, sticky='ew')

            url_label = ctk.CTkLabel(self, text=f'{result.url}', justify='left', wraplength=800, font=(
                'Ariel', 10, 'italic'))
            url_label.grid(row=last_unused_row + 1,
                           column=0, padx=10, pady=10, sticky='ew')

            body_label = ctk.CTkLabel(self, text=f'{self._get_body_snippet(result.parsed_content.body)}', justify='left', wraplength=800, font=(
                'Ariel', 11))
            body_label.grid(row=last_unused_row + 2, column=0,
                            padx=10, pady=(0, 20), sticky='ew')

            last_unused_row += 3

            self.widgets.append(title_label)
            self.widgets.append(url_label)
            self.widgets.append(body_label)

            if self.current_page_number != 0:
                previous_button = ctk.CTkButton(
                    self, text='Previous', command=self._display_previous_page)
                previous_button.grid(row=last_unused_row,
                                     column=0, padx=20, pady=20, sticky='ew')

                self.widgets.append(previous_button)

            if self.current_page_number != self.max_page_number:
                next_button = ctk.CTkButton(
                    self, text='Next', command=self._display_next_page)
                next_button.grid(row=last_unused_row + 1,
                                 column=0, padx=20, sticky='ew')

                self.widgets.append(next_button)

    def _clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()

    def _display_previous_page(self):
        self._clear_widgets()

        if self.current_page_number != 0:
            self.current_page_number -= 1
        self._display_results_window()

    def _display_next_page(self):
        self._clear_widgets()

        if self.current_page_number != self.max_page_number:
            self.current_page_number += 1
        self._display_results_window()

    def _get_next_three_results(self) -> list[Page]:
        return self.results[3 * self.current_page_number:3 * (self.current_page_number + 1)]

    def _get_body_snippet(self, body: str) -> str:
        first_query_term = self.query.split()[0]
        body_terms = body.split()

        if first_query_term in body:
            query_index = body_terms.index(first_query_term)
        else:
            query_index = None

        if len(body_terms) < 50:
            snippet = ' '.join(body_terms)
        elif query_index is None or query_index < 25:
            snippet = f"{' '.join(body_terms[0:50])}..."
        elif len(body_terms) - query_index < 25:
            snippet = f"{' '.join(body_terms[-50:])}"
        else:
            snippet = f"...{' '.join(body_terms[query_index - 25:query_index + 25])}..."

        return snippet


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Search Engine')

        self._display_search_window()

    def _display_search_window(self):
        self.minsize(450, 125)
        self.maxsize(900, 125)

        self.columnconfigure(0, weight=1)

        self.bind('<Return>', lambda event: self._handle_query())

        self.query_entry = ctk.CTkEntry(self, placeholder_text='Query')
        self.query_entry.grid(row=0, column=0, padx=20,
                              pady=(20, 0), sticky='ew')

        self.search_button = ctk.CTkButton(
            self, text='Search', command=self._handle_query)
        self.search_button.grid(row=1, column=0, padx=20, pady=20, sticky='ew')

    def _handle_query(self):
        query = self.query_entry.get().strip()
        self.query_entry.delete(0, len(query))

        if not query:
            return

        start_time = time.perf_counter()
        results = query_engine.handle_query(query)
        finish_time = time.perf_counter()

        self.results_window = ResultWindow(
            query, finish_time - start_time, results)
