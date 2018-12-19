import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np

from lib.game.game import Game, Command
from lib.game.agent import Agent


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

def no_target_walk(area, agent):
    direction = [0, 0, 0, 0, 0]
    target = [0, 0, 0, 0, 0]
    height = agent.height
    width = agent.width
    for i in range(0, height): # detect target and unseenspace in four direction for agent 
        for j in range(0, width):
            if i >= 0 and i <= agent.y:
                if j >= 0 and j <= agent.x:
                    if area[i][j] == -3:
                        direction[2] += 1
                    if area[i][j] == -2:
                        target[2] += 1
                if j >= agent.x:
                    if area[i][j] == -3:
                        direction[1] += 1
                    if area[i][j] == -2:
                        target[1] += 1
            if i >= agent.y:
                if j >= 0 and j <= agent.x:
                    if area[i][j] == -3:
                        direction[3] += 1
                    if area[i][j] == -2:
                        target[3] += 1
                if j >= agent.x:
                    if area[i][j] == -3:
                        direction[4] += 1
                    if area[i][j] == -2:
                        target[4] += 1
    ind = -1    
    maximum = 0
    if np.sum(direction) != 0:
        if direction[1] == direction[2] and direction[1] * direction[2] != 0:
            ind = 6
        elif direction[2] == direction[3] and direction[2] * direction[3] != 0:
            ind = 7
        elif direction[3] == direction[4] and direction[3] * direction[4] != 0:
            ind = 8
        elif direction[4] == direction[1] and direction[4] * direction[1] != 0:
            ind = 5
        else:    
            for k in range(0, len(direction)):
                if ind == -1:
                    maximum = direction[0]
                    ind = 0
                elif direction[k] > maximum:
                    maximum = direction[k]
                    ind = k
            
        
    else:
        maximum = 0
        ind == -1
        if target[1] == target[2] and target[1] * target[2] != 0:
            ind = 6
        elif target[2] == target[3] and target[2] * target[3] != 0:
            ind = 7
        elif target[3] == target[4] and target[3] * target[4] != 0:
            ind = 8
        elif target[4] == target[1] and target[4] * target[1] != 0:
            ind = 5
        else:  
            for k in range(0, len(target)):
                if ind == -1:
                    maximum = target[0]
                    ind = 0
                elif target[k] > maximum:
                    maximum = target[k]
                    ind = k
    return ind

def haveunseenspace(area, height, width):
    for i in range(0, width):
        for j in range(0, height):
            if area[i][j] == -3:
                return True
                break
    return False

def in_mission_field(agents, belongs, game): # cluster the target to the agent in the radius of their vision 
    mf = {0: [], 1: [], 2: []}
    for i in agents:
        for target in belongs[i]:
            if target_agent_len(target, agents[i]) < agents[i].radius * 1.5:
                mf[i].append(target)

    null = 0
    for i in agents:
        if belongs[i] == None:
            null += 1
    if null == 3:
        return False
    else:
        if mf == belongs and not haveunseenspace(game.consolemap.areas, agents[0].height, agents[0].width):
            return True

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


    game.printGodMap()

    agents = {
        0: Agent(0, 0, 0, height, width, r=5), # id, x, y, height, width
        1: Agent(1, width-1 , 0, height, width, r=5), # id, x, y, height, width
        2: Agent(2, int(width/2) , height-1 , height, width, r=5), # id, x, y, height, width
    }
    
    game.setAgents(agents)
    ##########
    game.runOneRoundwithoutMovement()
    game.printConsoleMap()   
    round = 1
    
    while(game.consolemap.targets != [] or haveunseenspace(game.consolemap.areas, height, width)):
    #for round in range(1, 180):
        print("====the %d round" % round)
        
        found_target = game.consolemap.targets
        
        for item in found_target: # cluster the target
            index = 0
            if target_agent_len(item,agents[index])>target_agent_len(item,agents[1]):
                index = 1
            if target_agent_len(item,agents[index])>target_agent_len(item,agents[2]):
                index = 2
            belongs[index].append(item)
        
        #belongs = target_belong(found_target, agents)
        
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
            
            no_target_command = { 0: {"dx": 0, "dy": 0}, # no move
                                  1: {"dx": 1, "dy": -1}, # move up-right
                                  2: {"dx": -1, "dy": -1}, # move up-left
                                  3: {"dx": -1, "dy": 1}, # move down-left
                                  4: {"dx": 1, "dy": 1}, # move down-rigth
                                  5: {"dx": 1, "dy": 0}, # move right
                                  6: {"dx": 0, "dy": -1}, # move up
                                  7: {"dx": -1, "dy": 0}, # move left
                                  8: {"dx": 0, "dy": 1}, # move down
                                 }
            
            if mode[i] == False: # assign the cammand to agent
                if in_mission_field(agents, belongs, game):
                    cmd.append(Command(agents[i].id, 0, 0))
                    print("agent %d goes 0 and 0" % agents[i].id)
                else:
                    direction = no_target_walk(game.getmap(), agents[i])
                    cmd.append(Command(agents[i].id, no_target_command[direction]["dx"],no_target_command[direction]["dy"]))
                    print("agent %d goes" % agents[i].id,no_target_command[direction]["dx"], "and", no_target_command[direction]["dy"])
            
            elif mode[i] == True:
                cmd.append(walk(now_target[i],agents[i]))
                mode[i] = False
        
        game.runOneRound(cmd)
        game.printConsoleMap()
        for i in agents: #calculate crash time
            for j in range(i + 1, len(agents)):
                if agents[i].x == agents[j].x and agents[i].y == agents[j].y:
                    crash += 1
        #print(found_target)
        
        belongs = {0:[],1:[],2:[]}
        round += 1
    #print(np.sum(game.consolemap.areas))    
    print("crush time: %d" %crash)
    print("finish")
        
testManualGameImageOutput2()

