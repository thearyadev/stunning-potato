from uuid import UUID

from dataclasses import dataclass

@dataclass
class IndexedIn:
    film_id: int
    title: str 
    actresses: list[str] 
    thumbnail: bytes 
    url: str

@dataclass
class Indexed:
    uuid: UUID 
    film_id: int
    title: str
    actresses: list[str] 
    thumbnail: bytes | memoryview 
    url: str 


@dataclass
class IndexedNoBytes:
    uuid: UUID 
    film_id: int
    title: str 
    actresses: list[str] 
    url: str 
