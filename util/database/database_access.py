import psycopg2
from pathlib import Path
import logging
from util.models.film_actress_rating import FilmActressRating
from util.models.actress import ActressIn, Actress
from util.models.film import FilmIn, Film
from util.models.indexed import IndexedIn, Indexed
from util.models.queue import QueueIn, Queue


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
        logging.info("Connected to database")

    def initialize(self, sql_path: Path):
        with open(sql_path, "r") as sql_file, self.connection.cursor() as cursor:
            cursor.execute(sql_file.read())
            self.connection.commit()
        logging.info("Initialized database")

    ## ACTRESS
    def insert_actress(self, actress: ActressIn) -> Actress:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO actress (name_) VALUES (%s) RETURN uuid",
                (actress.name_),
            )
            actress_inserted: Actress = Actress(uuid=cursor.fetchone()[0], name_=actress.name_)
            self.connection.commit()
        logging.info(f"Inserted actress {actress_inserted}")