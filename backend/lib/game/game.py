from maps import GodMap, ConsoleMap
from agent import Agent
import random


class Game():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        # godmap will be asked when agent observing
        # only god knows target and obstacles at the beginning
        self.godmap = GodMap(height, width)

        # console always knows where agents are
        # console will update targets and obstacles when agents find them
        self.consolemap = ConsoleMap(height, width)

    def setAgents(self, agents):
        self.consolemap.setAgents(agents)

    def setObstacles(self, obstacles):
        self.godmap.setObstacles(obstacles)

    def setTargets(self, targets):
        self.godmap.setTargets(targets)

    def setRandomMap(self, agents_number, targets_number, obstacles_number):
        self.godmap.setRandomObstables(obstacles_number)
        self.godmap.setRandomTargets(targets_number)
        agents = {}
        for id in range(0, agents_number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            agent = Agent(id, x, y, self.height, self.width)
            agents[id] = agent
        self.setAgents(agents)

    def runOneRound(self, commands):
        for command in commands:
            agent = self.consolemap.agents[command.id]
            agent.move(command.dx, command.dy)
            (foundTargets, foundObstacles) = agent.observe(self.godmap)
            self.consolemap.updateTargets(foundTargets)
            self.consolemap.updateObstacles(foundObstacles)
            self.consolemap.updateAgent(agent)

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


class Command():
    def __init__(self, id, dx, dy):
        self.id = id
        self.dx = dx
        self.dy = dy
