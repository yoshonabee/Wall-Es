import os
import glob
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class ActorCritic(nn.Module):
    def __init__(self, height = 128, width = 128):
        super(ActorCritic, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, stride=1, padding=2) # 1*n*n -> 32*(n+2)*(n+2)
        self.maxp1 = nn.MaxPool2d(2, 2) # -> 32*(n/2 + 1)*(n/2 + 1)
        self.conv2 = nn.Conv2d(32, 32, 3, stride=1, padding=1) # -> 32*(n/2 + 1)*(n/2 + 1)
        self.maxp2 = nn.MaxPool2d(2, 2) # -> 32*(n/4)*(n/4)
        self.conv3 = nn.Conv2d(32, 64, 3, stride=1, padding=1) # -> 64*(n/4)*(n/4)
        self.maxp3 = nn.MaxPool2d(2, 2) # -> 64*(n/8)*(n/8)
        self.conv4 = nn.Conv2d(64, 64, 3, stride=1, padding=1) # -> 64*(n/8)*(n/8)
        self.maxp4 = nn.MaxPool2d(2, 2) # -> 64*(n/16)*(n/16)
        # 64 * 16 * 16
        self.avgp = nn.AvgPool2d(height//16//4, width//16//4)
        # self.avgp = nn.AveragePool2d(height//16, width//16, stride=1, padding=1)

        self.lstm = nn.LSTMCell(1024, 512)
        self.critic_linear = nn.Linear(512, 1)
        self.actor_linear = nn.Linear(512, 5)

    def forward(self, inputs, hx, cx):
        x = F.relu(self.maxp1(self.conv1(inputs)))
        x = F.relu(self.maxp2(self.conv2(x)))
        x = F.relu(self.maxp3(self.conv3(x)))
        x = F.relu(self.maxp4(self.conv4(x)))
        x = self.avgp(x)
        x = x.view(x.size(0), -1)

        hx, cx = self.lstm(x, (hx, cx))

        return self.critic_linear(hx).view(-1), self.actor_linear(hx), (hx, cx)
