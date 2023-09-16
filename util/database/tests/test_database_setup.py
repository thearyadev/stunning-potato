import os
from pathlib import Path

import dotenv
import pytest

from util.database.database_access import DatabaseAccess

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def dba() -> DatabaseAccess:
    assert (
        os.getenv("DB_NAME") != "lewdlocale"
    )  # This is a safety check to make sure we don't accidentally run tests on the production database
    dba = DatabaseAccess(
        db_name=os.getenv("DB_NAME"),
        db_user=os.getenv("DB_USER"),
        db_password=os.getenv("DB_PASS"),
        db_host=os.getenv("DB_HOST"),
        db_port=int(os.getenv("DB_PORT")),
    )
    return dba


@pytest.mark.order(0)
def test_database_connection(dba: DatabaseAccess):
    assert dba.connection_pool


@pytest.mark.order(1)
def test_flush(dba: DatabaseAccess):
    dba.drop()


@pytest.mark.order(2)
def test_database_initialization(dba: DatabaseAccess):
    dba.initialize(Path("./util/database/tables.sql"))


@pytest.mark.order(3)
def test_populate_demo_data(dba: DatabaseAccess):
    dba.populate_demo_data(count=10)
