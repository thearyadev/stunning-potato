from bs4 import BeautifulSoup
from beartype import beartype


@beartype
def collect_urls(document: BeautifulSoup) -> list[str]:
    """
    Collects all urls from the first page of the site
    """
    urls = []
    content_boxes = document.find_all("div", class_="6u")

    for box in content_boxes:
        urls.append(box.find("a", href=True, class_="featured")['href'])
    return urls
