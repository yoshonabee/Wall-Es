"""
Module Map
"""


"""
State enum. Robots are added at run time.
"""
state = {
    "empty": 0,
    "obstacle": -1,
    # "robot1": id1,
    # "robot2": id2,
    # ...
}

"""
The map of the game.
"""


class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.areas = [[state["empty"]
                       for x in range(self.width)] for y in range(self.height)]
        self.targets = []
        self.agents = []
        self.obstacles = []


"""
God's map. God know every thing. 
"""


class GodMap(Map):

    def __init__(self, height, width):
        pass

    def setObstables(self, obstacles):
        self.obstacles = obstacles
        for obstacle in obstacles:
            self.areas[obstacle.x][obstacle.y] = state["obstable"]

    def setAgents(self, agents):
        self.agents = agents
        for agent in agents:
            self.areas[agent.x][agent.y] = agent.id

    def answerArea(self, pos):
        return self.areas[pos.x][pos.y]


"""
The map for console. Collect information from all agents and give information
back to them.
"""


class ConsoleMap(Map):

    def __init__(self, height, width):
        pass

    def setObstables(self, obstacles):
        self.obstacles = obstacles
        for obstacle in obstacles:
            self.areas[obstacle.x][obstacle.y] = state["obstable"]

    def updateAgent(self, agents):
        self.agents = agents
        for agent in agents:
            self.areas[agent.x][agent.y] = agent.id

    def answerArea(self, pos):
        return self.areas[pos.x][pos.y]


"""
The map for agent.
"""


class AgentMap(Map):

    def __init__(self, height, width):
        self.agent = {}

    def setAgentSelf(self, agent):
        self.agent = agent
