import random

from .food import Food
from .judger import Judger
from .position import Position
from .score import Score
from .snake import Snake
from .stage import Stage


class Model:
    def __init__(self):
        self.stage = Stage()
        self.snake = Snake()
        self.score = Score()
        self.food = Food(self.get_empty_position())
        self.game_over = False
        self._board = [[0 for _ in range(Stage.WIDTH)] for _ in range(Stage.HEIGHT)]

    def update(self):
        try:
            if Judger.check_back(self.snake):
                self.snake.move_according_to_inertia()
                return
        except ValueError:
            self.game_over = True
            return

        try:
            self.snake.move()
        except ValueError:
            self.game_over = True
            return
        if Judger.check_collision_food(self.snake, self.food):
            self.snake.grow()
            self.score.add()
            self.food = Food(self.get_empty_position())
        if Judger.check_collision_self(self.snake) or Judger.check_collision_wall(self.snake):
            self.game_over = True

        if not self.game_over:
            self._board = [[0 for _ in range(Stage.WIDTH)] for _ in range(Stage.HEIGHT)]
            self._board[self.snake.head.y - 1][self.snake.head.x - 1] = 1
            for body in self.snake.body:
                self._board[body.y - 1][body.x - 1] = 2

            self._board[self.food.pos.y - 1][self.food.pos.x - 1] = 3

    def get_empty_position(self) -> Position:
        while True:
            pos = Position(random.randint(1, Stage.WIDTH), random.randint(1, Stage.HEIGHT))
            if pos not in self.snake.position_list:
                return pos

    def is_game_over(self):
        return self.game_over

    @property
    def board(self) -> list[list[int]]:
        return self._board
