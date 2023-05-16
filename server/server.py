from uuid import UUID

import uvicorn
from fastapi import APIRouter, FastAPI, Query
from fastapi.responses import Response

from util.database.database_access import DatabaseAccess
from util.models.film import FilmNoBytes, FilmNoBytesWithAverage
from util.models.rating import Rating, RatingIn
from util.models.actress_detail import ActressDetail
import shutil
import os


class Server:
    def __init__(self, databaseAccess: DatabaseAccess):
        self.db = databaseAccess
        self.app = FastAPI()
        self.router = APIRouter(prefix="/api")
        self.router.add_api_route("/actresses", self.get_actresses, methods=["GET"])
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

        self.router.add_api_route("/set_rating", self.set_rating, methods=["POST"])

        self.router.add_api_route(
            "/storage", self.get_available_storage, methods=["GET"]
        )
        self.app.include_router(self.router)

    def main_loop(self):
        uvicorn.run(self.app, port=8000)

    def get_actresses(self) -> list[str]:
        return self.db.get_all_actresses()

    def get_films_no_bytes_with_average(self) -> list[FilmNoBytesWithAverage]:
        return self.db.get_all_films_no_bytes_with_rating_average()

    def get_single_film(
        self, uuid: UUID = Query(..., description="Film UUID")
    ) -> FilmNoBytes:
        return self.db.get_single_film_no_bytes(uuid)

    def get_thumbnail(self, uuid: UUID) -> bytes:
        return Response(
            self.db.get_film_thumbnail(uuid),
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
        return self.db.get_actress_detail_all()

    def get_available_storage(self) -> dict[str, int]:
        total, used, free = shutil.disk_usage(os.getenv("DOWNLOAD_PATH"))
        return {
            "total": int(total / 10**9),
            "used": int(used / 10**9),
            "free": int(free / 10**9),
        }
