from uuid import UUID

import uvicorn
from fastapi import APIRouter, FastAPI, Query
from fastapi.responses import Response

from util.database.database_access import DatabaseAccess
from util.models.film import FilmNoBytes, FilmNoBytesWithAverage
from util.models.rating import Rating, RatingIn
from util.models.actress_detail import ActressDetail
from util.models.indexed import IndexedNoBytes
import shutil
import os
import logging
import sys
import pickle
import time


class ReadCache:
    def __init__(self) -> None:
        self.films: list[FilmNoBytesWithAverage] = []
        self.actresses: list[ActressDetail] = []
        self.images: dict[UUID, bytes] = {}
        self.filmsStamp: UUID = None
        self.actressesStamp: UUID = None


class Server:
    def __init__(self, databaseAccess: DatabaseAccess):
        self.db = databaseAccess
        self.app = FastAPI()
        self.router = APIRouter(prefix="/api")
        self.router.add_api_route(
            "/actress_detail", self.get_all_actress_detail, methods=["GET"]
        )
        self.router.add_api_route(
            "/films", self.get_films_no_bytes_with_average, methods=["GET"]
        )
        self.router.add_api_route("/film", self.get_single_film, methods=["GET"])
        self.router.add_api_route("/thumbnail", self.get_thumbnail, methods=["GET"])
        self.router.add_api_route("/poster", self.get_poster, methods=["GET"])
        self.router.add_api_route("/rating", self.get_film_rating, methods=["GET"])
        self.router.add_api_route(
            "/watch_status", self.set_watch_status, methods=["GET"]
        )
        self.router.add_api_route("/delete", self.delete_film, methods=["GET"])
        self.router.add_api_route("/set_rating", self.set_rating, methods=["POST"])

        self.router.add_api_route("/indexed", self.get_indexed, methods=["GET"])
        self.router.add_api_route(
            "/indexed_thumbnail", self.get_indexed_thumbnail, methods=["GET"]
        )
        self.router.add_api_route(
            "/storage", self.get_available_storage, methods=["GET"]
        )

        self.router.add_api_route("/diagnostics", self.diagnostics, methods=["GET"])
        self.app.include_router(self.router)
        self.cache = ReadCache()

    def main_loop(self):
        uvicorn.run(self.app, port=8000)

    def get_films_no_bytes_with_average(self) -> list[FilmNoBytesWithAverage]:
        if self.cache.filmsStamp is None:  # first run, no stamp. Data must be outdated.
            logging.info("no stamp. Data must be outdated. :: films")
            self.cache.films = (
                self.db.get_all_films_no_bytes_with_rating_average()
            )  # refresh cache
            self.cache.filmsStamp = self.db.get_latest_commit_uuid()  # set stamp
            return self.cache.films  # return refreshed cache

        if self.cache.filmsStamp != (
            latestStamp := self.db.get_latest_commit_uuid()
        ):  # if stamp is outdated
            logging.info("Stamp is outdated. Data must be outdated. :: films")
            self.cache.films = self.db.get_all_films_no_bytes_with_rating_average()
            # refresh cache
            self.cache.filmsStamp = latestStamp  # set stamp
            return self.cache.films  # return refreshed cache
        logging.info("Stamp is up to date. Data must be up to date. :: films")
        return self.cache.films  # return cache

    def get_single_film(
        self, uuid: UUID = Query(..., description="Film UUID")
    ) -> FilmNoBytes | None:
        return self.db.get_single_film_no_bytes(uuid)

    def get_thumbnail(self, uuid: UUID) -> bytes:
        if uuid in self.cache.images:
            logging.info("Thumbnail found in cache. ")
            return Response(self.cache.images[uuid], media_type="image/png")
        logging.info("Thumbnail not found in cache. ")
        imageBytes: bytes = self.db.get_film_thumbnail(uuid)

        self.cache.images[uuid] = imageBytes
        return Response(
            imageBytes,
            media_type="image/png",
        )

    def get_poster(self, uuid: UUID) -> bytes:
        return Response(self.db.get_film_poster(uuid), media_type="image/png")

    def get_film_rating(self, uuid: UUID) -> Rating:
        return self.db.get_rating(uuid)

    def set_rating(self, rating: Rating) -> Rating:
        self.db.update_rating(rating)
        return self.db.get_rating(rating.uuid)

    def set_watch_status(
        self, uuid: UUID = Query(...), watch_status: bool = Query(...)
    ) -> None:
        self.db.update_watch_status(uuid, watch_status)

    def get_all_actress_detail(self) -> list[ActressDetail]:
        if (
            self.cache.actressesStamp is None
        ):  # first run, no stamp. Data must be outdated.
            logging.info("no stamp. Data must be outdated. :: actresses")
            self.cache.actresses = self.db.get_actress_detail_all()  # refresh cache
            self.cache.actressesStamp = self.db.get_latest_commit_uuid()  # set stamp
            return self.cache.actresses  # return refreshed cache

        if self.cache.actressesStamp != (
            latestStamp := self.db.get_latest_commit_uuid()
        ):  # if stamp is outdated
            logging.info("Stamp is outdated. Data must be outdated. :: actresses")
            self.cache.actresses = self.db.get_actress_detail_all()
            # refresh cache
            self.cache.actressesStamp = latestStamp  # set stamp
            return self.cache.actresses  # return refreshed cache
        logging.info("Stamp is up to date. Data must be up to date. : actresses")
        return self.cache.actresses  # return cache

    def get_available_storage(self) -> dict[str, int]:
        total, used, free = shutil.disk_usage(os.getenv("DOWNLOAD_PATH"))
        return {
            "total": int(total / 10**9),
            "used": int(used / 10**9),
            "free": int(free / 10**9),
        }

    def delete_film(self, uuid: UUID = Query(...)) -> Response:
        self.db.delete_film(uuid)
        return Response(status_code=200)

    def diagnostics(self) -> dict[str, int | float | str | dict]:
        total, used, free = shutil.disk_usage(os.getenv("DOWNLOAD_PATH"))
        start_time = time.perf_counter()
        self.db.get_all_films_no_bytes_with_rating_average()
        end_time = time.perf_counter()

        return {
            "cache_size": sys.getsizeof(pickle.dumps(self.cache)),
            "disk": {
                "total": int(total / 10**9),
                "used": int(used / 10**9),
                "free": int(free / 10**9),
            },
            "database": {
                "size": self.db.get_database_size(),
                "query_time": end_time - start_time,
            },
        }

    def get_indexed(self) -> list[IndexedNoBytes]:
        return self.db.get_by_count_indexed_no_bytes(100)

    def get_indexed_thumbnail(self, uuid: UUID = Query(...)) -> bytes:
        if uuid in self.cache.images:
            logging.info("Thumbnail found in cache. ")
            return Response(self.cache.images[uuid], media_type="image/png")
        logging.info("Thumbnail not found in cache. ")
        imageBytes: bytes = self.db.get_indexed_thumbnail(uuid)

        self.cache.images[uuid] = imageBytes
        return Response(
            imageBytes,
            media_type="image/png",
        )
