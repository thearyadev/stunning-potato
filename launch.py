import logging
from util.database.database_access import DatabaseAccess
from pathlib import Path
from uuid import UUID
from util.models.actress import ActressIn
from util.models.rating import RatingIn, Rating

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
# print(Queue)
db.initialize(Path("util/database/tables.sql"))
# print(db.insert_actress(ActressIn(name_="Scarlet Skies")))

# print(db.get_actress(uuid=UUID("0d6318a8-53c7-4594-8153-c74c1456c59a")))
db.update_rating(
    Rating(
        uuid=UUID("ae4850f7-49ee-49a2-a1f2-99f0571ebb25"),
        average=None,
        story=10,
        positions=1,
        pussy=1,
        shots=1,
        boobs=1,
        face=1,
        rearview=1,
    )
)
