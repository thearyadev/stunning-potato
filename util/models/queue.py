from uuid import UUID
from dataclasses import dataclass
@dataclass
class QueueIn:
    url: str
    film_uuid: UUID 

@dataclass
class Queue:
    uuid: UUID
    url: str
    film_uuid: UUID
