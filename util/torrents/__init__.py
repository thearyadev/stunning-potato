import qbittorrent
import os

from dotenv import load_dotenv

load_dotenv()


def get_all_unimported_torrents() -> list[str]:
    """Returns a list of all non-imported torrents"""
    client = qbittorrent.Client(os.environ.get("QBITTORRENT_HOST"))
    client.login(
        os.environ.get("QBITTORRENT_USERNAME"), os.environ.get("QBITTORRENT_PASSWORD")
    )
    torrents = client.torrents(
        tag=os.environ.get("TORRENT_DEFAULT_TAG")
    )  # all relevant torrents should have this tag.
    return torrents


if __name__ == "__main__":
    print(get_all_unimported_torrents())
