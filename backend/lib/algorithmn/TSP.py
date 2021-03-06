from tsp_solver.greedy import solve_tsp

#Prepare the square symmetric distance matrix for 3 nodes:
#  Distance from A to B is 1.0
#                B to C is 3.0
#                A to C is 2.0
D = [[],
             [1.0],
                  [2.0, 3.0]]

path = solve_tsp( D )

#will print [1,0,2], path with total length of 3.0 units
print(path)
