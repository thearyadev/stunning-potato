from uuid import UUID

import uvicorn
from fastapi import APIRouter, FastAPI, Query
from fastapi.responses import Response

from util.database.database_access import DatabaseAccess
from util.models.film import FilmNoBytes, FilmNoBytesWithAverage
from util.models.rating import Rating, RatingIn


class Server:
    def __init__(self, databaseAccess: DatabaseAccess):
        self.db = databaseAccess
        self.app = FastAPI()
        self.router = APIRouter(prefix="/api")
        self.router.add_api_route("/actresses", self.get_actresses, methods=["GET"])
        self.router.add_api_route(
            "/films", self.get_films_no_bytes_with_average, methods=["GET"]
        )
        self.router.add_api_route("/film", self.get_single_film, methods=["GET"])
        self.router.add_api_route("/thumbnail", self.get_thumbnail, methods=["GET"])
        self.router.add_api_route("/poster", self.get_poster, methods=["GET"])
        self.router.add_api_route("/rating", self.get_film_rating, methods=["GET"])

        self.router.add_api_route("/set_rating", self.set_rating, methods=["POST"])

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
