from bs4 import BeautifulSoup
import requests
import logging
from datetime import timedelta
import json
from pathlib import Path
import urllib.parse
import re

IFRAME_BLACKLIST: list[str] = json.loads(
    Path("util/scraper/iframe_url_blacklist.json").read_text()
).get("blacklist")


def parse_url(url: str) -> str:
    """validates a url"""
    parsed: urllib.parse.ParseResult = urllib.parse.urlparse(url)
    if not parsed.scheme:
        parsed = parsed._replace(scheme="http")

    return parsed.geturl()


def get_document(url: str) -> BeautifulSoup:
    """Get document from url"""
    response = requests.get(url, headers={"Referer": "https://hqporner.com"})
    response.raise_for_status()
    document = BeautifulSoup(response.text, "html.parser")
    try:
        logging.info(f"Got document from {url}. Title is <{document.title.text}>")
    except AttributeError:
        pass
    return document


def get_film_title(document: BeautifulSoup) -> str:
    """Get film title from document"""
    return document.find("h1", class_="main-h1").text.title()


def get_film_actresses(document: BeautifulSoup) -> list[str]:
    """Get film actresses from document"""
    return [a.text for a in document.find("li", class_="fa-star-o").find_all("a")]


def get_film_duration(document: BeautifulSoup) -> timedelta:
    """Get film duration from document"""
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
    return delta


def get_iframe_source(document: BeautifulSoup) -> str:
    """Get iframe source from document"""
    iframes = document.find_all("iframe")
    for frame in iframes:
        if frame["src"] not in IFRAME_BLACKLIST:
            return parse_url(frame["src"])
    raise ValueError("No iframe found")


def get_poster(document: BeautifulSoup) -> bytes:
    """Get poster from document"""
    all_script_tags = str(document.find_all("script"))
    poster_url_search = re.search("\/\S+\.mp4", all_script_tags)
    if poster_url_search:
        poster_url = parse_url(poster_url_search.group(0))
        poster_url = urllib.parse.urljoin(poster_url, "main.jpg")
    return requests.get(poster_url).content

def get_download_url(document: BeautifulSoup) -> bytes:
    """Get download url from document"""
    all_script_tags = str(document.find_all("script"))
    download_url_search = re.search("\/\S+\.mp4", all_script_tags)
    if download_url_search:
        download_url = parse_url(download_url_search.group(0))
        download_url = urllib.parse.urljoin(download_url, "1080.mp4")
    return download_url