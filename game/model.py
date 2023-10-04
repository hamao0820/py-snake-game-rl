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

    def update(self):
        if Judger.check_back(self.snake):
            self.snake.move_according_to_inertia()
            return
        self.snake.move()
        if Judger.check_collision_food(self.snake, self.food):
            self.snake.grow()
            self.score.add()
            self.food = Food(self.get_empty_position())
        if Judger.check_collision_self(self.snake) or Judger.check_collision_wall(self.snake):
            self.game_over = True

    def get_empty_position(self) -> Position:
        while True:
            pos = Position(random.randint(1, Stage.WIDTH), random.randint(1, Stage.HEIGHT))
            if pos not in self.snake.position_list:
                return pos

    def is_game_over(self):
        return self.game_over

    @property
    def board(self) -> list[list[int]]:
        board = [[0 for _ in range(Stage.WIDTH)] for _ in range(Stage.HEIGHT)]
        board[self.snake.head.y - 1][self.snake.head.x - 1] = 1
        for body in self.snake.body:
            board[body.y - 1][body.x - 1] = 2

        board[self.food.pos.y - 1][self.food.pos.x - 1] = 3

        return board
