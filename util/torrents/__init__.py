from torrentool.api import Torrent


def get_video_file_list(torrent_file_contents: bytes) -> list[str]:
    return [
        f.name
        for f in Torrent.from_string(torrent_file_contents).files
        if f.name.endswith("mp4") or f.name.endswith("mkv")
    ]
