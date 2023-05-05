import logging
from util.database.database_access import DatabaseAccess
from pathlib import Path
from uuid import UUID
from util.models.actress import ActressIn
from util.models.rating import RatingIn, Rating
from util.models.indexed import IndexedIn, Indexed
from rich.logging import RichHandler
from util.models.film import FilmIn, Film, FilmStateEnum
from datetime import timedelta, date

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    handlers=[RichHandler(markup=True)],
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
db.initialize(Path("util/database/tables.sql"))

db.get_film_no_bytes(uuid=UUID("e5c45cd7-2d8f-4aff-a16a-96a766ec4304"))

# 