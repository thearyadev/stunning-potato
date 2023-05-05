import logging

from rich.logging import RichHandler


logging.basicConfig(
    level=logging.CRITICAL,
    format="\[%(module)s.%(funcName)s] %(message)s",
    # handlers=[RichHandler(markup=True)],
)


"""
Scraper

- detail page scraper
    - get document
    - get title
    - get actresses
    - get thumbnail ( from poster )
    - get download url
    - get iframe url
    - get poster
- list page scraper
    - all urls on a page

"""