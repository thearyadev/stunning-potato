import psycopg2
from psycopg2.extras import DictCursor
from pathlib import Path
import logging
from util.models.film_actress_rating import FilmActressRating
from util.models.actress import ActressIn, Actress
from util.models.film import FilmIn, Film
from util.models.indexed import IndexedIn, Indexed
from util.models.queue import QueueIn, Queue
from util.models.rating import RatingIn, Rating
from util.models.indexed import IndexedIn, Indexed
from uuid import UUID


class DatabaseAccess:
    """Connection to PostgreSQL database tools"""

    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

        # Create connection
        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
        )
        logging.info("Connected to database")

    def initialize(self, sql_path: Path):
        """Creates all the tables as defined in a .sql file

        Args:
            sql_path (Path): path to sql file
        """
        with open(sql_path, "r") as sql_file, self.connection.cursor() as cursor:
            cursor.execute(sql_file.read())
            self.connection.commit()
        logging.info("Initialized database")

    ## ACTRESS
    def insert_actress(self, actress: ActressIn) -> Actress:
        """Adds an actress to the database

        Args:
            actress (ActressIn): Actress in (no uuid)

        Returns:
            Actress: Actress out (with uuid)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO actress (name_) VALUES (%s) RETURNING uuid",
                (actress.name_,),
            )
            # returns uuid, capture and recreate object
            actress_inserted: Actress = Actress(
                uuid=cursor.fetchone()[0], name_=actress.name_
            )
            self.connection.commit()
        logging.info(f"Inserted actress {actress_inserted}")

    def get_actress(self, uuid: UUID) -> Actress | None:
        """Gets an actress by the uuid

        Args:
            uuid (UUID):  uuid of the actress in the database

        Returns:
            Actress | None: Returns none if no actress is found
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
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
        return actress

    def get_all_actresses(self) -> list[Actress]:
        """Gets all actresses from the database

        Returns:
            list[Actress]: list of actress out objects
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT uuid, name_ FROM actress",
            )
            actresses: list[Actress] = [
                Actress(**actress) for actress in cursor.fetchall()
            ]
        logging.info(f"Retrieved {len(actresses)} actresses")
        return actresses

    ## RATING

    def insert_rating(self, rating: RatingIn) -> Rating:
        """Insert a rating to the database

        Args:
            rating (RatingIn): Rating in object; no uuid; no average

        Returns:
            Rating: Rating out, with uuid and average. Average will be none.
        """
        with self.connection.cursor() as cursor:
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
            self.connection.commit()
        logging.info(f"Inserted rating {rating_inserted}")
        return rating_inserted

    def get_rating(self, uuid: UUID) -> Rating | None:
        """Gets a rating record given the ratings uuid

        Args:
            uuid (UUID): ratings uuid

        Returns:
            Rating | None: returns none if no rating is found
        """
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM rating WHERE uuid = %s", str(uuid))
            if (query_result := cursor.fetchone()) is not None:
                rating: Rating = Rating(**query_result)
            else:
                rating: None = None
                logging.warning("Attemped to access record that does not exist.")
        logging.info(f"Retrieved Rating {rating}")
        return rating

    def update_rating(self, rating: Rating) -> Rating:
        """Updates a rating record in the database

        Args:
            rating (Rating): Rating object with uuid and average (average is ignored)

        Returns:
            Rating: Rating object with uuid and average (av is ignored)
        """
        with self.connection.cursor() as cursor:
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
            self.connection.commit()
        logging.info(f"Updated Rating {rating}")
        return rating

    ## INDEXED
    def insert_indexed(self, indexed: IndexedIn) -> Indexed:
        """Inserts an indexed entry

        Args:
            indexed (IndexedIn): indexed in object

        Returns:
            Indexed: indexed out, includes uuid
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO indexed (title, actresses, thumbnail, url) VALUES (%s, %s, %s, %s) RETURNING uuid",
                (indexed.title, indexed.actresses, indexed.thumbnail, indexed.url),
            )
            logging.info(f"Inserted indexed {indexed}")
            indexed_inserted: Indexed = Indexed(uuid=cursor.fetchone()[0], **indexed.dict())
            self.connection.commit()
            return indexed_inserted
