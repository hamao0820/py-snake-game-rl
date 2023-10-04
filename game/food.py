from position import Position


class Food():
    def __init__(self, pos: Position):
        self._pos = pos
        pass

    @property
    def pos(self) -> Position:
        return self._pos
