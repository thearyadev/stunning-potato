from dataclasses import dataclass


@dataclass
class ActressDetail:
    name: str | None = None
    average: float | None = None
    story: float | None = None
    positions: float | None = None
    pussy: float | None = None
    shots: float | None = None
    boobs: float | None = None
    face: float | None = None
    rearview: float | None = None
    film_count: int | None = None

    def __repr__(self) -> str:
        return (
            "ActressDetail(name=%s, average=%s, story=%s, positions=%s, pussy%s, shots=%s, boobs=%s, face=%s, rearview=%s, flimCount=%s)"
            % (
                self.name,
                self.average,
                self.story,
                self.positions,
                self.pussy,
                self.shots,
                self.boobs,
                self.face,
                self.rearview,
                self.film_count,
            )
        )
