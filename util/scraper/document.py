from bs4 import BeautifulSoup
import requests
import logging
from beartype import beartype

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
        logging.info(f"Got document from {url}. Title is <{document.title.text}>")
    except AttributeError:
        pass
    return document