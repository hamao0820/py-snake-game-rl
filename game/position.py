class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, delta: tuple[int, int]):
        return Position(self.x + delta[0], self.y + delta[1])
