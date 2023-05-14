from dataclasses import dataclass
from uuid import UUID


@dataclass
class IndexedIn:
    film_id: int
    title: str
    actresses: list[str]
    thumbnail: bytes
    url: str

    def __repr__(
        self,
    ) -> str:
        return "IndexedIn(film_id=%s, title=%s, actresses=%s, url=%s)" % (
            self.film_id,
            self.title,
            self.actresses,
            self.url,
        )


@dataclass
class Indexed:
    uuid: UUID
    film_id: int
    title: str
    actresses: list[str]
    thumbnail: bytes | memoryview
    url: str

    def __repr__(
        self,
    ) -> str:
        return "Indexed(uuid=%s, film_id=%s, title=%s, actresses=%s, url=%s)" % (
            self.uuid,
            self.film_id,
            self.title,
            self.actresses,
            self.url,
        )


@dataclass
class IndexedNoBytes:
    uuid: UUID
    film_id: int
    title: str
    actresses: list[str]
    url: str

    def __repr__(
        self,
    ) -> str:
        return "IndexedIn(uuid=%s, film_id=%s, title=%s, actresses=%s, url=%s)" % (
            self.uuid,
            self.film_id,
            self.title,
            self.actresses,
            self.url,
        )
