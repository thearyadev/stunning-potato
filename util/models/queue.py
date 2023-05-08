from uuid import UUID
from dataclasses import dataclass
@dataclass
class QueueIn:
    url: str
    film_uuid: UUID 

    def __repr__(self) -> str:
        return "QueueIn(url=%s, film_uuid=%s)" % (self.url, self.film_uuid)
@dataclass
class Queue:
    uuid: UUID
    url: str
    film_uuid: UUID

    def __repr__(self) -> str:
        return "Queue(uuid=%s, url=%s, film_uuid=%s)" % (self.uuid, self.url, self.film_uuid)