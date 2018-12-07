import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

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
    return (target['x']-agent.x)*(target['x']-agent.x)+(target['y']-agent.y)*(target['y']-agent.y)
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
    print("agent %d  goes" % agent.id,x,"and",y)
    return Command(agent.id,x,y)
def testManualGameImageOutput2():
    print("\n== init manual setting game ==")
    height = 20
    width = 20
    
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
    game.printConsoleMap()    
    ##########
    game.runOneRound([Command(0, 0, 0), Command(1, 0, 0), Command(2, 0, 0)])

    for round in range(10):
        print("====the %d round" % round)
        
        
        found_target = game.consolemap.targets
        
        
        for i in range(3):
            if mode[i] is True:
                if now_target[i] in found_target:
                    found_target.remove(now_target[i])
        
                else:
                    now_target[i]=[]
                    mode[i] = False
           
             
        for item in found_target:
            index = 0
            if target_agent_len(item,agents[index])>target_agent_len(item,agents[1]):
                index = 1
            if target_agent_len(item,agents[index])>target_agent_len(item,agents[2]):
                index = 2
            belongs[index].append(item)
        cmd = []
        for i in range(3):
            
            if mode[i] == False:
                target_find = belongs[i][0]
                for target_list in belongs[i]:
                    if target_agent_len(target_list,agents[i]) < target_agent_len(target_find,agents[i]):
                        target_find = target_list
               
                now_target[i] = target_find
                mode[i] = True
            print(now_target[i])
            cmd.append(walk(now_target[i],agents[i]))
            print()
            
        game.runOneRound(cmd)
        print("agent%d position:(%d,%d)" %(agents[0].id,agents[0].x,agents[0].y))
        print("agent%d position:(%d,%d)" %(agents[1].id,agents[1].x,agents[1].y))
        print("agent%d position:(%d,%d)" %(agents[2].id,agents[2].x,agents[2].y))
        game.printConsoleMap()
        belongs = {0:[],1:[],2:[]}
    '''for i in range(0, 10):
        
        print("\n== %dst round ==" % i)
        
        game.runOneRound([Command(0, 1, 1), Command(1, 1, 0), Command(2, -1, -1)])
        game.printConsoleMap()'''


testManualGameImageOutput2()

