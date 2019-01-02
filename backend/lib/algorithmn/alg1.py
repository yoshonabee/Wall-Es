import numpy as np
import lib.algorithmn.TSBTEST as TB
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
class Command():
	def __init__(self, id, dx, dy):
		self.id = id
		self.dx = dx
		self.dy = dy

def target_agent_len(target,agent):
	return np.sqrt(np.square(target['x'] - agent.x) + np.square(target['y'] - agent.y))

def walk(target,agent, area):
	print('a')
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
	
	(x, y) = avoid_obstacles(agent, area, x, y)
	print("agent %d goes" % agent.id,x,"and",y)
	return Command(agent.id,x,y)

def no_target_walk(area, agent):
	print('b')
	direction = [-100, 0, 0, 0, 0]
	target = [-100, 0, 0, 0, 0]
	height = agent.height
	width = agent.width
	command = { 0: {"dx": 0, "dy": 0}, # no move
				1: {"dx": 1, "dy": -1}, # move up-right
				2: {"dx": -1, "dy": -1}, # move up-left
				3: {"dx": -1, "dy": 1}, # move down-left
				4: {"dx": 1, "dy": 1}, # move down-rigth
				5: {"dx": 1, "dy": 0}, # move right
				6: {"dx": 0, "dy": -1}, # move up
				7: {"dx": -1, "dy": 0}, # move left
				8: {"dx": 0, "dy": 1}, # move down
			   }
	
	for i in range(0, height): # detect target and unseenspace in four direction for agent 
		for j in range(0, width):
			if i >= 0 and i <= agent.y:
				if j >= 0 and j <= agent.x:
					if area[i][j] == -3:
						direction[2] += 1
					if area[i][j] == -2:
						target[2] += 1
                    if area[i][j] > 0:
                        direction[2] -= 20
                        target[2] -= 20
				if j >= agent.x:
					if area[i][j] == -3:
						direction[1] += 1
					if area[i][j] == -2:
						target[1] += 1
                    if area[i][j] > 0:
                        direction[1] -= 20
                        target[1] -= 20
			if i >= agent.y:
				if j >= 0 and j <= agent.x:
					if area[i][j] == -3:
						direction[3] += 1
					if area[i][j] == -2:
						target[3] += 1
                    if area[i][j] > 0:
                        direction[3] -= 20
                        target[3] -= 20
				if j >= agent.x:
					if area[i][j] == -3:
						direction[4] += 1
					if area[i][j] == -2:
						target[4] += 1
                    if area[i][j] > 0:
                        direction[4] -= 20
                        target[4] -= 20
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
	x = command[ind]["dx"]
	y = command[ind]["dy"]
	(x, y) = avoid_obstacles(agent, area, x, y)

	print("agent %d goes" % agent.id, x, "and", y)
	return Command(agent.id, x, y)

def avoid_obstacles(agent, area, x, y): #有出界的bug
	command = { 0: {"dx": 0, "dy": 0}, # no move
				1: {"dx": 1, "dy": 0}, # move up-right
				2: {"dx": 1, "dy": -1}, # move up-left
				3: {"dx": 0, "dy": -1}, # move down-left
				4: {"dx": -1, "dy": -1}, # move down-rigth
				5: {"dx": -1, "dy": 0}, # move right
				6: {"dx": -1, "dy": 1}, # move up
				7: {"dx": 0, "dy": 1}, # move left
				8: {"dx": 1, "dy": 1}, # move down
			   }
	
	for i in command:
		if x == command[i]["dx"] and y == command[i]["dy"]:
			ind = i
	
	try_x = agent.x + x
	try_y  = agent.y + y
	indlist = []
	if (try_x >= 0 and try_x < agent.width) and (try_y >= 0 and try_y < agent.height):
		if area[try_y][try_x] == -1 or area[try_y][try_x] > 0:
			print('c')
			for i in range(1, 5):
				n_ind = ind - i
				if n_ind <= 0:
					fix_ind = np.abs((n_ind - 1) % 9)
					try_x = agent.x + command[fix_ind]["dx"]
					try_y = agent.y + command[fix_ind]["dy"]
				else:
					try_x = agent.x + command[n_ind]["dx"]
					try_y = agent.y + command[n_ind]["dy"] 
				if (try_x >= 0 and try_x < agent.width) and (try_y >= 0 and try_y < agent.height):
					if not (area[try_y][try_x] == -1 or area[try_y][try_x] > 0):
						indlist.append(n_ind)    
			for i in range(1, 5):
				n_ind = ind + i
				if n_ind > 8:
					fix_ind = np.abs(n_ind % 8)
					try_x = agent.x + command[fix_ind]["dx"]
					try_y = agent.y + command[fix_ind]["dy"]
				else:
					try_x = agent.x + command[n_ind]["dx"]
					try_y = agent.y + command[n_ind]["dy"] 
				if (try_x >= 0 and try_x < agent.width) and (try_y >= 0 and try_y < agent.height):
					if not (area[try_y][try_x] == -1 or area[try_y][try_x] > 0):
						indlist.append(n_ind)    
			print(indlist)
			if len(indlist) == 0:
				ind = 0
			else:
				min = 8
				for i in range(0, len(indlist)):
					if np.abs(ind - indlist[i]) < min:
						min = np.abs(ind - indlist[i])
						n_ind = indlist[i]
				if n_ind <= 0:
					ind = np.abs((n_ind - 1) % 9)
				elif n_ind > 8:
					ind = np.abs(n_ind % 8)
				else:
					ind = n_ind
	print(ind)
	return (command[ind]["dx"], command[ind]["dy"])


def haveunseenspace(area, height, width):
	for i in range(0, len(area)):
		for j in range(0, len(area[0])):
			if area[i][j] == -3:
				return True
				break
	return False

def in_mission_field(agents, belongs, game): # pick up the target that is in their belonging
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

def alg_next(round, game, agents, crash): # one round
	
	found_target = []
	mode = {}
	now_target = {}
	belongs = {}
	for id in agents:
		mode[id] = False # agents' mode True if agent has target rightnow 
		now_target[id] = []  
		belongs[id] = []
	#print(round)
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
			if len(belongs[i]) != 0:           
				out = TB.findpath(belongs[i])
				now_target[i] = belongs[i][out]
				mode[i] = True
			'''for target_list in belongs[i]:
				if now_target[i] == [] and target_list != []:
					now_target[i] = target_list
					mode[i] = True
				else:
					if target_agent_len(target_list,agents[i]) < target_agent_len(now_target[i],agents[i]):
						now_target[i] = target_list'''
		
		
		if mode[i] == False: # assign the cammand to agent
			if in_mission_field(agents, belongs, game):
				print('d')
				cmd.append(Command(agents[i].id, 0, 0))
				print("agent %d goes 0 and 0" % agents[i].id)
			else:
				cmd.append(no_target_walk(game.getmap(), agents[i]))
				
	
		elif mode[i] == True:
			cmd.append(walk(now_target[i],agents[i], game.getmap()))
			mode[i] = False
		
	game.runOneRound(cmd)
	game.printConsoleMap()
	
    #calculate crash time
    for i in agents:
		for j in range(i + 1, len(agents)):
			if agents[i].x == agents[j].x and agents[i].y == agents[j].y:
				crash += 1
	round == 1
	return crash
