from itertools import count

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from tqdm import tqdm

from .agent import Agent
from .env import Env


class Train:
    def __init__(self):
        num_episodes = 100000  # 学習させるエピソード数

        n_frame = 1
        reward_clipping = True  # 報酬のクリッピング
        stage_size = 16  # ステージのサイズ

        num_episode_plot = torch.tensor([10])  # 何エピソードで学習の進捗を確認するか
        num_episode_save = 10  # 何エピソードでモデルを保存するか

        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

        def to_normalized_tensor(arr: np.ndarray) -> torch.Tensor:
            return torch.tensor((arr - arr.min()) / (arr.max() - arr.min()))

        env = Env()
        agent = Agent(n_frame=n_frame, device=device, action_space=env.action_space)

        terminated = True
        frame1 = True
        total_steps = 0
        count_update = 0
        steps_done = 0
        reward_all = -num_episode_plot * 0.75 + 1
        reward_durations = []

        for i_episode in tqdm(range(num_episodes)):
            reward_frame = torch.tensor([0], dtype=torch.float32)
            if terminated == True:
                state_frame = torch.zeros((1, n_frame, stage_size, stage_size), dtype=torch.float32)
                next_state_frame = torch.zeros((1, n_frame, stage_size, stage_size), dtype=torch.float32)
                state, info = env.reset()
                t_state = to_normalized_tensor(state)
                state_frame[:, 0, :, :] = t_state
                next_state_frame[:, 0, :, :] = t_state

            for t in count():
                total_steps += 1
                action, eps_threshold = agent.e_greedy_select_action(state_frame, steps_done)
                steps_done += 1
                observation, reward, terminated, truncated, info = env.step(action)

                done = terminated or truncated

                t_reward = torch.tensor([reward])
                reward_all += t_reward
                if reward_clipping:  # 報酬のクリッピング
                    t_reward = torch.clamp(input=t_reward, min=-1, max=1)

                next_state = to_normalized_tensor(observation)
                # rollして一番古いフレームを新しいフレームで上書きする
                next_state_frame = torch.roll(input=next_state_frame, shifts=1, dims=1)
                next_state_frame[:, 0, :, :] = next_state

                if frame1 == True:
                    state_frame1 = state_frame
                    action_frame1 = action
                    next_state_frame1 = next_state_frame
                    if done:
                        next_state_frame1 = torch.zeros((1, n_frame, stage_size, stage_size), dtype=torch.float32)
                    frame1 = False

                reward_frame += t_reward

                if (total_steps % n_frame == 0) or done:
                    agent.push_memory(state_frame1, action_frame1, next_state_frame1, reward_frame)
                    frame1 = True
                    reward_frame = torch.tensor([0], dtype=torch.float32)

                    count_update += 1
                    if count_update % 4 == 0:
                        if count_update > agent.SIZE_REPLAY_MEMORY:
                            agent.update()
                    if count_update % 400 == 0:
                        agent.sync_target()

                state_frame = next_state_frame
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
        env.close()
