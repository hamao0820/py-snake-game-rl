from game_object import Game_Object
from position import Position


class Food(Game_Object):
    def __init__(self, pos: Position):
        self._pos = pos
        pass

    @property
    def pos(self) -> Position:
        return self._pos
