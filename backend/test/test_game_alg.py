import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np

from lib.game.game import Game, Command
from lib.game.agent import Agent
from lib.algorithmn.alg1 import haveunseenspace, alg_next


def testManualGameImageOutput2():
    print("\n== init manual setting game ==")
    height = 40
    width = 40
    crash = 0
    
    
    game = Game(height, width)

    game.setRandomMap(0, 300, 50) # numbers of agents, targets, obstacles


    game.printGodMap()

    agents = {
        0: Agent(0, 0, 0, height, width, r=5), # id, x, y, height, width
        1: Agent(1, width-1 , 0, height, width, r=5), # id, x, y, height, width
        2: Agent(2, 0 , height-1 , height, width, r=5), # id, x, y, height, width
        #3: Agent(3, width - 1, height- 1, height, width, r = 5)
    }
    
    game.setAgents(agents)
    ##########
    game.runOneRoundwithoutMovement()
    game.printConsoleMap()   
    round = 1
    
    while(game.consolemap.targets != [] or haveunseenspace(game.consolemap.areas, height, width)):
    #for round in range(1, 250):
        crash = alg_next(round, game, agents, crash)
        round += 1
    #print(np.sum(game.consolemap.areas))    
    print("crash time: %d" %crash)
    print("finish")
        
testManualGameImageOutput2()

