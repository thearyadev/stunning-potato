import sqlite3
from util.database.database_access import DatabaseAccess
from pathlib import Path
from util.models.film import FilmIn, FilmStateEnum, Film
from util.models.rating import RatingIn, Rating
import uuid
from datetime import timedelta


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


dest_db = DatabaseAccess(
    db_host="192.168.50.190",
    db_port=5433,
    db_name="lewdlocale",
    db_user="lewdlocale",
    db_password="lewdlocale",
)
dest_db.initialize(Path("./util/database/tables.sql"))
print(dest_db.get_actress_detail_all())
input()
src_db = sqlite3.connect("films.db")
src_db.row_factory = dict_factory
cur = src_db.cursor()
cur.execute("SELECT * FROM FILMS")
for i in cur.fetchall():
    rating: RatingIn = RatingIn(
        story=i["Story"],
        positions=i["Positions"],
        pussy=i["Pussy"],
        shots=i["Shots"],
        boobs=i["Boobs"],
        face=i["Face"],
        rearview=i["Rear"],
    )
    ratingIn = dest_db.insert_rating(rating)

    components: list[str] = i["Duration"].split()
    delta: timedelta = timedelta()
    for component in components:
        match component[-1]:
            case "h":
                delta += timedelta(hours=int(component[:-1]))
            case "m":
                delta += timedelta(minutes=int(component[:-1]))
            case "s":
                delta += timedelta(seconds=int(component[:-1]))

    film: FilmIn = FilmIn(
        title=i["Title"],
        duration=delta,
        date_added=i["Date"],
        filename=i["Filename"],
        watched=bool(i["WatchStatus"]),
        state=FilmStateEnum.COMPLETE,
        actresses=i["Actresses"].split(", "),
        rating=ratingIn.uuid,
        thumbnail=i["ThumbnailSmall"],
        poster=i["Thumbnail"],
        download_progress=100,
    )
    dest_db.insert_film(film)
