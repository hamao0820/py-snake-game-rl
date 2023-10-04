from .stage import Stage


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        if x < 0 or x > Stage.WIDTH + 1 or y < 0 or y > Stage.HEIGHT + 1:
            raise ValueError("Invalid position")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, delta: tuple[int, int]):
        return Position(self.x + delta[0], self.y + delta[1])
