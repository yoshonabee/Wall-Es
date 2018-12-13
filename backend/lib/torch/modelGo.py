import os
import torch
import numpy as np

from lib.torch.model import ActorCritic
from lib.torch.command import Command


class modelGo():
    def __init__(self, agent_num = 5, model_structure = ActorCritic(128, 128), model_weight = '../lib/torch/state_dict/weight.pkl'):
        self.model = model_structure
        self.model_weight = model_weight

        self.loadWeight()

        self.agent_numbers = agent_num

        self.bot_observe = None
        self.hx = torch.zeros([self.agent_numbers, 512], dtype=torch.float32)
        self.cx = torch.zeros([self.agent_numbers, 512], dtype=torch.float32)

    def loadWeight(self):
        if os.path.exists(self.model_weight):
            self.model.load_state_dict(torch.load(self.model_weight, map_location='cpu'))
        else:
            print('Model weight [{0}] not found'.format(self.model_weight))
        return

    def observe(self, image_list):
        self.bot_observe = np.array(image_list).astype(np.uint8)
        self.bot_observe = torch.from_numpy(self.bot_observe).float()

    def action(self):
        critic_score, bot_command, (self.hx, self.cx) = self.model(self.bot_observe, self.hx, self.cx)
        commands = self.interpretAction(bot_command)

        return commands

    def interpretAction(self, command_tensor):
        command_tensor = command_tensor.view(-1, 5)
        command = torch.max(command_tensor, 1)[1].tolist()
        commands = [self.intoCommand(i, command[i]) for i in range(len(command))]
        return commands

    def intoCommand(self, i, command):
        if command == 0: return Command(i, 0, 1)
        elif command == 1: return Command(i, 1, 0)
        elif command == 2: return Command(i, 0, -1)
        elif command == 3: return Command(i, -1, 0)
        return Command(i, 0, 0)
