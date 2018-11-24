from game import Game, Command
from agent import Agent

def testManualGameImageOutput1():
    print("\n== init manual setting game ==")
    height = 10
    width = 10
    game = Game(height, width)

    obstacles = [
        {"x": 1, "y": 1}, {"x": 2, "y": 2}, {"x": 3, "y": 3}
    ]
    targets = [
        {"x": 4, "y": 4}, {"x": 5, "y": 5}, {"x": 6, "y": 6}
    ]
    game.setObstacles(obstacles)
    game.setTargets(targets)

    game.printGodMap()

    agents = {
        0: Agent(0, 7, 6, height, width, r=3), # id, x, y, height, width
    }
    game.setAgents(agents)

    game.printConsoleMap()

    print("\n== 1st round ==")
    game.runOneRound([Command(0, -1, -1)]) # (6, 5)
    game.printConsoleMap()

    print("\n== 2st round ==")
    game.runOneRound([Command(0, -1, 0)]) # (5, 5)
    game.printConsoleMap()

    print("\n== 3st round ==")
    game.runOneRound([Command(0, -1, 0)]) #(4, 5)
    game.printConsoleMap()

def testManualGameImageOutput2():
    print("\n== init manual setting game ==")
    height = 20
    width = 20
    game = Game(height, width)

    game.setRandomMap(0, 20, 0) # numbers of agents, targets, obstacles


    game.printGodMap()

    agents = {
        0: Agent(0, 0, 0, height, width, r=5), # id, x, y, height, width
        1: Agent(1, 0, 10, height, width, r=5), # id, x, y, height, width
        2: Agent(2, 19, 19, height, width, r=5), # id, x, y, height, width
    }
    game.setAgents(agents)

    game.printConsoleMap()

    for i in range(0, 10):
        print("\n== %dst round ==" % i)
        game.runOneRound([Command(0, 1, 1), Command(1, 1, 0), Command(2, -1, -1)])
        game.printConsoleMap()

testManualGameImageOutput1()
testManualGameImageOutput2()

