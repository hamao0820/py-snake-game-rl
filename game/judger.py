from food import Food
from snake import Snake
from stage import Stage


class Judger:
    @staticmethod
    def check_collision_self(snake: Snake) -> bool:
        return snake.head in snake.body

    @staticmethod
    def check_collision_wall(snake: Snake) -> bool:
        return snake.head.x < 1 or snake.head.x > Stage.WIDTH or snake.head.y < 1 or snake.head.y > Stage.HEIGHT

    @staticmethod
    def check_collision_food(snake: Snake, food: Food) -> bool:
        return snake.head == food.pos

    @staticmethod
    def check_back(snake: Snake) -> bool:
        return snake.next_position == snake.body[0]
