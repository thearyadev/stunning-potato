import argparse
from indexer.indexer import Indexer
from util.database.database_access import DatabaseAccess
from pathlib import Path
import logging

parser = argparse.ArgumentParser(description='pogger')
parser.add_argument(
    "--log-level", type=str, default="INFO", help="logging level: INFO, DEBUG, WARNING, ERROR, CRITICAL"
)
parser.add_argument("--app", type=str, help="app name", choices=["server", "downloader", "indexer"])
parser.add_argument("--flush", type=str, help="flush database", default="True")
args = parser.parse_args()

logging.basicConfig(level=args.log_level)


db = DatabaseAccess("lewdlocale", "lewdlocale", "lewdlocale", "localhost", 5432)
db.initialize(Path("./util/database/tables.sql"))

if args.flush == "True":
    db.drop()
    db.initialize(Path("./util/database/tables.sql"))



match args.app:
    case "server":
        exit()
    case "downloader":
        exit()
    case "indexer":
        indexer = Indexer(databaseAccess=db)
