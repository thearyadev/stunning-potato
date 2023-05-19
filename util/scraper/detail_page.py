import json
import logging
import re
import urllib.parse
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import requests
from beartype import beartype
from bs4 import BeautifulSoup
from PIL import Image

IFRAME_BLACKLIST: list[str] = json.loads(
    Path("util/scraper/iframe_url_blacklist.json").read_text()
).get("blacklist")


@beartype
def parse_url(url: str) -> str:
    """Parse url and return url with scheme if missing

    Args:
        url (str): url to parse

    Returns:
        str: parsed url
    """
    parsed: urllib.parse.ParseResult = urllib.parse.urlparse(url)
    if not parsed.scheme:
        parsed = parsed._replace(scheme="http")

    return parsed.geturl()


@beartype
def get_film_title(document: BeautifulSoup) -> str:
    """Get film title from document. Document MUST be hqporner detail page

    Args:
        document (BeautifulSoup): document to parse

    Returns:
        str: film title
    """
    return document.find("h1", class_="main-h1").text.title().strip()


@beartype
def get_film_actresses(document: BeautifulSoup) -> list[str]:
    """Get film actresses from document. Document MUST be hqporner detail page

    Args:
        document (BeautifulSoup): document to parse

    Returns:
        list[str]:  actresses
    """
    actresses: list[str] = [
        a.text for a in document.find("li", class_="fa-star-o").find_all("a")
    ]
    logging.info(f"Parsed Film Actresses {actresses}")
    return actresses


@beartype
def get_film_duration(document: BeautifulSoup) -> timedelta:
    """Get film duration from document. Document MUST be hqporner detail page

    Args:
        document (BeautifulSoup): document to parse

    Returns:
        timedelta: film duration
    """
    abc = str(document)

    time_text: str = document.find("li", class_="fa-clock-o").text
    components: list[str] = time_text.split()
    delta: timedelta = timedelta()
    for component in components:
        match component[-1]:
            case "h":
                delta += timedelta(hours=int(component[:-1]))
            case "m":
                delta += timedelta(minutes=int(component[:-1]))
            case "s":
                delta += timedelta(seconds=int(component[:-1]))
    logging.info(f"Parsed Film Duration {time_text} to {delta}")
    return delta


@beartype
def get_iframe_source(document: BeautifulSoup) -> str:
    """Get iframe source from document. Document MUST be hqporner detail page

    Args:
        document (BeautifulSoup): _description_

    Raises:
        ValueError: If no iframe found

    Returns:
        str: iframe source
    """
    iframes = document.find_all("iframe")
    for frame in iframes:
        if frame["src"] not in IFRAME_BLACKLIST:
            url: str = parse_url(frame["src"])
            logging.info(f"Found iframe source {url}")
            return url
    raise ValueError("No iframe found")


@beartype
def get_poster(document: BeautifulSoup) -> bytes:
    """Get poster from document, Document MUST be iframe document

    Args:
        document (BeautifulSoup): iframe document

    Returns:
        bytes: poster
    """
    all_script_tags = str(document.find_all("script"))
    poster_url_search = re.search("\/\S+\.mp4", all_script_tags)
    if poster_url_search:
        poster_url = parse_url(poster_url_search.group(0))
        poster_url = urllib.parse.urljoin(poster_url, "main.jpg")
    logging.info(f"Poster url found {poster_url}... Downloading.")
    return requests.get(poster_url).content


@beartype
def get_download_url(document: BeautifulSoup) -> str:
    """Get download url from document. Document MUST be iframe document

    Args:
        document (BeautifulSoup): iframe document

    Returns:
        str: download url
    """
    all_script_tags = str(document.find_all("script"))
    download_url_search = re.search("\/\S+\.mp4", all_script_tags)
    if download_url_search:
        download_url = parse_url(download_url_search.group(0))
        download_url = urllib.parse.urljoin(download_url, "1080.mp4")
    logging.info(f"Download url found {download_url}")
    return download_url


@beartype
def generate_thumbnail(poster: bytes) -> bytes:
    """Generate thumbnail from poster

    Args:
        poster (bytes): poster

    Returns:
        bytes: thumbnail
    """
    with BytesIO(poster) as f:
        image = Image.open(f)
        image.thumbnail((400, 225))
        thumbnail_buffer = BytesIO()
        image.save(thumbnail_buffer, "PNG")
        logging.info("Thumbnail generated")
        return thumbnail_buffer.getvalue()
