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
from util.models.queue import QueueIn, Queue

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
