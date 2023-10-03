from food import Food
from snake import Snake
from stage import Stage


class Judger:
    @staticmethod
    def check_collision_self(self, snake: Snake) -> bool:
        if snake.head in snake.body:
            return True
        return False

    @staticmethod
    def check_collision_wall(self, snake: Snake) -> bool:
        if (
            snake.position_list[0].x < 1
            or snake.position_list[0].x > Stage.WIDTH
            or snake.position_list[0].y < 1
            or snake.position_list[0].y > Stage.HEIGHT
        ):
            return True
        return False

    @staticmethod
    def check_collision_food(self, snake: Snake, food: Food) -> bool:
        if snake.head == food.pos:
            return True
        return False
