from enum import Enum


class Action(Enum):
    STRAIGHT = 0
    TURN_RIGHt = 1
    TURN_LEFT = 2


class ActionSpace:
    def __init__(self) -> None:
        self._value = [Action.STRAIGHT, Action.TURN_RIGHt, Action.TURN_LEFT]
        return

    @property
    def action_space(self) -> list[Action]:
        return self._value

    @property
    def n(self) -> int:
        return len(self._value)
