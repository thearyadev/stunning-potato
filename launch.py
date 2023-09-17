import argparse
import datetime
import inspect
import json
import logging
import os
import platform
import string
import sys
import traceback
from datetime import timedelta
from pathlib import Path

import psutil
import uvicorn
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from downloader.downloader import Downloader
from indexer.indexer import Indexer
from server.server import Server
from transcoder.transcoder import Transcoder
from util.database.database_access import DatabaseAccess


def remove_invalid_characters(input_string):
    return "".join([x for x in input_string if x in string.printable])


def filter_bytes_variables(variables):
    filtered_vars = {}
    for name, value in variables.items():
        if isinstance(value, bytes):
            continue
        if inspect.isclass(value):
            class_attrs = {}
            for attr_name, attr_value in value.__dict__.items():
                if isinstance(attr_value, bytes):
                    continue
                class_attrs[attr_name] = attr_value
            filtered_vars[name] = class_attrs
        else:
            filtered_vars[name] = value
    return filtered_vars


parser = argparse.ArgumentParser(description="pogger")
parser.add_argument(
    "--log-level",
    type=str,
    default="INFO",
    help="logging level: INFO, DEBUG, WARNING, ERROR, CRITICAL",
)
parser.add_argument(
    "--app",
    type=str,
    help="app name",
    choices=["server", "downloader", "indexer"],
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
# db.drop()
if args.flush == "True":
    db.drop()
    db.initialize(Path("./util/database/tables.sql"))
    # db.populate_demo_data()

if __name__ == "__main__":
    try:
        match args.app:
            case "server":
                db.initialize(Path("./util/database/tables.sql"))
                Server(databaseAccess=db).main_loop()
            case "downloader":
                Downloader(databaseAccess=db).main_loop()
            case "indexer":
                Indexer(databaseAccess=db).main_loop()

    except Exception as e:
        _, _, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        filename = traceback.extract_tb(tb)[-1][0]
        full_traceback = traceback.format_exc()
        local_vars = inspect.trace()[-1][0].f_locals
        global_vars = inspect.trace()[-1][0].f_globals
        class_attrs = filter_bytes_variables(local_vars)

        local_vars = {
            str(k): (str(v) if not isinstance(v, bytes) else "bytes_omitted")
            for k, v in local_vars.items()
        }
        global_vars = {
            str(k): (str(v) if not isinstance(v, bytes) else "bytes_omitted")
            for k, v in global_vars.items()
        }
        class_attrs = {
            str(k): (str(v) if not isinstance(v, bytes) else "bytes_omitted")
            for k, v in class_attrs.items()
        }

        error_type = type(e).__name__
        function_name = inspect.getframeinfo(sys._getframe(0)).function
        module_name = __name__
        timestamp = datetime.datetime.now()
        args = sys.argv
        current_directory = os.getcwd()
        platform_info = platform.platform()
        memory_usage = psutil.Process(os.getpid()).memory_info().rss

        error_report = {
            "line_number": line_number,
            "function_name": function_name,
            "module_name": module_name,
            "timestamp": str(timestamp.timestamp()),
            "error_type": error_type,
            "full_traceback": full_traceback,
            "local_vars": local_vars,
            "global_vars": global_vars,
            "class_and_func_attrs": class_attrs,
            "args": args,
            "current_directory": current_directory,
            "platform_info": platform_info,
            "memory_usage": memory_usage,
        }

        with open(
            Path(os.getenv("ERROR_REPORT_PATH")).joinpath(
                f"{error_type}-{str(timestamp.timestamp())}.json"
            ),
            "w+",
        ) as f:
            json.dump(error_report, f, indent=4, sort_keys=True)
            logging.critical(f"Error report written to {f.name}")
            raise e
