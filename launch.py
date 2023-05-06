import logging
from util.scraper.document import (
    get_document,
    get_film_title,
    get_film_actresses,
    get_film_duration,
    get_iframe_source,
    get_poster,
    get_download_url,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(module)s.%(funcName)s] %(message)s",
)
doc = get_document("https://hqporner.com/hdporn/111444-natural_at_making_people_happy.html")
title = get_film_title(doc)
actresses = get_film_actresses(doc)
duration = get_film_duration(doc)
iframe_src = get_iframe_source(doc)
iframe_doc = get_document(iframe_src)
poster = get_poster(iframe_doc)
video_url = get_download_url(iframe_doc)
print(video_url)


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