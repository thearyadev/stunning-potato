import logging
from datetime import date, timedelta
from pathlib import Path
from uuid import UUID

from rich.logging import RichHandler

from util.database.database_access import DatabaseAccess
from util.models.film import Film, FilmIn, FilmStateEnum, FilmNoBytes, FilmNoBytesWithAverage
from util.models.indexed import Indexed, IndexedIn
from util.models.queue import Queue, QueueIn
from util.models.rating import Rating, RatingIn
import time

logging.basicConfig(
    level=logging.CRITICAL,
    format="\[%(module)s.%(funcName)s] %(message)s",
    # handlers=[RichHandler(markup=True)],
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
db.initialize(Path("util/database/tables.sql"))
# db.drop()
# db.initialize(Path("util/database/tables.sql"))
# db.populate_demo_data()
s= time.perf_counter()
data: list[FilmNoBytesWithAverage] = db.get_all_films_no_bytes_with_rating_average()



for i in data:
    db.get_rating(i.rating)

e = time.perf_counter()
print(f"Time: {e-s}")
"""

list_view: title, date, actresses, rating, state

1. get all film_actress_rating
2. for each entry, get the filmNoBytes, Actress Array, Rating Object


"""
