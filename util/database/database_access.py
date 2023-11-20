import logging
import os
import random
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import UUID

import psycopg2
from beartype import beartype
from psycopg2 import pool
from psycopg2.extras import DictCursor, UUID_adapter, register_uuid

from util.models.actress_detail import ActressDetail
from util.models.film import (
    Film,
    FilmIn,
    FilmNoBytes,
    FilmNoBytesWithAverage,
    FilmStateEnum,
)
from util.models.indexed import Indexed, IndexedIn, IndexedNoBytes
from util.models.queue import Queue, QueueIn
from util.models.rating import Rating, RatingIn

MAX_RETRIES = 10
RETRY_INTERVAL = 3


@beartype
class DatabaseAccess:
    """Connection to PostgreSQL database tools"""

    def __init__(
        self,
        db_name: str,
        db_user: str,
        db_password: str,
        db_host: str,
        db_port: int,
        max_connections: int = 15,
        min_connections: int = 1,
    ):
        self.db_name = db_name  # db connection creds
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.min_connections = min_connections  # for connection pool
        self.max_connections = max_connections
        register_uuid()  # allows use of UUID objects in psycopg2
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.connection_pool = pool.SimpleConnectionPool(
                    host=self.db_host,
                    port=self.db_port,
                    dbname=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    minconn=self.min_connections,
                    maxconn=self.max_connections,
                )
                break
            except psycopg2.OperationalError as e:
                logging.warning(
                    f"Attempt {attempt} of {MAX_RETRIES} to connect to database failed. Retrying in {RETRY_INTERVAL} seconds with credentials: {self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}"
                )
                time.sleep(RETRY_INTERVAL)
        else:
            logging.critical(
                f"Failed to connect to database after {MAX_RETRIES} attempts. Exiting."
            )
            exit(1)

        logging.info("Connected to database")

    def initialize(self, sql_path: Path) -> None:
        """Creates all the tables as defined in a .sql file

        Args:
            sql_path (Path): path to sql file
        """
        connection = self.connection_pool.getconn()
        with open(sql_path, "r") as sql_file, connection.cursor() as cursor:
            cursor.execute(sql_file.read())
            connection.commit()
        self.connection_pool.putconn(connection)
        logging.info("Initialized database")

    def get_all_actresses(self) -> list[str]:
        """Gets all actresses from the database

        Returns:
            list[Actress]: list of actress out objects
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT unnest(actresses) as name FROM film")
            raw_data_queried: list[tuple[str]] = cursor.fetchall()
            actresses: list[str] = [actress[0] for actress in raw_data_queried]
        self.connection_pool.putconn(connection)
        return actresses

    ## RATING

    def insert_rating(self, rating: RatingIn) -> Rating:
        """Insert a rating to the database

        Args:
            rating (RatingIn): Rating in object; no uuid; no average

        Returns:
            Rating: Rating out, with uuid and average. Average will be none.
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO rating ( story, positions, pussy, shots, boobs, face, rearview) VALUES ( %s, %s, %s, %s, %s, %s, %s) RETURNING uuid, average",
                (
                    rating.story,
                    rating.positions,
                    rating.pussy,
                    rating.shots,
                    rating.boobs,
                    rating.face,
                    rating.rearview,
                ),
            )
            # contains a tuple of uuid and average
            raw_data_queried: tuple[str] = cursor.fetchone()
            rating_inserted: Rating = Rating(
                uuid=raw_data_queried[0], average=raw_data_queried[1], **rating.__dict__
            )
            connection.commit()
        self.connection_pool.putconn(connection)

        logging.info(f"Inserted rating {rating_inserted}")
        return rating_inserted

    def get_rating(self, uuid: UUID) -> Rating | None:
        """Gets a rating record given the ratings uuid

        Args:
            uuid (UUID): ratings uuid

        Returns:
            Rating | None: returns none if no rating is found
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM rating WHERE uuid = %s", (str(uuid),))
            if (query_result := cursor.fetchone()) is not None:
                rating: Rating = Rating(**query_result)
            else:
                rating: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved Rating {rating}")
        self.connection_pool.putconn(connection)
        return rating

    def update_rating(self, rating: Rating) -> Rating:
        """Updates a rating record in the database

        Args:
            rating (Rating): Rating object with uuid and average (average is ignored)

        Returns:
            Rating: Rating object with uuid and average (av is ignored)
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE rating SET story = %s, positions = %s, pussy = %s, shots = %s, boobs = %s, face = %s, rearview = %s WHERE uuid = %s",
                (
                    rating.story,
                    rating.positions,
                    rating.pussy,
                    rating.shots,
                    rating.boobs,
                    rating.face,
                    rating.rearview,
                    rating.uuid,
                ),
            )
            connection.commit()
        logging.info(f"Updated Rating {rating}")
        self.connection_pool.putconn(connection)

        return rating

    ## INDEXED
    def insert_indexed(self, indexed: IndexedIn) -> Indexed | None:
        """Inserts an indexed entry

        Args:
            indexed (IndexedIn): indexed in object

        Returns:
            Indexed: indexed out, includes uuid
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO indexed (title, actresses, thumbnail, poster, url, film_id, duration) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING uuid",
                (
                    indexed.title,
                    indexed.actresses,
                    indexed.thumbnail,
                    indexed.poster,
                    indexed.url,
                    indexed.film_id,
                    indexed.duration,
                ),
            )
            logging.info(f"Inserted indexed {indexed}")
            indexed_inserted: Indexed = Indexed(
                uuid=cursor.fetchone()[0], **indexed.__dict__
            )
            connection.commit()
        self.connection_pool.putconn(connection)
        return indexed_inserted

    def get_indexed(self, uuid: UUID) -> Indexed | None:
        """Given a indexed uuid, returns the indexed object

        Args:
            uuid (UUID): indexed item uuid

        Returns:
            Indexed: indexed item, uuid included
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM indexed WHERE uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                indexed: Indexed = Indexed(**query_result)
            else:
                indexed: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved indexed {indexed}")
        self.connection_pool.putconn(connection)
        return indexed

    def get_indexed_no_bytes(self, uuid: UUID) -> IndexedNoBytes | None:
        """Given a indexed uuid, returns the indexed object

        Args:
            uuid (UUID): indexed item uuid

        Returns:
            Indexed: indexed item, uuid included
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, title, actresses, url, film_id, duration FROM indexed WHERE uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                indexed: IndexedNoBytes = IndexedNoBytes(**query_result)
            else:
                indexed: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved indexed {indexed}")
        self.connection_pool.putconn(connection)
        return indexed

    def is_indexed(self, film_id) -> bool:
        """Checks if a film_id is already indexed

        Args:
            film_id (_type_): film id to check

        Returns:
            bool: result
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT uuid, title, actresses, url, duration FROM indexed WHERE film_id = %s",
                (film_id,),
            )
            result: bool = bool(cursor.fetchone())
        self.connection_pool.putconn(connection)
        return result

    def get_by_count_indexed_no_bytes(self, count: int) -> list[IndexedNoBytes]:
        """Retrives {count} number of indexed items from the database

        Args:
            count (int): number of indexed items to retrieve

        Returns:
            list[IndexedNoBytes]: list of indexed items
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, film_id, title, actresses, url, duration FROM indexed ORDER BY film_id DESC LIMIT %s OFFSET 0",
                (count,),
            )
            indexed: list[IndexedNoBytes] = [
                IndexedNoBytes(**row) for row in cursor.fetchall()
            ]
        self.connection_pool.putconn(connection)
        logging.info(f"Retrieved indexed {len(indexed)}")
        return indexed

    def get_oldest_indexed(self) -> IndexedNoBytes | None:
        """gets the oldest indexed value, if it exists.

        Returns:
            Indexed | None: indexed item or none
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, title, actresses, thumbnail, url, film_id, poster, duration FROM indexed ORDER BY film_id ASC LIMIT 1",
            )
            if (query_result := cursor.fetchone()) is not None:
                indexed: IndexedNoBytes = IndexedNoBytes(**query_result)
            else:
                indexed: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved indexed {indexed}")
        self.connection_pool.putconn(connection)
        return indexed

    def insert_film(self, film: FilmIn) -> Film:
        """Inserts a film into the database

        Args:
            film (FilmIn): film in object

        Returns:
            Film: film out object
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO film (title, duration, date_added, filename, watched, state, thumbnail, poster, download_progress, actresses, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING uuid",
                (
                    film.title,
                    film.duration,
                    film.date_added,
                    film.filename,
                    film.watched,
                    film.state,
                    film.thumbnail,
                    film.poster,
                    film.download_progress,
                    film.actresses,
                    film.rating,
                ),
            )

            film_inserted = Film(uuid=cursor.fetchone()[0], **film.__dict__)
            connection.commit()
        logging.info(f"Inserted film {film_inserted}")
        self.connection_pool.putconn(connection)
        return film_inserted

    def get_film(self, uuid: UUID) -> Film | None:
        """Gets a film from the database

        Args:
            uuid (UUID): film uuid

        Returns:
            Film: film object
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM film WHERE uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                film: Film = Film(**query_result)
            else:
                film: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {film}")
        self.connection_pool.putconn(connection)
        return film

    def get_film_no_bytes(self, uuid: UUID) -> FilmNoBytes | None:
        """Gets a film from the database without the bytes

        Args:
            uuid (UUID): film uuid

        Returns:
            Film: film object
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, title, duration, date_added, filename, watched, state, download_progress, actresses, rating FROM film WHERE uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                film: FilmNoBytes = FilmNoBytes(**query_result)
            else:
                film: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {film}")
        self.connection_pool.putconn(connection)
        return film

    def get_film_thumbnail(self, uuid: UUID) -> bytes | None:
        """gets the thumbnail for a film

        Args:
            uuid (UUID): film uuid

        Returns:
            bytes: image as bytes
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT thumbnail FROM film WHERE uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                thumbnail_bytes: bytes = bytes(query_result[0])
            else:
                thumbnail_bytes: bytes = bytes()
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {uuid} thumbnail")
        self.connection_pool.putconn(connection)
        return thumbnail_bytes

    def get_film_poster(self, uuid: UUID) -> bytes | None:
        """gets poster for a film

        Args:
            uuid (UUID): film uuid

        Returns:
            bytes: image as bytes
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT poster FROM film WHERE uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                poster_bytes: bytes = bytes(query_result[0])
            else:
                poster_bytes: bytes = bytes()
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {uuid} thumbnail")
        self.connection_pool.putconn(connection)
        return poster_bytes

    def set_film_state(self, uuid: UUID, new_state: FilmStateEnum):
        """Sets the state of a film

        Args:
            uuid (UUID): film uuid
            new_state (FilmStateEnum): new state
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE film SET state = %s WHERE uuid = %s",
                (new_state, uuid),
            )
            connection.commit()
        logging.info(f"Set film {uuid} state to {new_state}")
        self.connection_pool.putconn(connection)

    ## QUEUE

    def insert_queue(self, queue: QueueIn) -> Queue:
        """Inserts a queue item into the database

        Args:
            queue (QueueIn): queue in object

        Returns:
            Queue: queue out object
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO queue (url, film_uuid) VALUES (%s, %s) RETURNING uuid",
                (queue.url, queue.film_uuid),
            )
            queue_inserted = Queue(uuid=cursor.fetchone()[0], **queue.__dict__)
            connection.commit()
        logging.info(f"Inserted queue {queue_inserted}")
        self.connection_pool.putconn(connection)
        return queue_inserted

    def get_and_pop_queue(self) -> Queue | None:
        """Gets and pops a queue item from the database

        Returns:
            Queue: queue out object
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM queue WHERE uuid = ( SELECT uuid FROM queue ORDER BY uuid LIMIT 1 FOR UPDATE SKIP LOCKED) LIMIT 1 FOR UPDATE;",
            )
            if (query_result := cursor.fetchone()) is not None:
                queueRetrieved: Queue = Queue(**query_result)
                cursor.execute(
                    "DELETE FROM queue WHERE uuid = %s",
                    (queueRetrieved.uuid,),
                )
                connection.commit()
            else:
                queueRetrieved: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved queue {queueRetrieved}")
        self.connection_pool.putconn(connection)
        return queueRetrieved

    def get_all_films_no_bytes_with_rating_average(
        self,
    ) -> list[FilmNoBytesWithAverage]:
        """Gets all films from the database

        Returns:
            list[Film]: list of film objects
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT f.uuid, f.title, f.duration, f.date_added, f.filename, f.watched, f.state, f.download_progress, f.actresses, f.rating, r.average FROM film f join rating r on f.rating = r.uuid ORDER BY f.uuid",
            )
            films: list[FilmNoBytesWithAverage] = [
                FilmNoBytesWithAverage(**film) for film in cursor.fetchall()
            ]
        logging.info(f"Retrieved all films")
        self.connection_pool.putconn(connection)
        return films

    def drop(self):
        """Drops all tables in the database"""
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "DROP TABLE IF EXISTS queue CASCADE",
            )
            cursor.execute(
                "DROP TABLE IF EXISTS film CASCADE",
            )
            cursor.execute(
                "DROP TABLE IF EXISTS film_actress_rating CASCADE",
            )
            cursor.execute(
                "DROP TABLE IF EXISTS actress CASCADE",
            )
            cursor.execute(
                "DROP TABLE IF EXISTS film CASCADE",
            )
            cursor.execute(
                "DROP TABLE IF EXISTS rating CASCADE",
            )

            cursor.execute(
                "DROP TABLE IF EXISTS film CASCADE",
            )
            cursor.execute(
                "DROP TRIGGER IF EXISTS update_rating_average_trigger ON rating;"
            )
            cursor.execute(
                "DROP TRIGGER IF EXISTS insert_update_delete_history_rating_trigger ON rating;"
            )
            cursor.execute(
                "DROP FUNCTION IF EXISTS insert_update_delete_history_rating;"
            )
            cursor.execute("DROP FUNCTION IF EXISTS insert_update_delete_history_film;")
            cursor.execute(
                "DROP TRIGGER IF EXISTS insert_update_delete_history_film_trigger ON film;"
            )

            cursor.execute("DROP TABLE IF EXISTS history CASCADE;")
            cursor.execute("DROP FUNCTION IF EXISTS update_rating_average();")
            cursor.execute('DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;')
            cursor.execute("DROP TYPE IF EXISTS film_state")
            cursor.execute("DROP TABLE IF EXISTS indexed CASCADE;")
            connection.commit()
        self.connection_pool.putconn(connection)

    def populate_demo_data(self, count: int = 100):
        def load_thumbs(thumbs_dir) -> list[bytes]:
            try:
                thumbs: list[bytes] = []
                for thumb in os.listdir(thumbs_dir):
                    with open(os.path.join(thumbs_dir, thumb), "rb") as f:
                        thumbs.append(f.read())
                return thumbs
            except:
                return [
                    b"this is a thumbnail",
                ]

        def load_posters(posters_dir) -> list[bytes]:
            try:
                posters: list[bytes] = []
                for poster in os.listdir(posters_dir):
                    with open(os.path.join(posters_dir, poster), "rb") as f:
                        posters.append(f.read())
                return posters
            except:
                return [
                    b"this is a poster",
                ]

        list_of_porn_actresses = [
            "Scarlet Skies",
            "Aria Banks",
            "Lily Larimar",
            "Lacy Lennon",
            "Holly Molly",
            "Sharon White",
            "Eliza Ibbarra",
            "Kenna James",
            "Maya Woulfe",
        ]

        ratings: list[Rating] = []

        for _ in range(count):
            ratings.append(
                self.insert_rating(
                    RatingIn(
                        story=random.randint(0, 10),
                        positions=random.randint(0, 10),
                        pussy=random.randint(0, 10),
                        shots=random.randint(0, 10),
                        boobs=random.randint(0, 10),
                        face=random.randint(0, 10),
                        rearview=random.randint(0, 10),
                    )
                )
            )

        thumbs = load_thumbs("temp/thumbs")
        posters = load_posters("temp/posters")

        films: list[Film] = []

        for i in range(count):
            films.append(
                self.insert_film(
                    FilmIn(
                        title=f"sexy time {i + 1}",
                        duration=timedelta(seconds=random.randint(500, 5000)),
                        date_added=date(2022, 4, 22)
                        + timedelta(
                            days=random.randint(
                                0, (date(2023, 4, 22) - date(2022, 4, 22)).days
                            )
                        ),
                        watched=random.choice([False, True]),
                        state=random.choice(list(FilmStateEnum)),
                        thumbnail=random.choice(thumbs),
                        poster=random.choice(posters),
                        download_progress=random.randint(0, 100),
                        filename=f"film_number_{i * random.randint(1, 20)}.mp4",
                        actresses=random.sample(
                            list_of_porn_actresses, random.randint(1, 3)
                        ),
                        rating=ratings[i].uuid,
                    )
                )
            )

        for i in range(1, count):
            self.insert_indexed(
                IndexedIn(
                    title=f"Downloadable Film #{i}",
                    actresses=random.sample(
                        ["Scarlet Skies", "Aria Banks", "Lily Larimar"],
                        random.randint(1, 3),
                    ),
                    thumbnail=random.choice(thumbs),
                    poster=random.choice(posters),
                    url=f"https://hqporner.com/hdporn/{i}.html",
                    film_id=i,
                    duration=timedelta(seconds=random.randint(500, 5000)),
                )
            )

    def set_film_progress(self, newProgress: int, film_uuid: UUID):
        """Sets the download progress of a film

        Args:
            newProgress (int): new progress
            film_uuid (UUID): film to update
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE film SET download_progress = %s WHERE uuid = %s",
                (newProgress, film_uuid),
            )
            connection.commit()
        logging.info(f"Updated download progress for film {film_uuid} to {newProgress}")
        self.connection_pool.putconn(connection)

    def get_single_film_no_bytes(self, uuid: UUID) -> FilmNoBytes | None:
        """gets a single film object with no bytes values (thumbnail, poster, etc)

        Args:
            uuid (UUID): uuid of the film to retrieve

        Returns:
            FilmNoBytes | None: Film object with no bytes values, or None if not found.
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT f.uuid, f.title, f.duration, f.date_added, f.filename, f.watched, f.state, f.download_progress, f.actresses, f.rating FROM film f WHERE f.uuid = %s",
                (uuid,),
            )
            if (query_result := cursor.fetchone()) is not None:
                filmRetrieved: FilmNoBytes = FilmNoBytes(**query_result)
            else:
                filmRetrieved: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {filmRetrieved}")
        self.connection_pool.putconn(connection)
        return filmRetrieved

    def get_actress_detail_all(self) -> list[ActressDetail]:
        """Gets all the actresses and calculates their average rating for each category

        Returns:
            list[ActressDetail]: list of ActressDetail objects
        """

        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            # this gets all the actresses and calculates their average rating for each category
            cursor.execute(
                """
                SELECT 
                    actress as name, 
                    ROUND(CAST(AVG(average) AS NUMERIC), 2) as average,
                    ROUND(CAST(AVG(story) AS NUMERIC), 2) AS story, 
                    ROUND(CAST(AVG(positions) AS NUMERIC), 2) AS positions, 
                    ROUND(CAST(AVG(pussy) AS NUMERIC), 2) AS pussy, 
                    ROUND(CAST(AVG(shots) AS NUMERIC), 2) AS shots, 
                    ROUND(CAST(AVG(boobs) AS NUMERIC), 2) AS boobs, 
                    ROUND(CAST(AVG(face) AS NUMERIC), 2) AS face, 
                    ROUND(CAST(AVG(rearview) AS NUMERIC), 2) AS rearview,
                    count(*) as film_count
                FROM (
                SELECT 
                    unnest(actresses) AS actress, 
                    rating.*
                FROM 
                    film 
                    JOIN rating ON film.rating = rating.uuid
                ) subquery
                GROUP BY 
                actress
                ORDER BY name;
                """
            )

            actresses: list[ActressDetail] = [
                ActressDetail(**a) for a in cursor.fetchall()
            ]

        self.connection_pool.putconn(connection)

        logging.info("Retrieved all actress detail")
        return actresses

    def update_watch_status(self, uuid: UUID, watch_status: bool) -> None:
        """updates the watch status for a given film

        Args:
            uuid (UUID): film uuid
            watch_status (bool): new watch status
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE film SET watched = %s WHERE uuid = %s",
                (
                    watch_status,
                    uuid,
                ),
            )
            connection.commit()
        logging.info(f"Updated watch status for film {uuid}")
        self.connection_pool.putconn(connection)

    def get_latest_commit_uuid(self) -> UUID | None:
        """The database has a trigger which runs on every database operation (other than read.)
        This trigger inserts a new row into the history table.
        this table is used to track when the database data has changed, and to only
        rehydrate the server state once it has.

        Returns:
            UUID: uuid of the latest commit
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM history ORDER BY timestamp DESC LIMIT 1",
            )
            try:
                uuid = cursor.fetchone()[0]
            except TypeError:
                uuid = None
        self.connection_pool.putconn(connection)
        logging.info(f"Retrieved latest commit uuid {uuid}")
        return uuid

    def delete_film(self, uuid: UUID) -> None:
        """deletes a film from the database. This does not handle the deletion of the referenced video file.

        Args:
            uuid (UUID): uuid of film to delete
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            # this sql deletes the film and rating records in a single transaction
            cursor.execute(
                "WITH deleted_film_ret AS (DELETE FROM film WHERE uuid = %s RETURNING rating) DELETE FROM rating where uuid = (SELECT * FROM deleted_film_ret);",
                (uuid,),
            )
            connection.commit()
        self.connection_pool.putconn(connection)
        logging.info(f"Deleted film {uuid}")

    def get_database_size(self) -> int:
        """Query the current size of the database in Megabytes

        Returns:
            int: megabytes of database size
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT pg_size_pretty(pg_database_size(%s));",
                (self.db_name,),
            )
            size: int = int("".join([i for i in cursor.fetchone()[0] if i.isdigit()]))
        self.connection_pool.putconn(connection)
        logging.info(f"Retrieved database size {size}")
        return size

    def get_indexed_thumbnail(self, uuid: UUID) -> bytes:
        """gets the thumbnail of an indexed film

        Args:
            uuid (UUID): uuid of indexed item

        Returns:
            bytes: thumbnail bytes
        """
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT thumbnail FROM indexed WHERE uuid = %s",
                (uuid,),
            )
            thumbnail: bytes = cursor.fetchone()[0]
        self.connection_pool.putconn(connection)
        logging.info("Retrieved thumbnail")

        return bytes(thumbnail)
