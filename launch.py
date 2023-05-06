# import argparse
# parser = argparse.ArgumentParser(description='pogger')
# parser.add_argument(
#     "--log-level", type=str, default="INFO", help="logging level: INFO, DEBUG, WARNING, ERROR, CRITICAL"
# )
# parser.add_argument("--app", type=str, help="app name", choices=["server", "downloader", "indexer"])
# args = parser.parse_args()
# print(args)



from indexer.indexer import Indexer
from util.database.database_access import DatabaseAccess
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", 5432)
db.drop()
db.initialize(Path("util/database/tables.sql"))
db.populate_demo_data()
indexer = Indexer(databaseAccess=db)
indexer.main_loop()

