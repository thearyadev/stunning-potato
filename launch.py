import argparse
import logging
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

from downloader.downloader import Downloader
from indexer.indexer import Indexer
from server.server import Server
from util.database.database_access import DatabaseAccess

parser = argparse.ArgumentParser(description="pogger")
parser.add_argument(
    "--log-level",
    type=str,
    default="INFO",
    help="logging level: INFO, DEBUG, WARNING, ERROR, CRITICAL",
)
parser.add_argument(
    "--app", type=str, help="app name", choices=["server", "downloader", "indexer"]
)
parser.add_argument("--flush", type=str, help="flush database", default="False")
args = parser.parse_args()

load_dotenv()
logging.basicConfig(level=args.log_level)

db = DatabaseAccess(
    db_host=os.getenv("DB_HOST"),
    db_port=int(os.getenv("DB_PORT")),
    db_user=os.getenv("DB_USER"),
    db_password=os.getenv("DB_PASS"),
    db_name=os.getenv("DB_NAME"),
)
db.initialize(Path("./util/database/tables.sql"))

if args.flush == "True":
    db.drop()
    db.initialize(Path("./util/database/tables.sql"))
    db.populate_demo_data()

if __name__ == "__main__":
    match args.app:
        case "server":
            Server(databaseAccess=db).main_loop()
        case "downloader":
            Downloader(databaseAccess=db).main_loop()
        case "indexer":
            Indexer(databaseAccess=db).main_loop()
