from lib.game.maps import GodMap, ConsoleMap, State
from lib.game.agent import Agent

from lib.torch.model import ActorCritic
from lib.torch.modelGo import modelGo

import random
import numpy as np
import json


class Game():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        #initial round of the game
        self.round = -1

        self.modelGo = modelGo()

        # godmap will be asked when agent observing
        # only god knows target and obstacles at the beginning
        self.godmap = GodMap(height, width)

        # console always knows where agents are
        # console will update targets and obstacles when agents find them
        self.consolemap = ConsoleMap(height, width)

    def getmap(self):
        return self.consolemap.areas
    
    def setAgents(self, agents):
        self.consolemap.setAgents(agents)
        self.agents_number = len(agents)

    def setObstacles(self, obstacles):
        self.godmap.setObstacles(obstacles)

    def setTargets(self, targets):
        self.godmap.setTargets(targets)
        self.targets_number = len(targets)

    def setScore(self, acquired_target_sum = 100, time_decrease = -0.1):
        self.acquired_target_sum = acquired_target_sum
        self.time_decrease = time_decrease

    def setRandomMap(self, agents_number, targets_number, obstacles_number):
        self.godmap.setRandomObstables(obstacles_number)
        self.godmap.setRandomTargets(targets_number)
        self.agents_number = agents_number
        self.targets_number = targets_number
        agents = {}
        xy_temp = []
        for id in range(0, agents_number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            while (x, y) in xy_temp:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            xy_temp.append((x, y))
            agent = Agent(id, x, y, self.height, self.width)
            agents[id] = agent
        self.setAgents(agents)

    def runOneRound(self, commands):
        self.round += 1
        for command in commands:
            agent = self.consolemap.agents[command.id]
            agent.move(command.dx, command.dy, self.consolemap)
            (areas, foundTargets, foundObstacles) = agent.observe(self.godmap)
            self.consolemap.updateObserveAreas(areas)
            self.consolemap.updateTargets(foundTargets)
            self.consolemap.updateObstacles(foundObstacles)
            self.consolemap.updateAgent(agent) # must at the end
            print("agent%d position:(%d,%d)" %(agent.id,agent.x,agent.y))
        
    def runOneRoundwithoutMovement(self):
        self.round += 1
        commands = []
        for id in self.consolemap.agents:
            commands.append(Command(id, 0, 0))
        self.runOneRound(commands)

    def getScore(self):
        collected_targets_ratio = 1 - (len(self.godmap.targets) + len(self.consolemap.targets)) / self.targets_number

        return self.acquired_target_sum * collected_targets_ratio + self.time_decrease * self.round

    def printConsoleInfo(self):
        agents = []
        for id in self.consolemap.agents:
            agent = self.consolemap.agents[id]
            agents.append({"id": agent.id, "x": agent.x, "y": agent.y})
        print("Console: agents")
        print(agents)
        print("Console: found targets")
        print(self.consolemap.targets)
        print("Console: found obstacles")
        print(self.consolemap.obstacles)

    def printGodInfo(self):
        print("God: targets:")
        print(self.godmap.targets)
        print("God: obstacles")
        print(self.godmap.obstacles)

    def outputAgentImage(self, agentId):
        map = np.zeros((self.width, self.height, 3))
        image = np.zeros((3, self.width, self.height))
        for x in range(0, self.width):
            for y in range(0, self.height):
                area = self.consolemap.areas[y][x]
                if area is agentId:
                    map[(y, x)] = [0, 102, 255]  # blue, this agent
                elif area is State["emptyWhite"]:
                    map[(y, x)] = [255, 255, 255]  # white
                elif area is State["emptyGray"]:
                    map[(y, x)] = [204, 204, 204]  # gray
                elif area is State["target"]:
                    map[(y, x)] = [255, 51, 0]  # red
                elif area is State["obstacle"]:
                    map[(y, x)] = [0, 0, 0]  # black
                else:
                    map[(y, x)] = [51, 204, 51]  # green, other agents

        for i in range(3):
            image[i, :, :] = map[:, :, i]

        return image

    def outputGodImage(self):
        map = np.zeros((self.width, self.height, 3))
        for y in range(0, self.height):
            for x in range(0, self.width):
                area = self.godmap.areas[y][x]
                if area is State["emptyWhite"]:
                    map[(y, x)] = [255, 255, 255]  # white
                elif area is State["target"]:
                    map[(y, x)] = [255, 51, 0]  # red
                elif area is State["obstacle"]:
                    map[(y, x)] = [0, 0, 0]  # black
        return map

    def printGodMap(self):
        print("<- God Map ->")
        for y in range(0, self.height):
            row = ""
            for x in range(0, self.width):
                area = self.godmap.areas[y][x]
                if area is State["emptyWhite"]:
                    row += "█"
                elif area is State["target"]:
                    row += "◪"
                elif area is State["obstacle"]:
                    row += "X"
            print(row)

    def printConsoleMap(self):
        print("<- Console Map ->")
        for y in range(0, self.height):
            row = ""
            for x in range(0, self.width):
                area = self.consolemap.areas[y][x]
                if area is State["emptyWhite"]:
                    row += "█"
                elif area is State["emptyGray"]:
                    row += "░"
                elif area is State["target"]:
                    row += "◪"
                elif area is State["obstacle"]:
                    row += "X"
                else:
                    row += str(area)
            print(row)

    def torchNext(self):
        bot_observe = [self.outputAgentImage(i) for i in range(self.agents_number)]
        self.modelGo.observe(bot_observe)

        commands = self.modelGo.action()

        self.runOneRound(commands)

    def jsonMap(self):
        return json.dumps(self.consolemap.areas)

class Command():
    def __init__(self, id, dx, dy):
        self.id = id
        self.dx = dx
        self.dy = dy
