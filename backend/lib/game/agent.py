"""
Module Agent
"""

import math
from lib.game.maps import State


class Agent:
    def __init__(self, id, x, y, h, w, r=5):
        self.id = id
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        self.radius = r
        self.active = True

    def move(self, dx, dy, consolemap):
        if(self.active):
            try_x = self.x + dx
            try_y = self.y + dy
            update_check = True
            #out of the map check
            if (try_x < 0 or try_x >= self.width) or (try_y < 0 or try_y >= self.height):
                self.active = False
                update_check = False
                x = self.x
                y = self.y

            if update_check:
                #obstacle crash check
                if consolemap.areas[try_y][try_x] is State["obstacle"]:
                    self.active = False
                    update_check = False
                    x = self.x
                    y = self.y

                #collision crash check
                for i in range(len(consolemap.agents)):
                    if self.id == i:
                        continue
                    else:
                        if try_x == consolemap.agents[i].x and try_y == consolemap.agents[i].y:
                            self.active = False
                            consolemap.agents[i].active = False
                            update_check = False
                            x = self.x
                            y = self.y
                            break

            consolemap.areas[self.y][self.x] = State["emptyGray"]

            if update_check:
                x = try_x
                y = try_y

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

    def state(self):
        return self.active
