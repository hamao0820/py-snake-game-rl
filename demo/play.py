import os

from pynput.keyboard import Listener

from game.model import Model
from game.stage import Stage

from .controller import Controller


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
        with Listener(on_press=self.controller.on_press, on_release=self.controller.on_release) as listener:
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
