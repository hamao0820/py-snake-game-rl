from game.model import Model
from game.direction import Right, Left, Up, Down
from pynput.keyboard import Key


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def on_press(self, key):
        if key == Key.up:
            self.handle_arrow_up()
        elif key == Key.down:
            self.handle_arrow_down()
        elif key == Key.left:
            self.handle_arrow_left()
        elif key == Key.right:
            self.handle_arrow_right()
        else:
            print("Invalid input")

    def on_release(self, key):
        return key != Key.up and key != Key.down and key != Key.left and key != Key.right

    def handle_arrow_up(self) -> bool:
        if isinstance(self.model.snake.direction, Down):
            return False

        if isinstance(self.model.snake.direction, Right):
            self.model.snake.turn_left()
        elif isinstance(self.model.snake.direction, Left):
            self.model.snake.turn_right()
        else:
            self.model.snake.straight()

        return True

    def handle_arrow_down(self) -> bool:
        if isinstance(self.model.snake.direction, Up):
            return False

        if isinstance(self.model.snake.direction, Right):
            self.model.snake.turn_right()
        elif isinstance(self.model.snake.direction, Left):
            self.model.snake.turn_left()
        else:
            self.model.snake.straight()

        return True

    def handle_arrow_left(self) -> bool:
        if isinstance(self.model.snake.direction, Right):
            return False

        if isinstance(self.model.snake.direction, Up):
            self.model.snake.turn_left()
        elif isinstance(self.model.snake.direction, Down):
            self.model.snake.turn_right()
        else:
            self.model.snake.straight()

        return True

    def handle_arrow_right(self) -> bool:
        if isinstance(self.model.snake.direction, Left):
            return False

        if isinstance(self.model.snake.direction, Up):
            self.model.snake.turn_right()
        elif isinstance(self.model.snake.direction, Down):
            self.model.snake.turn_left()
        else:
            self.model.snake.straight()

        return True
