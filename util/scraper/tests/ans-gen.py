import sys

sys.path.append(".")  # just so i can run this from root

from indexer.indexer import build_url, extract_film_id
from util.scraper.detail_page import *
from util.scraper.document import *
from util.scraper.list_page import *

answers: dict = {}

TARGET_URL = "https://hqporner.com/"


def main():
    urls: list[str] = collect_urls(get_document(TARGET_URL))
    for url in urls:
        document = get_document(build_url(extract_film_id(url)))
        title = get_film_title(document)
        actresses = get_film_actresses(document)
        duration = get_film_duration(document)
        iframe_src = get_iframe_source(document)
        download_url = get_download_url(get_document(iframe_src))

        answers[url] = {
            "title": title,
            "actresses": actresses,
            "duration": duration.seconds,
            "iframe_src": iframe_src,
            "download_url": download_url,
        }
    with open("answers.json", "w") as f:
        json.dump(answers, f)


if __name__ == "__main__":
    main()
