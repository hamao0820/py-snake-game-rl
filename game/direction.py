from abc import ABC, abstractmethod, abstractproperty


class Direction(ABC):
    def __init__(self):
        return

    @abstractproperty
    def delta(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def turn_right(self) -> "Direction":
        pass

    @abstractmethod
    def turn_left(self) -> "Direction":
        pass

    @abstractmethod
    def straight(self) -> "Direction":
        pass


class Right(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (1, 0)

    def turn_right(self) -> "Down":
        return Down()

    def turn_left(self) -> "Up":
        return Up()

    def straight(self) -> "Right":
        return Right()


class Left(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (-1, 0)

    def turn_right(self) -> "Up":
        return Up()

    def turn_left(self) -> "Down":
        return Down()

    def straight(self) -> "Left":
        return Left()


class Up(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (0, -1)

    def turn_right(self) -> "Right":
        return Right()

    def turn_left(self) -> "Left":
        return Left()

    def straight(self) -> "Up":
        return Up()


class Down(Direction):
    @property
    def delta(self) -> tuple[int, int]:
        return (0, 1)

    def turn_right(self) -> "Left":
        return Left()

    def turn_left(self) -> "Right":
        return Right()

    def straight(self) -> "Down":
        return Down()
