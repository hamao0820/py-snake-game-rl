import numpy as np
import PIL.Image as Image

from game.model import Model
from game.direction import Right, Left, Up, Down

from .action_space import Action, ActionSpace


class Env:
    def __init__(self) -> None:
        self._action_space = ActionSpace()
        self.frames: list[np.ndarray] = []
        self.actions: list[Action] = []
        return

    def reset(self) -> tuple[np.ndarray, dict]:
        self.model = Model()
        array = self._get_state()
        self.frames = [self.to_image(self.model.board)]
        self.actions = []
        return array, {}

    def step(self, action: Action) -> tuple[np.ndarray, float, bool, bool, dict]:
        if action == Action.STRAIGHT:
            self.model.snake.straight()
        elif action == Action.TURN_RIGHt:
            self.model.snake.turn_right()
        elif action == Action.TURN_LEFT:
            self.model.snake.turn_left()
        else:
            raise ValueError("Invalid action")

        self.model.update()
        self.frames.append(self.to_image(self.model.board))
        self.actions.append(action)

        try:
            observation = self._get_state()
        except IndexError:
            observation = np.zeros((1, 16 * 16 * 3 + 4 + 4 + 3), dtype=np.uint8)
        terminated = self.model.is_game_over()
        truncated = False
        reward = min(1, self.model.score.score / 30)
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

    def _get_state(self) -> np.ndarray:
        food_one_hot = np.zeros((len(self.model.board), len(self.model.board[0])), dtype=np.uint8)
        food_one_hot[self.model.food.pos.y - 1][self.model.food.pos.x - 1] = 1
        head_one_hot = np.zeros((len(self.model.board), len(self.model.board[0])), dtype=np.uint8)
        head_one_hot[self.model.snake.head.y - 1][self.model.snake.head.x - 1] = 1
        body_one_hot = np.zeros((len(self.model.board), len(self.model.board[0])), dtype=np.uint8)
        for body in self.model.snake.body:
            body_one_hot[body.y - 1][body.x - 1] = 1
        direction_one_hot = np.array(
            [
                isinstance(self.model.snake.direction, Right),
                isinstance(self.model.snake.direction, Left),
                isinstance(self.model.snake.direction, Up),
                isinstance(self.model.snake.direction, Down),
            ],
            dtype=np.uint8,
        )
        food_direction_one_hot = np.array(
            [
                self.model.food.pos.x > self.model.snake.head.x,
                self.model.food.pos.x < self.model.snake.head.x,
                self.model.food.pos.y > self.model.snake.head.y,
                self.model.food.pos.y < self.model.snake.head.y,
            ],
            dtype=np.uint8,
        )

        danger_one_hot = np.array(
            [
                self.model.snake.can_turn_left,
                self.model.snake.can_turn_right,
                self.model.snake.can_straight,
            ],
            dtype=np.uint8,
        )

        state = np.expand_dims(
            np.concatenate(
                [
                    food_one_hot.flatten(),
                    head_one_hot.flatten(),
                    body_one_hot.flatten(),
                    direction_one_hot,
                    food_direction_one_hot,
                    danger_one_hot,
                ],
                axis=0,
            ),
            axis=0,
        )

        return state

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
