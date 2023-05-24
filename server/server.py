import datetime
import inspect
import logging
import os
import pickle
import platform
import shutil
import sys
import time
import traceback
from pathlib import Path
from uuid import UUID, uuid4

import psutil
import uvicorn
from fastapi import APIRouter, FastAPI, Query
from fastapi.exception_handlers import HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from util.database.database_access import DatabaseAccess
from util.models.actress_detail import ActressDetail
from util.models.film import (
    Film,
    FilmIn,
    FilmNoBytes,
    FilmNoBytesWithAverage,
    FilmStateEnum,
)
from util.models.indexed import IndexedNoBytes
from util.models.queue import QueueIn
from util.models.rating import Rating, RatingIn

from typing import Any
import docker
from indexer.indexer import index, extract_film_id


def filter_bytes_variables(variables):
    filtered_vars = {}
    for name, value in variables.items():
        if isinstance(value, bytes):
            continue
        if inspect.isclass(value):
            class_attrs = {}
            for attr_name, attr_value in value.__dict__.items():
                if isinstance(attr_value, bytes):
                    continue
                class_attrs[attr_name] = attr_value
            filtered_vars[name] = class_attrs
        else:
            filtered_vars[name] = value
    return filtered_vars


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


class ReadCache:
    """Cache for read operations. This is used to reduce the number of database calls."""

    def __init__(self) -> None:
        self.films: list[FilmNoBytesWithAverage] = []
        self.filmsStamp: UUID = None

        self.actresses: list[ActressDetail] = []
        self.actressesStamp: UUID = None

        self.images: dict[UUID, bytes] = {}


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
        self.router.add_api_route("/v", self.serve_video, methods=["GET"])
        self.router.add_api_route("/queue_add", self.add_to_queue, methods=["POST"])
        self.router.add_api_route(
            "/downloaders", self.get_active_downloaders, methods=["GET"]
        )

        self.router.add_api_route(
            "/quwu", self.manual_queue_insertion, methods=["POST"]
        )
        self.router.add_api_route("/diagnostics", self.diagnostics, methods=["GET"])

        self.app.include_router(self.router)

        self.app.mount("/", SPAStaticFiles(directory="./server/build"), name="static")
        self.app.add_route("/", self.serve_webpage)
        # self.app.add_api_route("/api/diagnostics", self.diagnostics, methods=["GET"])
        self.cache = ReadCache()

    def main_loop(self):
        uvicorn.run(self.app, port=8000, host="0.0.0.0")

    def get_films_no_bytes_with_average(self) -> list[FilmNoBytesWithAverage]:
        """Queries all records in the films table. This is cached. If the cache is outdated, it will be refreshed.

        Returns:
            list[FilmNoBytesWithAverage]: list of FilmNoBytesWithAverage objects
        """
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
        """Gets single film from cache or database.

        Args:
            uuid (UUID, optional): uuid of film. Defaults to Query(..., description="Film UUID").

        Returns:
            FilmNoBytes | None: FilmNoBytes object
        """
        return self.db.get_single_film_no_bytes(uuid)

    def get_thumbnail(self, uuid: UUID) -> bytes:
        """Gets thumbnail from cache or database.

        Args:
            uuid (UUID): uuid of film

        Returns:
            bytes: thumbnail bytes
        """
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
        """Gets the poster. This isnt used much so it doesnt need to be cached.

        Args:
            uuid (UUID): uuid of film

        Returns:
            bytes: poster bytes
        """
        return Response(self.db.get_film_poster(uuid), media_type="image/png")

    def get_film_rating(self, uuid: UUID) -> Rating:
        """Gets rating of film.

        Args:
            uuid (UUID): uuid of film

        Returns:
            Rating: Rating object
        """
        return self.db.get_rating(uuid)

    def set_rating(self, rating: Rating) -> Rating:
        """Sets rating of film.

        Args:
            rating (Rating): Rating object

        Returns:
            Rating: Rating object
        """
        self.db.update_rating(rating)
        return self.db.get_rating(rating.uuid)

    def set_watch_status(
        self, uuid: UUID = Query(...), watch_status: bool = Query(...)
    ) -> None:
        """Sets watch status of film.

        Args:
            uuid (UUID, optional): uuid of film. Defaults to Query(...).
            watch_status (bool, optional): new watch status. Defaults to Query(...).
        """
        self.db.update_watch_status(uuid, watch_status)

    def get_all_actress_detail(self) -> list[ActressDetail]:
        """Uses ReadCache to return cached data if possible. Otherwise, refreshes cache and returns refreshed data.

        Returns:
            list[ActressDetail]: _description_
        """
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
        """deprecated"""
        total, used, free = shutil.disk_usage(os.getenv("DOWNLOAD_PATH"))
        return {
            "total": int(total / 10**9),
            "used": int(used / 10**9),
            "free": int(free / 10**9),
        }

    def delete_film(self, uuid: UUID = Query(...)) -> Response:
        """Delete a film from the database

        Args:
            uuid (UUID, optional): uuid of film. Defaults to Query(...).

        Returns:
            Response: _description_
        """
        film: Film = self.db.get_film_no_bytes(uuid)
        full_file_to_delete: Path = Path(os.getenv("DOWNLOAD_PATH")).joinpath(
            film.filename
        )
        if os.path.isfile(full_file_to_delete):
            os.remove(full_file_to_delete)
        self.db.delete_film(film.uuid)
        return Response(status_code=200)

    def diagnostics(self) -> dict[str, int | float | str | dict]:
        """Diagnostic information about the server

        Returns:
            dict[str, int | float | str | dict]: diagnostic information
        """
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
        """Returns all indexed items by count value

        Returns:
            list[IndexedNoBytes]: list of indexed items
        """
        return self.db.get_by_count_indexed_no_bytes(100)

    def get_indexed_thumbnail(self, uuid: UUID = Query(...)) -> bytes:
        """Uses cached thumbnails if available.

        Args:
            uuid (UUID, optional): uuid of indexed item. Defaults to Query(...).

        Returns:
            bytes: _description_
        """

        if uuid in self.cache.images:
            logging.info("Thumbnail found in cache. ")
            return Response(self.cache.images[uuid], media_type="image/png")
        logging.info("Thumbnail not found in cache. ")
        imageBytes: bytes = self.db.get_indexed_thumbnail(uuid)

        self.cache.images[uuid] = imageBytes
        return Response(
            self.cache.images[uuid],
            media_type="image/png",
        )

    def add_to_queue(self, queueItems: list[UUID]) -> Response:
        """Adds items to queue

        Args:
            queueItems (list[UUID]): list of uuids to add to queue

        Returns:
            Response: status
        """
        for i in queueItems:
            indexed_queue_item = self.db.get_indexed(i)

            # add rating record
            rating: Rating = self.db.insert_rating(
                RatingIn(
                    story=0, positions=0, pussy=0, shots=0, boobs=0, face=0, rearview=0
                )
            )
            # add film record
            film: Film = self.db.insert_film(
                FilmIn(
                    title=indexed_queue_item.title,
                    duration=indexed_queue_item.duration,
                    date_added=datetime.datetime.now(),  # gen cur date
                    filename=f"{uuid4().hex}.mp4",  # gen filename
                    watched=False,
                    state=FilmStateEnum.IN_QUEUE,
                    actresses=indexed_queue_item.actresses,
                    thumbnail=indexed_queue_item.thumbnail,
                    poster=indexed_queue_item.poster,
                    download_progress=0,  # default value
                    rating=rating.uuid,  # get rating uuid
                )
            )

            self.db.insert_queue(
                # url to get from             # film record uuid
                QueueIn(url=indexed_queue_item.url, film_uuid=film.uuid)
            )

        return Response(status_code=200)

    def serve_video(self, uuid: UUID = Query(...)) -> FileResponse:
        """Serves video file

        Args:
            uuid (UUID, optional): uuid of film. Defaults to Query(...).

        Returns:
            Response: video file
        """
        response = FileResponse(
            Path(os.getenv("DOWNLOAD_PATH")).joinpath(self.db.get_film(uuid).filename),
            media_type="video/mp4",
        )
        response.headers["Accept-Ranges"] = "bytes"
        return response

    def serve_webpage(self, *_) -> HTMLResponse:
        return HTMLResponse(content=open("./server/build/index.html").read())

    def get_active_downloaders(self):
        """Returns list of active downloaders

        Returns:
            list[dict[Any, Any]]: list of active downloaders
        """
        NETWORK_NAME = "stunning-potato_lewdlocale"
        try:
            results: list[dict[Any, Any]] = list()
            client = docker.from_env()
            containers = client.containers.list()
            for container in containers:
                c = container
                netAttrs = (
                    c.attrs.get("NetworkSettings").get("Networks").get(NETWORK_NAME)
                )
                if netAttrs is not None:
                    results.append(
                        {
                            "aliases": netAttrs.get("Aliases"),
                            "ip_address": netAttrs.get("IPAddress"),
                            "mac_address": netAttrs.get("MacAddress"),
                        }
                    )

            return results
        except Exception as e:
            logging.error(e)
            return []

    def manual_queue_insertion(self, urls: list[str]) -> Response:
        """Manually insert items into queue

        Args:
            urls (list[str]): list of urls to insert into queue

        Returns:
            Response: status
        """
        for url in urls:
            film_id = extract_film_id(url)
            indexed_queue_item = index(film_id)
            # add rating record
            rating: Rating = self.db.insert_rating(
                RatingIn(
                    story=0, positions=0, pussy=0, shots=0, boobs=0, face=0, rearview=0
                )
            )
            # add film record
            film: Film = self.db.insert_film(
                FilmIn(
                    title=indexed_queue_item.title,
                    duration=indexed_queue_item.duration,
                    date_added=datetime.datetime.now(),  # gen cur date
                    filename=f"{uuid4().hex}.mp4",  # gen filename
                    watched=False,
                    state=FilmStateEnum.IN_QUEUE,
                    actresses=indexed_queue_item.actresses,
                    thumbnail=indexed_queue_item.thumbnail,
                    poster=indexed_queue_item.poster,
                    download_progress=0,  # default value
                    rating=rating.uuid,  # get rating uuid
                )
            )

            self.db.insert_queue(
                # url to get from             # film record uuid
                QueueIn(url=indexed_queue_item.url, film_uuid=film.uuid)
            )
        return Response(status_code=200)
