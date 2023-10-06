import torch
import torch.nn as nn


class Dueling_Network(nn.Module):
    def __init__(self, n_actions) -> None:
        super(Dueling_Network, self).__init__()
        self.relu = nn.ReLU()
        self.leaner1 = nn.Linear(1547, 256)  # 16 * 16 * 6 + 4 + 4 + 3
        self.act_fc = nn.Linear(256, 64)
        self.act_fc2 = nn.Linear(64, n_actions)
        self.value_fc = nn.Linear(256, 64)
        self.value_fc2 = nn.Linear(64, 1)
        torch.nn.init.kaiming_normal_(self.leaner1.weight)
        torch.nn.init.kaiming_normal_(self.act_fc.weight)
        torch.nn.init.kaiming_normal_(self.act_fc2.weight)
        torch.nn.init.kaiming_normal_(self.value_fc.weight)
        torch.nn.init.kaiming_normal_(self.value_fc2.weight)
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.relu(self.leaner1(x))
        x_act = self.relu(self.act_fc(x))
        x_act = self.act_fc2(x_act)
        x_val = self.relu(self.value_fc(x))
        x_val = self.value_fc2(x_val)
        x_act_ave = torch.mean(x_act, dim=1, keepdim=True)
        q = x_val + x_act - x_act_ave
        return q
