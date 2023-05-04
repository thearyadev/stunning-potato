import logging
from util.database.database_access import DatabaseAccess
from pathlib import Path
from uuid import UUID
from util.models.actress import ActressIn
from util.models.rating import RatingIn, Rating
from util.models.indexed import IndexedIn, Indexed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432")
# print(Queue)
db.initialize(Path("util/database/tables.sql"))
# print(db.insert_actress(ActressIn(name_="Scarlet Skies")))

# print(db.get_actress(uuid=UUID("0d6318a8-53c7-4594-8153-c74c1456c59a")))
db.insert_indexed(
    IndexedIn(title="Scarlet Skies Sexy Time", actresses=["Scarlet Skies", "Lacy Lennon"], thumbnail=b"this is a thumbnail", url="https://www.pornhub.com/view_video.php?viewkey=ph5f1b0b1a2b1a4")
)
