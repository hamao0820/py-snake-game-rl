from abc import ABC


class Action(ABC):
    pass


class Right(Action):
    pass


class Left(Action):
    pass


class Up(Action):
    pass


class Down(Action):
    pass


class ActionSpace:
    def __init__(self) -> None:
        self._value = [Right(), Left(), Up(), Down()]
        return

    @property
    def action_space(self) -> list[Action]:
        return self._value

    @property
    def n(self) -> int:
        return len(self._value)
