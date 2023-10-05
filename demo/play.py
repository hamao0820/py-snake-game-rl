import os

from pynput.keyboard import Key, Listener

from game.controller import Controller
from game.model import Model
from game.stage import Stage


class Game:
    def __init__(self) -> None:
        self.model = Model()
        self.controller = Controller(self.model)

    def start(self) -> None:
        display_board(self.model.snake, self.model.food)
        while not self.model.is_game_over():
            self.step()
            display_board(self.model.snake, self.model.food)

    def step(self) -> None:
        def on_press(key):
            if key == Key.up:
                self.controller.handle_up()
            elif key == Key.down:
                self.controller.handle_down()
            elif key == Key.left:
                self.controller.handle_left()
            elif key == Key.right:
                self.controller.handle_right()
            else:
                print("Invalid input")

        def on_release(key):
            return False

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        self.model.update()


def display_board(snake, food):
    """
    盤面をterminalに表示する

    Args:
      snake: Snakeクラスのインスタンス
      food: Foodクラスのインスタンス

    Returns:
      なし
    """

    os.system("clear")

    # 盤面を初期化
    # fix
    board = [["･" for _ in range(Stage.WIDTH + 2)] for _ in range(Stage.HEIGHT + 2)]
    # board = [["･"] * Stage.WIDTH + 2 for _ in range(Stage.HEIGHT + 2)]

    # ヘビを表示
    board[snake.head.y][snake.head.x] = "H"
    for body in snake.body:
        board[body.y][body.x] = "S"

    # 餌を表示
    board[food.pos.y][food.pos.x] = "*"

    # 盤面の外側を壁で囲む
    for i in range(len(board)):
        board[i][0] = "#"
        board[i][-1] = "#"
    for i in range(len(board[0])):
        board[0][i] = "#"
        board[-1][i] = "#"

    # 盤面を表示
    for line in board:
        print("".join(line))


if __name__ == "__main__":
    game = Game()
    game.start()
