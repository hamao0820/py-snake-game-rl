import numpy as np

from game.controller import Controller
from game.model import Model

from .action_space import Action, ActionSpace


class Env:
    def __init__(self) -> None:
        self._action_space = ActionSpace()
        self.frames: list[np.ndarray] = []
        self.prev_score = 0
        return

    def reset(self) -> tuple[np.ndarray, dict]:
        self.model = Model()
        self.controller = Controller(self.model)
        array = np.array(self.model.board)
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

        observation = np.array(self.model.board)
        terminated = self.model.is_game_over()
        truncated = False
        reward = self.model.score.score - self.prev_score
        if self.model.game_over:
            reward = -1

        return observation, reward, terminated, truncated, {}

    def render(self, fname: str = "snake-game") -> None:
        pass

    @property
    def action_space(self) -> ActionSpace:
        return self._action_space
