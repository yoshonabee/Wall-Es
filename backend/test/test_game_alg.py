import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np

from lib.game.game import Game, Command
from lib.game.agent import Agent


def testManualGameImageOutput2():
    print("\n== init manual setting game ==")
    height = 50
    width = 50
    crash = 0
    
    game = Game(height, width)

    game.setRandomMap(8, 300, 200) # numbers of agents, targets, obstacles


    game.printGodMap()
    #agents = game.godmap.agents
    '''agents = {
        0: Agent(0, 0, 0, height, width, r=5), # id, x, y, height, width
        1: Agent(1, width-1 , 0, height, width, r=5), # id, x, y, height, width
        2: Agent(2, 0 , height-1 , height, width, r=5), # id, x, y, height, width
        #3: Agent(3, width - 1, height- 1, height, width, r = 5)
    }'''
    
    #game.setAgents(agents)
    ##########
    game.runOneRoundwithoutMovement()
    game.printConsoleMap()   
    round = 1
    while(game.algNext(crash, round)):
        round += 1
        
testManualGameImageOutput2()

