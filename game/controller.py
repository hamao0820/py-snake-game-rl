from model import Model


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def handle_up(self):
        self.model.snake.up()

    def handle_down(self):
        self.model.snake.down()

    def handle_left(self):
        self.model.snake.left()

    def handle_right(self):
        self.model.snake.right()
