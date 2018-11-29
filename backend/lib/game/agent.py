"""
Module Agent
"""

import math
from maps import State


class Agent:
    def __init__(self, id, x, y, h, w, r=5):
        self.id = id
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.radius = r

    def move(self, dx, dy, consolemap):
        x = self.x + dx
        y = self.y + dy
        if not ((x > 0 and x < self.width) and ( y > 0 and y < self.height)):
            raise Exception('Move out boundary!')
        if consolemap.areas[y][x] is State["obstacle"]:
            raise Exception('Move to obstacle!')
        consolemap.areas[self.y][self.x] = State["emptyGray"]
        self.x = x
        self.y = y

    """
    Use GodMap to get the area data in which the agent is observing.
    """

    def observe(self, godmap):
        areas = []
        newTargets = []
        newObstacles = []
        newObserveAreas = []
        # search area in agent's vision
        for h in range(0, godmap.height):
            for w in range(0, godmap.width):
                if math.sqrt(((self.x - w) * (self.x - w) +
                              (self.y - h) * (self.y - h))) < self.radius:
                    areas.append({"x": w, "y": h})
        # ask god to simulate observing
        for area in areas:
            state = godmap.answerArea(area)
            if(state is State["target"]):
                newTargets.append(area)
                if area in godmap.targets:
                    godmap.targets.remove(area)
                    godmap.areas[area["y"]][area["x"]] = State["emptyGray"]
            elif(state is State["obstacle"]):
                newObstacles.append(area)
                if area in godmap.obstacles:
                    godmap.obstacles.remove(area)
                    godmap.areas[area["y"]] [area["x"]]= State["emptyGray"]
            elif(state is State["emptyWhite"]):
                newObserveAreas.append(area)
                godmap.areas[area["y"]][area["x"]] = State["emptyGray"]
        return (newObserveAreas, newTargets, newObstacles)
