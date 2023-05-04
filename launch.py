import logging
from util.database.database_access import DatabaseAccess
from pathlib import Path
from uuid import UUID
from util.models.actress import ActressIn
from util.models.rating import RatingIn, Rating
from util.models.indexed import IndexedIn, Indexed
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        RichHandler(markup=True)
    ]
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
# print(Queue)
db.initialize(Path("util/database/tables.sql"))
# print(db.insert_actress(ActressIn(name_="Scarlet Skies")))

# print(db.get_actress(uuid=UUID("0d6318a8-53c7-4594-8153-c74c1456c59a")))
print(db.get_indexed(uuid=UUID("fcea7a03-e33c-4750-8d89-15a5a2917e41")))