from uuid import UUID

from dataclasses import dataclass

@dataclass
class IndexedIn:
    title: str 
    actresses: list[str] 
    thumbnail: bytes 
    url: str

@dataclass
class Indexed:
    uuid: UUID 
    title: str
    actresses: list[str] 
    thumbnail: bytes | memoryview 
    url: str 


@dataclass
class IndexedNoBytes:
    uuid: UUID 
    title: str 
    actresses: list[str] 
    url: str 
