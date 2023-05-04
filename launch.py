import logging
from util.database.database_access import DatabaseAccess
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


db_access = DatabaseAccess(
    "lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432"
)
# print(Queue)
db_access.initialize(Path("util/database/tables.sql"))
