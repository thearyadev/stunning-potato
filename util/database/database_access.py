import psycopg2
from pathlib import Path


class DatabaseAccess:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
        )

    def initialize(self, sql_path: Path):
        with open(sql_path, "r") as sql_file, self.connection.cursor() as cursor:
            cursor.execute(sql_file.read())
            self.connection.commit()

if __name__ == "__main__":
    db_access = DatabaseAccess(
        "lewdlocale", "lewdlocale", "lewdlocale", "localhost", "5432"
    )
    db_access.initialize(Path("util/database/tables.sql"))
