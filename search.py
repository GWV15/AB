#!/usr/bin/python

# GWV 15/16 Abgabe - Zettel 3
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009 

# Imports
import sys
import numpy as np

# Constants
bound	= 'x'
goal	= 'g'
start	= 's'

# Functions


# Print the given field
# field - Field to print
def printField(field):
	for i in range(len(field)):
		print(''.join(field[i]))

# Search for character in field
# c		- Character to find
# field	- Search space
def searchFor(c,field):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)

# Returns true if pos in field is a boundary
# pos	- Position in field
# field - Search space
def isBound(pos,field):
	return field[pos[0]][pos[1]] == bound

# Returns true if pos in field is a Portal
def isPortal(pos,field):
	return field[pos[0]][pos[1]] in [chr(el+ord('0')) for el in range(10)]

# Returns the position of the other point of the input portal position
def searchPortalPoint(pos,field):
	portalnumber = field[pos[0]][pos[1]]
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == portalnumber:
				if not (i == pos[0] and j == pos[1]): 
					return (i,j)

# Draws the path in the field
# path	- the path to draw
# field - the field to draw on
def drawPath(path, field):
	tmp = [line for line in field]
	if path:
		start = path[0]
		goal = path[-1]
		for el in path:
			if el is not start and el is not goal:
				tmp[el[0]][el[1]] = '+'
	return tmp

# Performes a bfs
# field - Search space
def bfs(field):
	#find start and goal position
	start_pos = searchFor(start,field)
	goal_pos = searchFor(goal,field)
	#initialize frontier with only start node
	frontier = [[start_pos]]
	#repeat while frontier is not empty:
	while len(frontier)>0:
		for path in frontier:
			node = path[-1]
			w = (node[0] + 1, node[1]  + 0)
			a = (node[0] + 0, node[1]  - 1)
			s = (node[0] - 1, node[1]  + 0)
			d = (node[0] + 0, node[1]  + 1)
			neighbors = [w,a,s,d]
			#return path if goal is the end of path
			if node == goal_pos: return path
			#try to expand each path in all directions which havent been visited yet and are not boundaries
			for n in neighbors:
				if (field[n[0]][n[1]] != bound) and all(n not in path for path in frontier):
					path_found = [e for e in path]
					path_found.append(n)
					frontier.append(path_found)

			frontier.remove(path)
	return 0

# Performes a dfs
# field - Search space
def dfs(field):
	# Find goal
	goal_pos = searchFor(goal, field)

	# Create frontier with start in it
	frontier = [[searchFor(start, field)]]

	# Search as long as frontier != []
	while frontier:
		# Most recent path
		path = frontier[-1]

		# Last node of path
		head = path[-1]
		printField(drawPath(path,field))
		print(path)
		input("step")
		# Get the neighborhood
		north = (head[0] + 1, head[1])
		south = (head[0] - 1, head[1])
		west  = (head[0], head[1] - 1)
		east  = (head[0], head[1] + 1)

		# Iterate over the neighborhood
		for nextNode in [north,east,south,west]:
			# Test nextNode if it is a 'x' and whether it is already in the stack
			if not isPortal(nextNode,field) and not isBound(nextNode,field) and all(nextNode not in p for p in frontier):
				# Copy the path and add nextNode to it
				new_path = [node for node in path] 
				new_path.append(nextNode)

				# Are we finished?
				if new_path[-1] == goal_pos: return new_path 

				# Add the newfound path to the frontier
				frontier.append(new_path)
			elif isPortal(nextNode,field) and all(nextNode not in p for p in frontier):
				if searchPortalPoint(nextNode,field) and all(searchPortalPoint(nextNode,field) not in p for p in frontier):
					new_path = [node for node in path]
					new_path.append(searchPortalPoint(nextNode,field))

					if new_path[-1] == goal_pos: return new_path

					frontier.append(new_path)

		# Remove the old path
		frontier.remove(path)

def cost(path,goal_pos):
	return len(path) + abs((path[-1][0] - goal_pos[0])) + abs((path[-1][1] - goal_pos[1]))

def AStarSearch(field):

	#find start and goal position
	start_pos = searchFor(start,field)
	goal_pos = searchFor(goal,field)

	#initialize frontier with only start node
	frontier = [[start_pos]]

	#repeat while frontier is not empty:
	while frontier:
		#current_costs = 0
		#current_path = None
		#for path in frontier:
		#	if cost(path, goal_pos) < current_costs or current_costs == 0:
		#		current_costs = cost(path, goal_pos)
		#		current_path = path
		#	else:
		#		continue
		current_path = frontier[np.argmin([cost(path,goal_pos) for path in frontier])]

		# Take the old path out
		frontier.remove(current_path)

		# Last node of path
		head = current_path[-1]

		# Get the neighborhood
		north = (head[0] + 1, head[1])
		south = (head[0] - 1, head[1])
		west  = (head[0], head[1] - 1)
		east  = (head[0], head[1] + 1)

		# Iterate over the neighborhood
		for nextNode in [north,east,south,west]:
			# Test nextNode if it is a 'x' and whether it is already in the stack
			if not isPortal(nextNode,field) and not isBound(nextNode,field) and all(nextNode not in p for p in frontier):
				# Copy the path and add nextNode to it
				new_path = [node for node in current_path] 
				new_path.append(nextNode)

				# Are we finished?
				if new_path[-1] == goal_pos: return new_path 

				# Add the newfound path to the frontier
				frontier.append(new_path)
			elif isPortal(nextNode,field) and all(nextNode not in p for p in frontier):
				new_path = [node for node in current_path]
				new_path.append(searchPortalPoint(nextNode,field))

				if new_path[-1] == goal_pos: return new_path

				frontier.append(new_path)


# Main method
def main():
	# Load the field
	if len(sys.argv) == 2:
		field = [list(line.rstrip('\n')) for line in open(sys.argv[1])]
	else:
		print("There has to be exactly one command line argument. It should be our enviroment.")
		return

	# Print the field
	print("Enviroment")
	printField(field)

	# Some Info
	print("Character", start, "found at", searchFor(start,field))
	print("Character", goal , "found at", searchFor(goal,field), "\n")

	# Ask for algorithm
	howToSearch = input("Should I do the \"bfs\", \"dfs\" or \"astar\"?:")
	# Ask until valid answer is given
	while(howToSearch != "dfs" and howToSearch != "bfs" and howToSearch != "astar"):
		howToSearch = input("I didn't understand you. \"bfs\", \"dfs\" or \"astar\"?:")

	# Run the search
	if  (howToSearch == "dfs"  ): search_path = dfs(field)
	elif(howToSearch == "bfs"  ): search_path = bfs(field)
	elif(howToSearch == "astar"): search_path = AStarSearch(field)

	# Print the path
	print(howToSearch.upper(), "Path:\n", search_path, "\n")
	print("Visualized Path:\n")
	printField(drawPath(search_path,field)) # Draw the path to the field
	#printField(field) # Print the field

# Run the main method
if __name__ == "__main__":
    main()