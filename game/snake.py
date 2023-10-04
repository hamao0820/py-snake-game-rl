from direction import Direction, Down, Left, Right, Up
from position import Position


class Snake():
    def __init__(self) -> None:
        self._position_list: list[Position] = [Position(x=3, y=8), Position(x=2, y=8)]
        self.direction: Direction = Right()
        pass

    def move(self) -> None:
        new_position = self.head + self.direction.delta
        self._position_list.insert(0, new_position)
        self._position_list.pop()

    def up(self) -> None:
        self.direction = Up()

    def down(self) -> None:
        self.direction = Down()

    def left(self) -> None:
        self.direction = Left()

    def right(self) -> None:
        self.direction = Right()

    def grow(self) -> None:
        new_position = self.head + self.direction.delta
        self._position_list.insert(0, new_position)

    @property
    def position_list(self) -> list[Position]:
        return self._position_list

    @property
    def head(self) -> Position:
        return self._position_list[0]

    @property
    def body(self) -> list[Position]:
        return self._position_list[1:]
