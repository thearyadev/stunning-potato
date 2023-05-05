import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import pool
from pathlib import Path
import logging
from util.models.film_actress_rating import FilmActressRating
from util.models.actress import ActressIn, Actress
from util.models.film import FilmIn, Film, FilmNoBytes
from util.models.indexed import IndexedIn, Indexed
from util.models.queue import QueueIn, Queue
from util.models.rating import RatingIn, Rating
from util.models.indexed import IndexedIn, Indexed, IndexedNoBytes
from uuid import UUID


class DatabaseAccess:
    """Connection to PostgreSQL database tools"""

    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.min_connections = 1
        self.max_connections = 5

        # Create connection
        # self.connection = psycopg2.connect(
        #     host=self.db_host,
        #     port=self.db_port,
        #     dbname=self.db_name,
        #     user=self.db_user,
        #     password=self.db_password,
        # )


        self.connection_pool = pool.ThreadedConnectionPool(
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

    ## ACTRESS
    def insert_actress(self, actress: ActressIn) -> Actress:
        """Adds an actress to the database

        Args:
            actress (ActressIn): Actress in (no uuid)

        Returns:
            Actress: Actress out (with uuid)
        """
        connection = self.connection_pool.getconn()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO actress (name_) VALUES (%s) RETURNING uuid",
                (actress.name_,),
            )
            # returns uuid, capture and recreate object
            actress_inserted: Actress = Actress(
                uuid=cursor.fetchone()[0], name_=actress.name_
            )
            connection.commit()
        self.connection_pool.putconn(connection)
        logging.info(f"Inserted actress {actress_inserted}")

    def get_actress(self, uuid: UUID) -> Actress | None:
        """Gets an actress by the uuid

        Args:
            uuid (UUID):  uuid of the actress in the database

        Returns:
            Actress | None: Returns none if no actress is found
        """
        connection = self.connection_pool.getconn()

        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, name_ FROM actress WHERE uuid = %s",
                (str(uuid),),
            )
            if (query_result := cursor.fetchone()) is not None:
                actress: Actress = Actress(**query_result)
            else:
                actress: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved actress {actress}")
        self.connection_pool.putconn(connection)
        return actress

    def get_all_actresses(self) -> list[Actress]:
        """Gets all actresses from the database

        Returns:
            list[Actress]: list of actress out objects
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, name_ FROM actress",
            )
            actresses: list[Actress] = [
                Actress(**actress) for actress in cursor.fetchall()
            ]
        logging.info(f"Retrieved {len(actresses)} actresses")
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
                uuid=raw_data_queried[0], average=raw_data_queried[1], **rating.dict()
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
            cursor.execute("SELECT * FROM rating WHERE uuid = %s", str(uuid))
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
                    str(rating.uuid),
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
                "INSERT INTO indexed (title, actresses, thumbnail, url) VALUES (%s, %s, %s, %s) RETURNING uuid",
                (indexed.title, indexed.actresses, indexed.thumbnail, indexed.url),
            )
            logging.info(f"Inserted indexed {indexed}")
            indexed_inserted: Indexed = Indexed(
                uuid=cursor.fetchone()[0], **indexed.dict()
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
                (str(uuid),),
            )
            if (query_result := cursor.fetchone()) is not None:
                indexed: Indexed = Indexed(**query_result)
            else:
                indexed: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved indexed {indexed}")
        self.connection_pool.putconn(connection)
        return indexed

    def get_indexed_no_bytes(self, uuid: UUID) -> IndexedNoBytes:
        """Given a indexed uuid, returns the indexed object

        Args:
            uuid (UUID): indexed item uuid

        Returns:
            Indexed: indexed item, uuid included
        """
        connection = self.connection_pool.getconn()
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, title, actresses, thumbnail, url FROM indexed WHERE uuid = %s",
                (str(uuid),),
            )
            if (query_result := cursor.fetchone()) is not None:
                indexed: IndexedNoBytes = IndexedNoBytes(**query_result)
            else:
                indexed: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved indexed {indexed}")
        self.connection_pool.putconn(connection)
        return indexed

    def get_page_indexed(self) -> list[Indexed]:
        """This method will be used to get a page of indexed items. TBI"""
        ...

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
                "INSERT INTO film (title, duration, date_added, filename, watched, state, thumbnail, poster, download_progress) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING uuid",
                (film.title, film.duration, film.date_added, film.filename, film.watched, film.state, film.thumbnail, film.poster, film.download_progress),
            )
            film_inserted = Film(uuid=cursor.fetchone()[0], **film.dict())
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
                (str(uuid),),
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
                "SELECT uuid, title, duration, date_added, filename, watched, state, download_progress FROM film WHERE uuid = %s",
                (str(uuid),),
            )
            if (query_result := cursor.fetchone()) is not None:
                film: FilmNoBytes = FilmNoBytes(**query_result)
            else:
                film: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {film}")
        self.connection_pool.putconn(connection)
        return film
    
    def get_film_thumbnail(self, uuid: UUID) -> bytes:
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
                (str(uuid),),
            )
            if (query_result := cursor.fetchone()) is not None:
                thumbnail_bytes: bytes = bytes(query_result[0])
            else:
                thumbnail_bytes: bytes = bytes()
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {uuid} thumbnail")
        self.connection_pool.putconn(connection)
        return thumbnail_bytes
    
    def get_film_poster(self, uuid: UUID) -> bytes:
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
                (str(uuid),),
            )
            if (query_result := cursor.fetchone()) is not None:
                poster_bytes: bytes = bytes(query_result[0])
            else:
                poster_bytes: bytes = bytes()
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved film {uuid} thumbnail")
        self.connection_pool.putconn(connection)
        return poster_bytes
    
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
                (queue.url, str(queue.film_uuid)),
            )
            queue_inserted = Queue(uuid=cursor.fetchone()[0], **queue.dict())
            connection.commit()
        logging.info(f"Inserted queue {queue_inserted}")
        connection = self.connection_pool.getconn()
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
                queue: Queue = Queue(**query_result)
                cursor.execute(
                    "DELETE FROM queue WHERE uuid = %s",
                    (str(queue.uuid),),
                )
                connection.commit()
            else:
                queue: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved queue {queue}")
        self.connection_pool.putconn(connection)
        return queue
    
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
                "DROP FUNCTION IF EXISTS update_rating_average();"
            )
            cursor.execute(
                "DROP EXTENSION IF EXISTS \"uuid-ossp\" CASCADE;"
            )
            cursor.execute(
                "DROP TYPE IF EXISTS film_state"
            )
            cursor.execute(
                "DROP TABLE IF EXISTS indexed CASCADE;"
            )
            if input("ENTER Y TO RESET DATABASE: ") == "y":
                logging.warning("DROPPING DATABASE")
                connection.commit()
            else:
                logging.warning("NOT DROPPING DATABASE")
                connection.rollback()
        self.connection_pool.putconn(connection)