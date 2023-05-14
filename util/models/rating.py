from dataclasses import dataclass
from uuid import UUID


@dataclass
class RatingIn:
    story: int
    positions: int
    pussy: int
    shots: int
    boobs: int
    face: int
    rearview: int

    def __repr__(self) -> str:
        return (
            "RatingIn(story=%s, positions=%s, pussy=%s, shots=%s, boobs=%s, face=%s, rearview=%s)"
            % (
                self.story,
                self.positions,
                self.pussy,
                self.shots,
                self.boobs,
                self.face,
                self.rearview,
            )
        )


@dataclass
class Rating:
    uuid: UUID

    average: float | None
    story: int
    positions: int
    pussy: int
    shots: int
    boobs: int
    face: int
    rearview: int

    def __repr__(self) -> str:
        return (
            "Rating(uuid=%s, story=%s, positions=%s, pussy=%s, shots=%s, boobs=%s, face=%s, rearview=%s)"
            % (
                self.uuid,
                self.story,
                self.positions,
                self.pussy,
                self.shots,
                self.boobs,
                self.face,
                self.rearview,
            )
        )
