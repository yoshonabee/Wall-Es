import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np

from lib.game.game import Game, Command
from lib.game.agent import Agent


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
    game.setScore(100, 10, -0.01, -100)

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

def target_agent_len(target,agent):
    return np.sqrt(np.square(target['x'] - agent.x) + np.square(target['y'] - agent.y))


def walk(target,agent):
    x = 0
    y = 0
    if (target['x'] - agent.x) > 0:
        x = 1
    elif (target['x'] - agent.x) == 0:
        x = 0
    else:
        x = -1
    if (target['y'] - agent.y) > 0:
        y = 1
    elif (target['y'] - agent.y) == 0:
        y = 0
    else:
        y = -1
    print("agent %d goes" % agent.id,x,"and",y)
    return Command(agent.id,x,y)


def testManualGameImageOutput2():
    print("\n== init manual setting game ==")
    height = 20
    width = 20
    crash = 0
    
    mode ={0:False,1:False,2:False} #agents' mode True if agent has target rightnow
    found_target = []    
    now_target = {0:[],1:[],2:[]}    
    belongs = {0:[],1:[],2:[]}
    cmd = []
    
    game = Game(height, width)

    game.setRandomMap(0, 50, 0) # numbers of agents, targets, obstacles
    game.setScore(100, 10, -0.01, -100)


    game.printGodMap()

    agents = {
        0: Agent(0, 0, 0, height, width, r=5), # id, x, y, height, width
        1: Agent(1, width-1 , 0, height, width, r=5), # id, x, y, height, width
        2: Agent(2, int(width/2) , height-1 , height, width, r=5), # id, x, y, height, width
    }
    
    game.setAgents(agents)
    ##########
    game.runOneRound([Command(0, 0, 0), Command(1, 0, 0), Command(2, 0, 0)])
    game.printConsoleMap()   
    round = 1
    
    while(game.consolemap.targets != []):
        print("====the %d round" % round)
        
        found_target = game.consolemap.targets
        #print("found:",found_target)        
        #print("agent mode",mode)           
        
        for item in found_target: # cluster the target
            index = 0
            if target_agent_len(item,agents[index])>target_agent_len(item,agents[1]):
                index = 1
            if target_agent_len(item,agents[index])>target_agent_len(item,agents[2]):
                index = 2
            belongs[index].append(item)
        
        cmd = [] # store the new command for agents 

        for i in agents:
            if mode[i] == False:
                now_target[i] = []
                for target_list in belongs[i]:
                    if now_target[i] == [] and target_list != []:
                        now_target[i] = target_list
                        mode[i] = True
                    else:
                        if target_agent_len(target_list,agents[i]) < target_agent_len(now_target[i],agents[i]):
                            now_target[i] = target_list
            
            if mode[i] == False:
                if agents[i].x <= np.int(width / 2) and agents[i].y <= np.int(height / 2):
                    cmd.append(Command(agents[i].id, np.random.randint(0, 2), np.random.randint(0, 2)))
                elif agents[i].x <= np.int(width / 2) and agents[i].y > np.int(height / 2):
                    cmd.append(Command(agents[i].id, np.random.randint(0, 2), np.random.randint(-1, 1)))
                elif agents[i].x > np.int(width / 2) and agents[i].y <= np.int(height / 2):
                    cmd.append(Command(agents[i].id, np.random.randint(-1, 1), np.random.randint(0, 2)))
                elif agents[i].x > np.int(width / 2) and agents[i].y > np.int(height / 2):
                    cmd.append(Command(agents[i].id, np.random.randint(-1, 1), np.random.randint(-1, 1)))
            elif mode[i] == True:
                cmd.append(walk(now_target[i],agents[i]))
                mode[i] = False
                
        game.runOneRound(cmd)
        
        for i in agents:
            for j in range(i + 1, len(agents)):
                if agents[i].x == agents[j].x and agents[i].y == agents[j].y:
                    crash += 1
        print(found_target)
        
        game.printConsoleMap()
        belongs = {0:[],1:[],2:[]}
        round += 1
    print("crush time: %d" %crash)
    print("finish")
        
testManualGameImageOutput2()

