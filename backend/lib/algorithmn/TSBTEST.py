import math

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
def euclid_distance(x1, y1, x2, y2):
	# Euclidean distance between points.
	dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	return dist
def create_distance_matrix(locations):
# Create the distance matrix.
	size = len(locations)
	dist_matrix = {}

	for from_node in range(size):
		dist_matrix[from_node] = {}
		for to_node in range(size):
			x1 = locations[from_node]['x']
			y1 = locations[from_node]['y']
			x2 = locations[to_node]['x']
			y2 = locations[to_node]['y']
			dist_matrix[from_node][to_node] = euclid_distance(x1, y1, x2, y2)
	return dist_matrix
def create_distance_callback(dist_matrix):
	# Create the distance callback.

	def distance_callback(from_node, to_node):
		return int(dist_matrix[from_node][to_node])

	return distance_callback

def findpath(targets):
	# Create the data.
	locations = targets
	dist_matrix = create_distance_matrix(locations)
	dist_callback = create_distance_callback(dist_matrix)
	tsp_size = len(locations)
	num_routes = 1
	depot = 0

	# Create routing model.
	if tsp_size > 0:
		routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
		search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
		routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
		# Solve the problem.
		assignment = routing.SolveWithParameters(search_parameters)
		if assignment:

			# Solution cost.
			print ("Total distance: " + str(assignment.ObjectiveValue()) + "\n")

			# Inspect solution.
			# Only one route here; otherwise iterate from 0 to routing.vehicles() - 1.
			route_number = 0
			node = routing.Start(route_number)
			start_node = node
			route = ''
			count = 0
			out = 0
			while not routing.IsEnd(node):
				count += 1
				if count == 2 :
					out = node
				route += str(node) + ' -> '
				node = assignment.Value(routing.NextVar(node))
			route += '0'

			#print ("Route:\n\n" + str(out))
		else:
			print ('No solution found.')
	else:
		print ('Specify an instance greater than 0.')

	return out
def create_data_array():
	locations = [{'x':12,'y':20},{'x':0,'y':0},{'x':30,'y':20},{'x':12,'y':50}]

	return locations

'''if __name__ == '__main__':
	main()'''	