class Score:
    def __init__(self) -> None:
        self._score = 0

    def add(self) -> None:
        self._score += 1

    @property
    def score(self) -> int:
        return self._score
