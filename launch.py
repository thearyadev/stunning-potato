import logging
from datetime import date, timedelta
from pathlib import Path
from uuid import UUID

from rich.logging import RichHandler

from util.database.database_access import DatabaseAccess
from util.models.actress import ActressIn
from util.models.film import Film, FilmIn, FilmStateEnum
from util.models.indexed import Indexed, IndexedIn
from util.models.queue import Queue, QueueIn
from util.models.rating import Rating, RatingIn

logging.basicConfig(
    level=logging.INFO,
    format="\[%(module)s.%(funcName)s] %(message)s",
    handlers=[RichHandler(markup=True)],
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
db.initialize(Path("util/database/tables.sql"))

# db.insert_queue(
#     QueueIn(
#         url="this is a url3",
#         film_uuid=UUID("e5c45cd7-2d8f-4aff-a16a-96a766ec4304")
#     )
# )
#


# print(db.get_and_pop_queue())
# db.drop()
