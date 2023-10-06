from itertools import count

import torch

from .agent import Agent
from .env import Env

from tqdm import tqdm


class Predictor:
    def __init__(self):
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

        self.env = Env()
        self.agent = Agent(
            device=device,
            action_space=self.env.action_space,
            mode="predict",
            state_dict_path="model_weights/9ff7f581fbb3c9b5492da245ab996b1caef239ff/snake-game_policy.pth",
        )

    def run(self, num_episodes: int = 1):
        max_score = 0
        for i in tqdm(range(num_episodes)):
            state, info = self.env.reset()
            t_state = torch.tensor(state, dtype=torch.float)
            total_reward = 0
            for t in count():
                action = self.agent.select_action(t_state)
                observation, reward, terminated, truncated, info = self.env.step(action, t)
                t_observation = torch.tensor(observation, dtype=torch.float)
                done = terminated or truncated

                t_state = t_observation
                total_reward += reward

                if done:
                    break

            if self.env.model.score.score > max_score:
                max_score = self.env.model.score.score
                tqdm.write(f"max_score: {max_score}")
                self.env.render(fname="9ff7f581fbb3c9b5492da245ab996b1caef239ff.png")
