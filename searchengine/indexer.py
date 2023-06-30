import xml.etree.ElementTree as et
import zlib

from searchengine import indexes, pages
from searchengine.page import Page, ParsedContent


PAGE_REPOSITORY_FILE_PATH = 'data/page_repository.xml'


def index_pages() -> None:
    xml_root = et.parse(PAGE_REPOSITORY_FILE_PATH).getroot()
    for page_element in xml_root.iterfind('page'):
        page = _load_page(page_element)

        pages.add(page)

        indexes.index_page(page)


def _load_page(page_element: et.Element) -> Page:
    id = int(page_element.attrib['id'])

    url = bytes.fromhex(page_element[0].text).decode()

    title = bytes.fromhex(page_element[1].text).decode()

    compressed_body = bytes.fromhex(page_element[2].text)
    body = zlib.decompress(compressed_body).decode()

    return Page(id, url, ParsedContent(title, body))
