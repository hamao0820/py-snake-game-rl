from game_object import Game_Object
from position import Position


class Cell:
    def __init__(self, pos: Position, game_object: Game_Object | None = None):
        self.pos = pos
        self.value: Game_Object | None = game_object

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self.value = value


class Stage:
    Width: int = 16
    Height: int = 16

    def __init__(self):
        self.grid = [[Cell(Position(x, y)) for x in range(Stage.Width + 1)] for y in range(Stage.Height + 1)]

    def get_cell_value(self, pos: Position) -> Cell:
        return self.grid[pos.y][pos.x].value

    def set_cell(self, pos: Position, game_object: Game_Object | None = None) -> None:
        self.grid[pos.y][pos.x].value = game_object

    def clear_cell(self, pos: Position) -> None:
        self.grid[pos.y][pos.x].value = None
