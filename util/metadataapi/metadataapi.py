import requests
import dataclasses
from typing import Any
from rich import print
from dotenv import load_dotenv
import os


@dataclasses.dataclass
class TpdbFilmData:
    title: str
    actresses: list[str]
    thumbnail: bytes
    poster: bytes


load_dotenv()


def get_film_data(tpdb_scene_id: str) -> TpdbFilmData:
    """Get film data from TPDB.
    This function is expected to raise exceptions when there are issues.
    Checks for request completion, and data integrity
    """
    r = requests.get(
        f"https://api.metadataapi.net/scenes/{tpdb_scene_id}",
        headers={"Authorization": f"Bearer {os.environ.get('TPDB_API_TOKEN')}"},
    )
    if r.status_code == requests.status_codes.codes.NOT_FOUND:
        raise ValueError(f"Scene not found.")

    if r.status_code == requests.status_codes.codes.UNAUTHORIZED:
        raise ValueError(f"Unable to retrieve data. Invalid token. {r.status_code}")

    if r.status_code != requests.status_codes.codes.OK:
        raise ValueError(
            f"Unable to retrieve data. Status code was unexpected. {r.status_code}"
        )
    try:
        data = r.json()["data"]
    except KeyError as e:
        raise ValueError("The data appears to be malformed. Missing key 'data'")

    return TpdbFilmData(
        title=data["title"],
        actresses=get_actresses(data),
        thumbnail=get_image(data["background"]["small"]),
        poster=get_image(data["background"]["full"]),
    )


def get_image(url: str) -> bytes:
    r = requests.get(url)
    if r.status_code != requests.status_codes.codes.OK:
        raise ValueError(
            f"Unable to fetch image. {url}. Status code was unexpected. {r.status_code}"
        )
    return r.content


def get_actresses(data: dict[str, Any]) -> list[str]:
    _o = list()
    for actress in data["performers"]:
        if (
            actress["extra"]["gender"] is not None
            and actress["extra"]["gender"].lower() != "male"
        ):
            _o.append(actress["name"])
            continue

        if (
            actress["parent"]["extras"]["gender"] is not None
            and actress["parent"]["extras"]["gender"].lower() != "male"
        ):
            _o.append(actress["name"])

    return _o


def test() -> None:
    """Test the function"""

    cases = [
        ("72b28b93-ce6c-4b45-94c2-780e0813f948", 2),
        ("4d05764f-03df-4056-9e7a-3612fa83e533", 1),
        ("0100bc74-90b5-47b0-b5f4-ff0517302068", 2),
    ]
    for case in cases:
        o = get_film_data(case[0])

        if len(o.actresses) == case[1]:
            print("actresses correctly detected")


if __name__ == "__main__":
    test()
