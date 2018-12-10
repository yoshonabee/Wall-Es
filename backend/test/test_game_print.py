import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np

from lib.game.game import Game, Command
from lib.game.agent import Agent
from lib.game.maps import ConsoleMap


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

def no_target_walk(area, agent, height, width):
    direction = [0, 0, 0, 0, 0]
    for i in range(0, width):
        for j in range(0, height):
            if i >= 0 and i < agent.x:
                if j >= 0 and j < agent.y:
                    if area[i][j] == -3:
                        direction[2] += 1
                elif j > agent.y and j < width:
                    if area[i][j] == -3:
                        direction[3] += 1
            elif i > agent.x and i < height:
                if j >= 0 and j < agent.y:
                    if area[i][j] == -3:
                        direction[1] += 1
                elif j > agent.y and j < width:
                    if area[i][j] == -3:
                        direction[4] += 1
     
    ind = -1    
    maximum = 0
    for k in range(0, 5):
        if ind == -1:
            maximum = direction[0]
            ind = 0
        elif direction[k] > maximum:
            maximum = direction[k]
            ind = k
    if ind == 0:
        if agent.x <= np.int(width / 2) and agent.y <= np.int(height / 2):
            ind = 4
        elif agent.x <= np.int(width / 2) and agent.y > np.int(height / 2):
            ind = 1
        elif agent.x > np.int(width / 2) and agent.y <= np.int(height / 2):
            ind = 3
        elif agent.x > np.int(width / 2) and agent.y > np.int(height / 2):
            ind = 2
    return ind

def haveunseenspace(area, height, width):
    for i in range(0, width):
        for j in range(0, height):
            if area[i][j] == -3:
                return True
                break
    return False

def testManualGameImageOutput2():
    print("\n== init manual setting game ==")
    height = 40
    width = 40
    crash = 0
    
    mode ={0:False,1:False,2:False} #agents' mode True if agent has target rightnow
    found_target = []    
    now_target = {0:[],1:[],2:[]}    
    belongs = {0:[],1:[],2:[]}
    cmd = []
    
    game = Game(height, width)

    game.setRandomMap(0, 200, 0) # numbers of agents, targets, obstacles
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
    
    while(game.consolemap.targets != [] or haveunseenspace(game.consolemap.areas, height, width)):
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
            
            if mode[i] == False: # assign a target to agent 
                now_target[i] = []
                for target_list in belongs[i]:
                    if now_target[i] == [] and target_list != []:
                        now_target[i] = target_list
                        mode[i] = True
                    else:
                        if target_agent_len(target_list,agents[i]) < target_agent_len(now_target[i],agents[i]):
                            now_target[i] = target_list
            
            no_target_command = { 1: {"dx": 1, "dy": -1},
                                  2: {"dx": -1, "dy": -1},
                                  3: {"dx": -1, "dy": -1},
                                  4: {"dx": 1, "dy": -1},
                                 }
            
            if mode[i] == False: # assign the cammand to agent
                direction = no_target_walk(game.getmap(), agents[i], height, width)
                if direction > 0:
                    cmd.append(Command(agents[i].id, no_target_command[direction]["dx"],no_target_command[direction]["dy"]))
                    print("agent %d goes" % agents[i].id,no_target_command[direction]["dx"], " and ", no_target_command[direction]["dy"])
            elif mode[i] == True:
                cmd.append(walk(now_target[i],agents[i]))
                mode[i] = False
                
        game.runOneRound(cmd)
        
        for i in agents: #calculate crash time
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

