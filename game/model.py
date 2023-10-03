import random

from food import Food
from judger import Judger
from position import Position
from score import Score
from snake import Snake
from stage import Stage


class Model:
    def __init__(self):
        self.stage = Stage()
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.game_over = False

    def update(self):
        self.snake.move()
        if Judger.check_collision_food(self.snake, self.food):
            self.snake.grow()
            self.score.add()
            self.set_food()
        if Judger.check_collision_self(self.snake) or Judger.check_collision_wall(self.snake):
            self.game_over = True

    def set_food(self):
        while True:
            pos = Position(random.randint(1, Stage.WIDTH), random.randint(1, Stage.HEIGHT))
            if self.stage.is_empty(pos):
                break
        self.food = Food(pos)
