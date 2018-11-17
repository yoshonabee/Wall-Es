"""
Module Agent
"""

import math
from maps import State


class Agent:
    def __init__(self, id, x, y, h, w, r=20, v=1, b=0):
        self.id = id
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.radius = r
        self.velocity = v
        self.breakTime = b

    def move(self, dx, dy):
        x = self.x + dx
        y = self.y + dy
        if x > 0 and x < self.width:
            self.x = x
        if y > 0 and y < self.height:
            self.y = y

    """
    Use GodMap to get the area data in which the agent is observing.
    """

    def observe(self, godmap):
        areas = []
        newTargets = []
        newObstacles = []
        # search area in agent's vision
        for h in range(0, godmap.height):
            for w in range(0, godmap.width):
                if math.sqrt(((self.x - w) * (self.x - w) +
                              (self.y - h) * (self.y - h)) < self.radius):
                    areas.append({"x": w, "y": h})
        # ask god to simulate observing
        for area in areas:
            state = godmap.answerArea(area)
            if(state is State["target"]):
                newTargets.append(area)
            elif(state is State["obstacle"]):
                newObstacles.append(area)
        return (newTargets, newObstacles)
