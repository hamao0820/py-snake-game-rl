from itertools import count

import matplotlib.pyplot as plt
import numpy as np
import torch
from tqdm import tqdm

from .agent import Agent
from .env import Env


class Train:
    def __init__(self):
        num_episodes = 100000  # 学習させるエピソード数

        reward_clipping = True  # 報酬のクリッピング

        num_episode_plot = torch.tensor([300])  # 何エピソードで学習の進捗を確認するか
        num_episode_save = 100  # 何エピソードでモデルを保存するか

        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        device = torch.device("cpu")

        env = Env()
        agent = Agent(device=device, action_space=env.action_space)

        terminated = True
        total_steps = 0
        count_update = 0
        steps_done = 0
        reward_all = -num_episode_plot * 0.75 + 1
        reward_durations = []

        for i_episode in tqdm(range(num_episodes)):
            if terminated == True:
                state, info = env.reset()
                t_state = torch.tensor(state, dtype=torch.float)

            for t in count():
                total_steps += 1
                action, eps_threshold = agent.e_greedy_select_action(t_state, steps_done)
                t_action = torch.tensor([[action.value]])
                steps_done += 1
                observation, reward, terminated, truncated, info = env.step(action)
                t_observation = torch.tensor(observation, dtype=torch.float)
                done = terminated or truncated

                t_reward = torch.tensor([reward], dtype=torch.float)
                reward_all += t_reward
                if reward_clipping:  # 報酬のクリッピング
                    t_reward = torch.clamp(input=t_reward, min=-1, max=1)

                agent.push_memory(t_state, t_action, t_observation, t_reward)

                t_state = t_observation

                count_update += 1
                if count_update % 4 == 0:
                    if count_update > agent.SIZE_REPLAY_MEMORY:
                        agent.update()
                if count_update % 400 == 0:
                    agent.sync_target()

                if done:
                    break
            if i_episode % num_episode_plot == 0:
                reward_durations.append(reward_all / num_episode_plot)
                plt.figure(1)
                plt.clf()
                plt.xlabel("Episode")
                plt.ylabel("Reward")
                plt.plot(
                    np.arange(0, (i_episode / num_episode_plot + 1) * num_episode_plot, num_episode_plot),
                    torch.tensor(reward_durations, dtype=torch.float).numpy(),
                )
                plt.savefig(f"progress/reward_duration.png")
                plt.clf()

                if (i_episode % num_episode_save) == 0:
                    agent.save()
                    env.render()

        agent.save()
        env.render()
