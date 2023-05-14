import logging
import random
from datetime import date, timedelta
from pathlib import Path
from uuid import UUID

import psycopg2
from beartype import beartype
from psycopg2 import pool
from psycopg2.extras import DictCursor, UUID_adapter, register_uuid

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
        max_connections: int = 5,
        min_connections: int = 1,
    ):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.min_connections = min_connections
        self.max_connections = max_connections
        register_uuid()
        self.connection_pool = pool.SimpleConnectionPool(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            minconn=self.min_connections,
            maxconn=self.max_connections,
        )

        logging.info("Connected to database")

    def initialize(self, sql_path: Path):
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
                "INSERT INTO indexed (title, actresses, thumbnail, url, film_id) VALUES (%s, %s, %s, %s, %s) RETURNING uuid",
                (
                    indexed.title,
                    indexed.actresses,
                    indexed.thumbnail,
                    indexed.url,
                    indexed.film_id,
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
                "SELECT uuid, title, actresses, thumbnail, url, film_id FROM indexed WHERE uuid = %s",
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
            cursor.execute("SELECT uuid FROM indexed WHERE film_id = %s", (film_id,))
            result: bool = bool(cursor.fetchone())
        self.connection_pool.putconn(connection)
        return result

    def get_page_indexed(self) -> list[Indexed]:
        """This method will be used to get a page of indexed items. TBI"""
        ...

    def get_oldest_indexed(self) -> IndexedNoBytes | None:
        """gets the oldest indexed value, if it exists.

        Returns:
            Indexed | None: indexed item or none
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, title, actresses, thumbnail, url, film_id FROM indexed ORDER BY film_id ASC LIMIT 1",
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
            queue_inserted = Queue(uuid=cursor.fetchone()[0], **queue.dict())
            connection.commit()
        logging.info(f"Inserted queue {queue_inserted}")
        connection = self.connection_pool.putconn()
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
                "SELECT f.uuid, f.title, f.duration, f.date_added, f.filename, f.watched, f.state, f.download_progress, f.actresses, f.rating, r.average FROM film f join rating r on f.rating = r.uuid",
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
            cursor.execute("DROP FUNCTION IF EXISTS update_rating_average();")
            cursor.execute('DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;')
            cursor.execute("DROP TYPE IF EXISTS film_state")
            cursor.execute("DROP TABLE IF EXISTS indexed CASCADE;")
            connection.commit()
        self.connection_pool.putconn(connection)

    def populate_demo_data(self):
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

        for _ in range(500):
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

        films: list[Film] = []

        for i in range(len(ratings)):
            with open("./temp/thumbnail.jpg", "rb") as thumbnail, open(
                "./temp/poster.jpg", "rb"
            ) as poster:
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
                            watched=random.choice([True, False]),
                            state=random.choice(list(FilmStateEnum)),
                            thumbnail=thumbnail.read(),
                            poster=poster.read(),
                            download_progress=random.randint(0, 100),
                            filename=f"film_number_{i * random.randint(1, 20)}.mp4",
                            actresses=random.sample(
                                list_of_porn_actresses, random.randint(1, 3)
                            ),
                            rating=ratings[i].uuid,
                        )
                    )
                )

        for i in range(111420, 111450):
            self.insert_indexed(
                IndexedIn(
                    title=f"Downloadable Film #{i}",
                    actresses=random.sample(
                        ["Scarlet Skies", "Aria Banks", "Lily Larimar"],
                        random.randint(1, 3),
                    ),
                    thumbnail=b"this is a thumbnail",
                    url=f"https://www.pornhub.com/view_video.php?viewkey={i}",
                    film_id=i,
                )
            )

    def set_film_progress(self, newProgress: int, film_uuid: UUID):
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
