import logging
from util.database.database_access import DatabaseAccess
from pathlib import Path
from uuid import UUID
from util.models.actress import ActressIn
from util.models.rating import RatingIn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
# print(Queue)
db.initialize(Path("util/database/tables.sql"))
# print(db.insert_actress(ActressIn(name_="Scarlet Skies")))

# print(db.get_actress(uuid=UUID("0d6318a8-53c7-4594-8153-c74c1456c59a")))
db.insert_rating(
    RatingIn(
        story=1, 
        positions=0,
        pussy=5,
        shots=6,
        boobs=6,
        face=9, 
        rearview=10
    )
)