from enum import Enum


class Action(Enum):
    Right = 0
    Left = 1
    Up = 2
    Down = 3


class ActionSpace:
    def __init__(self) -> None:
        self._value = [Action.Right, Action.Left, Action.Up, Action.Down]
        return

    @property
    def action_space(self) -> list[Action]:
        return self._value

    @property
    def n(self) -> int:
        return len(self._value)
