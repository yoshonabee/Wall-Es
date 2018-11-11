"""
Module Agent
"""

import math
import map


class Agent:
    def __init__(self, x, y, h, w, godmap):
        self.x = 0
        self.y = 0
        self.radius = 10
        self.velocity = 1
        self.breakTime = 0
        # Store self information on map
        self.map = map.AgentMap(h, w)
        # Use the god map to simulate discovering the unknown area
        self.godmap = godmap

    def move(self, dis):
        self.x += dis.x
        self.y += dis.y

    def observe(self):
        areas = []
        for h in self.map.height:
            for w in self.map.width:
                if math.sqrt(((self.x - w) * (self.x - w) +
                              (self.y - h) * (self.y - h)) < self.radius):
                    areas.append({"x": w, "y": h})
        for area in areas:
            self.map.areas[area.x][area.y] = self.godmap.answerArea(area)
