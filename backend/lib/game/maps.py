"""
Module BaseMap
"""

import random
import numpy as np
"""
State enum. Robots are added at run time.
"""
State = {
    "emptyWhite": -3,
    "emptyGray": -4,
    "obstacle": -1,
    "target": -2,
    # "id1": id1,
    # "id2": id2,
    # ...
}

"""
The map of the game.
"""


class BaseMap():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.areas = [[State["emptyWhite"]
                       for x in range(self.width)] for y in range(self.height)]
        self.targets = []
        self.obstacles = []
        # agents is dict. In convenience for finding the certain one
        self.agents = {}
        self.cluster = []

    def answerArea(self, area):
        return self.areas[area["y"]][area["x"]]


"""
God's map. God know every thing. 
"""


class GodMap(BaseMap):

    def setObstacles(self, obstacles):
        self.obstacles = obstacles
        for obstacle in obstacles:
            self.areas[obstacle["y"]][obstacle["x"]] = State["obstacle"]

    def setTargets(self, targets):
        self.targets = targets
        for target in targets:
            self.areas[target["y"]][target["x"]] = State["target"]

    def setRandomObstables(self, obstacles_number):
        self.obstacles = []
        for i in range(0, obstacles_number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            while self.areas[y][x] != State['emptyWhite']:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            obstacle = {"x": x, "y": y}
            self.obstacles.append(obstacle)
            self.areas[obstacle["y"]][obstacle["x"]] = State["obstacle"]

    def setRandomTargets(self, targets_number):
        self.targets = []
        for i in range(0, targets_number):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            while self.areas[y][x] != State['emptyWhite']:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

            target = {"x": x, "y": y}
            self.targets.append(target)
            self.areas[target["y"]][target["x"]] = State["target"]

"""
The map for console. Collect information from all agents and give information
back to them.
"""


class ConsoleMap(BaseMap):
    
    
    def setAgents(self, agents):
        self.agents = agents
        for id in agents:
            agent = agents[id]
            self.areas[agent.y][agent.x] = agent.id
            self.cluster.append([])

    # update all agents position
    def updateAgents(self, agents):
        self.agents = agents
        for id in agents:
            agent = self.agents[id]
            self.areas[agent.y][agent.x] = agent.id
            area = {"x": agent.x, "y": agent.y}
            if area in self.targets:
                print("find")
                self.targets.remove(area)

    # update a agent's position
    def updateAgent(self, agent):
        self.agents[agent.id] = agent
        self.areas[agent.y][agent.x] = agent.id
        area = {"x": agent.x, "y": agent.y}
        if area in self.targets:
            self.targets.remove(area)

    # update targets information got from agent
    def updateTargets(self, targets):
        for target in targets:
            if not target in self.targets:
                self.targets.append(target)
                self.areas[target["y"]][target["x"]] = State["target"]

    # update obstacles information got from agent
    def updateObstacles(self, obstacles):
        for obstable in obstacles:
            if not obstable in self.obstacles:
                self.obstacles.append(obstable)
                self.areas[obstable["y"]][obstable["x"]] = State["obstacle"]

    def updateObserveAreas(self, areas):
        for area in areas:
            self.areas[area["y"]][area["x"]] = State["emptyGray"]
    
    def targetclustering(self):
        agent_location = []
        dist = 0
        for id in self.agents:
            agent = self.agents[id]
            location= {"x": agent.x, "y": agent.y}
            agent_location.append(location)
        for target_id in self.targets:
            min_dist = 0
            min_ind = 0
            target = self.targets[target_id]
            for num in location:
                dist = np.sqrt(np.square(target["x"] - agent_location["x"]) + np.square(target["y"] - agent_location["y"]))
                if min_dist == 0 or dist < min_dist:
                    dist = min_dist
                    min_ind = num
            self.cluster[min_ind].append(target)
            
