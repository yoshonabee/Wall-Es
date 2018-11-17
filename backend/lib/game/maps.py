"""
Module Map
"""

import random

"""
State enum. Robots are added at run time.
"""
State = {
    "empty": 0,
    "obstacle": -1,
    "target": -2,
    # "id1": id1,
    # "id2": id2,
    # ...
}

"""
The map of the game.
"""


class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.areas = [[State["empty"]
                       for x in range(self.width)] for y in range(self.height)]
        self.targets = []
        self.obstacles = []
        # agents is dict. In convenience for finding the certain one
        self.agents = {}

    def answerArea(self, area):
        return self.areas[area["x"]][area["y"]]


"""
God's map. God know every thing. 
"""


class GodMap(Map):

    def setObstacles(self, obstacles):
        self.obstacles = obstacles
        for obstacle in obstacles:
            self.areas[obstacle["x"]][obstacle["y"]] = State["obstacle"]

    def setTargets(self, targets):
        self.targets = targets
        for target in targets:
            self.areas[target["x"]][target["y"]] = State["target"]

    def setRandomObstables(self, obstacles_number):
        self.obstacles = []
        for i in range(0, obstacles_number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            obstacle = {"x": x, "y": y}
            self.obstacles.append(obstacle)
            self.areas[obstacle["x"]][obstacle["y"]] = State["obstacle"]

    def setRandomTargets(self, targets_number):
        self.targets = []
        for i in range(0, targets_number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            target = {"x": x, "y": y}
            self.targets.append(target)
            self.areas[target["x"]][target["y"]] = State["target"]



"""
The map for console. Collect information from all agents and give information
back to them.
"""


class ConsoleMap(Map):

    def setAgents(self, agents):
        self.agents = agents
        for id in agents:
            agent = agents[id]
            self.areas[agent.x][agent.y] = agent.id

    # update all agents position
    def updateAgents(self, agents):
        # clear origin
        for id in self.agents:
            agent = self.agents[id]
            self.areas[agent.x][agent.y] = State["empty"]
        # set new
        self.agents = agents
        for id in agents:
            agent = self.agents[id]
            self.areas[agent.x][agent.y] = agent.id

    # update a agent's position
    def updateAgent(self, agent):
        oldAgent = self.agents[agent.id]
        # clear origin
        self.areas[oldAgent.x][oldAgent.y] = State["empty"]
        # set new
        self.agents[agent.id] = agent
        self.areas[agent.x][agent.y] = agent.id

    # update targets information got from agent
    def updateTargets(self, targets):
        for target in targets:
            self.targets.append(target)
            self.areas[target["x"]][target["y"]] = State["target"]

    # update obstacles information got from agent
    def updateObstacles(self, obstacles):
        for obstable in obstacles:
            self.obstacles.append(obstable)
            self.areas[obstable["x"]][obstable["y"]] = State["obstacle"]
