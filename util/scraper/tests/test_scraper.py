import json
import pytest

from util.scraper.detail_page import *
from util.scraper.document import *
from util.scraper.list_page import *

from indexer.indexer import build_url, extract_film_id


with open("./util/scraper/tests/answers.json", "r") as f:
    data = json.load(f)

    for _, url_data in data.items():
        url_data["duration"] = timedelta(seconds=url_data["duration"])
        url_data["document"] = None
        url_data["iframe_document"] = None
        url_data["iframe_source"] = None


def test_document():
    for url, url_data in data.items():
        document = get_document(build_url(extract_film_id(url)))
        assert document
        url_data[
            "document"
        ] = document  # populate data dict with document, used in future tests


def test_get_iframe_source():
    for _, url_data in data.items():
        assert url_data["document"]
        iframe_source = get_iframe_source(url_data["document"])
        assert "mydaddy" in iframe_source
        url_data["iframe_source"] = iframe_source


def test_get_iframe_document():
    for _, url_data in data.items():
        assert url_data["iframe_source"]
        iframe_document = get_document(url_data["iframe_source"])
        assert iframe_document
        url_data["iframe_document"] = iframe_document  # used in future tests

def test_get_film_title():
    for _, url_data in data.items():
        assert url_data["document"]
        assert get_film_title(url_data["document"]) == url_data["title"]

def test_get_film_duration():
    for _, url_data in data.items():
        assert url_data["document"]
        assert get_film_duration(url_data["document"]) == url_data["duration"]

def test_get_film_actresses():
    for _, url_data in data.items():
        assert url_data["document"]
        assert get_film_actresses(url_data["document"]) == url_data["actresses"]