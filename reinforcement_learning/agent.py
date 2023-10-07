import math
import random

import torch
import torch.nn as nn
import torch.optim as optim

from .action_space import Action, ActionSpace
from .nnet import Dueling_Network
from .replay_memory import ReplayMemory, Transition

from typing import Literal


class Agent:
    GAMMA = 0.99
    EPS_START = 0.15
    EPS_END = 0.01
    EPS_DECAY = 100000
    SIZE_REPLAY_MEMORY = 1000
    BATCH_SIZE = 32
    TAU = 0.005
    LR = 1e-4

    def __init__(
        self,
        device: torch.device,
        action_space: ActionSpace,
        state_dict_path: str | None = None,
        mode: Literal["train"] | Literal["predict"] = "train",
    ):
        self.device = device
        self.action_space = action_space
        self.policy_net = Dueling_Network(n_actions=self.action_space.n).to(device)
        self.target_net = Dueling_Network(n_actions=self.action_space.n).to(device)
        if state_dict_path is not None:
            self.policy_net.load_state_dict(torch.load(state_dict_path))
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.memory = ReplayMemory(Agent.SIZE_REPLAY_MEMORY)
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=Agent.LR, amsgrad=True)
        self.mode = mode
        if self.mode == "predict":
            self.policy_net.eval()
            self.target_net.eval()

    def e_greedy_select_action(self, state: torch.Tensor, steps_done) -> tuple[Action, float]:
        eps_threshold = Agent.EPS_END + (Agent.EPS_START - Agent.EPS_END) * math.exp(
            -1.0 * steps_done / Agent.EPS_DECAY
        )
        steps_done += 1

        if random.random() > eps_threshold:
            with torch.no_grad():
                return (
                    self.action_space.action_space[
                        self.policy_net(state.to(self.device)).argmax().view(1, 1).cpu().item()
                    ],
                    eps_threshold,
                )
        return (
            self.action_space.action_space[torch.tensor([[random.randint(0, self.action_space.n - 1)]]).item()],
            eps_threshold,
        )

    def select_action(self, state: torch.Tensor) -> Action:
        with torch.no_grad():
            return self.action_space.action_space[self.policy_net(state.to(self.device)).argmax().view(1, 1).item()]

    def update(self) -> None:
        if len(self.memory) < Agent.BATCH_SIZE:
            return
        transitions = self.memory.sample(Agent.BATCH_SIZE)
        batch = Transition(*zip(*transitions))
        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)), device=self.device, dtype=torch.bool
        )
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        state_batch = torch.cat(batch.state).to(self.device)
        action_batch = torch.cat(batch.action).to(self.device)
        reward_batch = torch.cat(batch.reward).to(self.device)

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)
        next_state_values = torch.zeros(Agent.BATCH_SIZE, device=self.device)

        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states.to(self.device)).max(1)[0]

        expected_state_action_values = (next_state_values * Agent.GAMMA) + reward_batch

        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 1000)
        self.optimizer.step()

    def push_memory(self, *args) -> None:
        self.memory.push(*args)

    def sync_target(self) -> None:
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key] * Agent.TAU + target_net_state_dict[key] * (
                1 - Agent.TAU
            )
        self.target_net.load_state_dict(target_net_state_dict)

    def save(self, fname: str = "snake-game") -> None:
        torch.save(self.target_net.state_dict(), f"model_weights/{fname}_target.pth")
        torch.save(self.policy_net.state_dict(), f"model_weights/{fname}_policy.pth")
