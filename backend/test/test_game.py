import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from lib.game.game import Game, Command
from lib.game.agent import Agent

from lib.torch.model import ActorCritic
from lib.torch.modelGo import modelGo

def torchGame():
    print("\n== init random game ==")
    game = Game(128, 128)  # height, width
    t = 128 + 128 / 2

    game.setRandomMap(5, int(t * 0.3) ** 2, int(t * 0.1) ** 2)
    # numbers of agents, targets, obstacles

    #game.printGodInfo()

    print("\n== 1st round ==")

    game.torchNext()

    print("\n== 2ed round ==")
    game.torchNext()

def randomGame():
    print("\n== init random game ==")
    game = Game(20, 20)  # height, width
    game.setRandomMap(3, 3, 4)  # numbers of agents, targets, obstacles

    game.printGodInfo()

    print("\n== 1st round ==")
    commands = []
    commands.append(Command(0, 1, 1))  # id, dx, dy
    commands.append(Command(1, -1, 1))
    commands.append(Command(2, 1, -1))

    game.runOneRound(commands)

    game.printConsoleInfo()

    print("\n== 2ed round ==")
    commands = []
    commands.append(Command(0, 1, 1))
    commands.append(Command(1, -1, 1))
    commands.append(Command(2, 1, -1))

    game.runOneRound(commands)

    game.printConsoleInfo()

def manualGame():
    print("\n== init manual setting game ==")
    height = 20
    width = 20
    game = Game(height, width)

    obstacles = [
        {"x": 1, "y": 1}, {"x": 2, "y": 2}, {"x": 3, "y": 3}
    ]
    targets = [
        {"x": 10, "y": 10}, {"x": 12, "y": 12}, {"x": 13, "y": 13}
    ]
    game.setObstacles(obstacles)
    game.setTargets(targets)

    agents = {
        0: Agent(0, 4, 4, height, width),  # id, x, y, height, width
        1: Agent(1, 15, 17, height, width),
        2: Agent(2, 12, 15, height, width),
    }
    game.setAgents(agents)

    game.printGodInfo()

    print("\n== 1st round ==")
    commands = []
    commands.append(Command(0, 1, 1))  # id, dx, dy
    commands.append(Command(1, -1, 1))
    commands.append(Command(2, 1, -1))

    game.runOneRound(commands)

    game.printConsoleInfo()

    print("\n== 2ed round ==")
    commands = []
    commands.append(Command(0, 1, 1))
    commands.append(Command(1, -1, 1))
    commands.append(Command(2, 1, -1))

    game.runOneRound(commands)

    game.printConsoleInfo()


randomGame()
manualGame()
torchGame()
