import numpy as np
import PIL.Image as Image

from game.controller import Controller
from game.model import Model

from .action_space import Action, ActionSpace


class Env:
    def __init__(self) -> None:
        self._action_space = ActionSpace()
        self.frames: list[np.ndarray] = []
        self.actions: list[Action] = []
        self.prev_score = 0
        return

    def reset(self) -> tuple[np.ndarray, dict]:
        self.model = Model()
        self.controller = Controller(self.model)
        array = np.array(self.model.board)
        self.frames = [self.to_image(self.model.board)]
        self.actions = []
        return array, {}

    def step(self, action: Action) -> tuple[np.ndarray, float, bool, bool, dict]:
        if action == Action.Up:
            self.controller.handle_up()
        elif action == Action.Right:
            self.controller.handle_right()
        elif action == Action.Down:
            self.controller.handle_down()
        elif action == Action.Left:
            self.controller.handle_left()
        else:
            raise ValueError("Invalid action")

        self.model.update()
        self.frames.append(self.to_image(self.model.board))
        self.actions.append(action)

        observation = np.array(self.model.board)
        terminated = self.model.is_game_over()
        truncated = False
        reward = self.model.score.score - self.prev_score
        if self.model.game_over:
            reward = -1

        return observation, reward, terminated, truncated, {}

    def to_image(self, board: list[list[int]]) -> np.ndarray:
        image = np.zeros((len(board), len(board[0]), 3), dtype=np.uint8)
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.model.board[i][j] == 1:
                    image[i][j] = [0, 0, 255]
                elif self.model.board[i][j] == 2:
                    image[i][j] = [0, 255, 0]
                elif self.model.board[i][j] == 3:
                    image[i][j] = [255, 0, 0]
        return image

    def render(self, fname: str = "snake-game") -> None:
        images = [Image.fromarray(frame) for frame in self.frames]
        images[0].save(
            f"img/{fname}.gif",
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )
        f = open("actions/list.txt", "w")
        for x in self.actions:
            f.write(str(x) + "\n")
        f.close()

    @property
    def action_space(self) -> ActionSpace:
        return self._action_space
