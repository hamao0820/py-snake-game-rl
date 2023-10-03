from abc import ABC, abstractproperty


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
