from .direction import Direction, Right
from .position import Position
from .stage import Stage


class Snake:
    def __init__(self) -> None:
        self._position_list: list[Position] = [Position(x=3, y=8), Position(x=2, y=8)]
        self.direction: Direction = Right()
        self.grow_flag: bool = False
        pass

    def move(self) -> None:
        self._position_list.insert(0, self.next_position)
        if not self.grow_flag:
            self._position_list.pop()
        self.grow_flag = False

    def turn_right(self) -> None:
        self.direction = self.direction.turn_right()

    def turn_left(self) -> None:
        self.direction = self.direction.turn_left()

    def straight(self) -> None:
        self.direction = self.direction.straight()

    def grow(self) -> None:
        self.grow_flag = True

    @property
    def position_list(self) -> list[Position]:
        return self._position_list

    @property
    def head(self) -> Position:
        return self._position_list[0]

    @property
    def body(self) -> list[Position]:
        return self._position_list[1:]

    @property
    def next_position(self) -> Position:
        return self.head + self.direction.delta

    @property
    def can_turn_left(self) -> bool:
        try:
            left_pos = self.head + self.direction.turn_left().delta
        except ValueError:
            return False

        return (
            left_pos.x >= 1
            and left_pos.x <= Stage.WIDTH
            and left_pos.y >= 1
            and left_pos.y <= Stage.HEIGHT
            and left_pos not in self.body
        )

    @property
    def can_turn_right(self) -> bool:
        try:
            right_pos = self.head + self.direction.turn_right().delta
        except ValueError:
            return False

        return (
            right_pos.x >= 1
            and right_pos.x <= Stage.WIDTH
            and right_pos.y >= 1
            and right_pos.y <= Stage.HEIGHT
            and right_pos not in self.body
        )

    @property
    def can_straight(self) -> bool:
        try:
            straight_pos = self.head + self.direction.straight().delta
        except ValueError:
            return False

        return (
            straight_pos.x >= 1
            and straight_pos.x <= Stage.WIDTH
            and straight_pos.y >= 1
            and straight_pos.y <= Stage.HEIGHT
            and straight_pos not in self.body
        )
