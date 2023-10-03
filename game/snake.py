from abc import ABC, abstractproperty

from game_object import Game_Object
from position import Position


class Direction(ABC):
    def __init__(self):
        return

    @abstractproperty
    def delta(self) -> tuple[int, int]:
        pass


class Right(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (1, 0)


class Left(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (-1, 0)


class Up(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (0, -1)


class Down(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (0, 1)


class Snake(Game_Object):
    def __init__(self) -> None:
        self.position_list: list[Position] = [Position(x=3, y=8), Position(x=2, y=8)]
        self.direction: Direction = Right()
        pass

    def move(self):
        head = self.position_list[0]
        new_position = head + self.direction.delta
        self.position_list.insert(0, new_position)
        self.position_list.pop()

    def change_direction(self, new_direction: Direction) -> None:
        self.direction = new_direction

    def grow(self) -> None:
        head = self.position_list[0]
        new_position = head + self.direction.delta
        self.position_list.insert(0, new_position)
