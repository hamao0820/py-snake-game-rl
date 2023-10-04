import os

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
        while True:
            match input("Enter action:\n0: Up 1: Down 2: Left 3: Right\ninput: "):
                case "0":
                    self.controller.handle_up()
                    break
                case "1":
                    self.controller.handle_down()
                    break
                case "2":
                    self.controller.handle_left()
                    break
                case "3":
                    self.controller.handle_right()
                    break
                case _:
                    print("Invalid input")
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
