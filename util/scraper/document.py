import logging

import requests
from beartype import beartype
from bs4 import BeautifulSoup


@beartype
def get_document(url: str) -> BeautifulSoup:
    """Get document from url

    Args:
        url (str): url to get document from

    Returns:
        BeautifulSoup: document
    """
    response = requests.get(url, headers={"Referer": "https://hqporner.com"})
    response.raise_for_status()
    document = BeautifulSoup(response.text, "html.parser")
    try:
        logging.info(f"Got document from {url}. Title is <{document.title.text}>")  # type: ignore
        # title may not have .text. Ignore for mypy
        # exception is caught
    except AttributeError:
        pass
    return document
