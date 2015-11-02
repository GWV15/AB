#!/usr/bin/python

# GWV 15/16 Abgabe - Zettel 3
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009 

# Imports
import sys

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

# Draws the path in the field
# path	- the path to draw
# field - the field to draw on
def drawPath(path, field):
	start = path[0]
	goal = path[-1]
	for el in path:
		if el is not start and el is not goal:
			field[el[0]][el[1]] = '+'

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
	tuple_goal = searchFor(goal, field)

	# Create frontier with start in it
	frontier = [[searchFor(start, field)]]

	# Search as long as frontier != []
	while frontier:

		# Most recent path
		path = frontier[-1]

		# Last node of path
		head = path[-1]

		# Get the neighborhood
		north = (head[0] + 1, head[1])
		south = (head[0] - 1, head[1])
		west  = (head[0], head[1] - 1)
		east  = (head[0], head[1] + 1)

		# Iterate over the neighborhood
		for nextNode in [north,east,south,west]:
			# Test nextNode if it is a 'x' and whether it is already in the stack
			if not isBound(nextNode,field) and all(nextNode not in p for p in frontier):
				# Copy the path and add nextNode to it
				new_path = [node for node in path] 
				new_path.append(nextNode)

				# Are we finished?
				if new_path[-1] == tuple_goal: return new_path 

				# Add the newfound path to the frontier
				frontier.append(new_path)

		# Remove the old path
		frontier.remove(path)

def AStarSearch(field):
	#find start and goal position
	start_pos = searchFor(start,field)
	goal_pos = searchFor(goal,field)

	#initialize frontier with only start node
	frontier = [[start_pos]]

	#repeat while frontier is not empty:
	while frontier:
		for path in frontier:
			if cost(path) < currentCosts or currentCosts == 0:
				currentCosts = cost(path)
				currentPath = path
			else:
				continue

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
			if not isBound(nextNode,field) and all(nextNode not in p for p in frontier):
				# Copy the path and add nextNode to it
				new_path = [node for node in current_path] 
				new_path.append(nextNode)

				# Are we finished?
				if new_path[-1] == tuple_goal: return new_path 

				# Add the newfound path to the frontier
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
	howToSearch = input("Should I do the \"bfs\" or \"dfs\"?:")
	# Ask until valid answer is given
	while(howToSearch != "dfs" and howToSearch != "bfs"):
		howToSearch = input("I didn't understand you. \"bfs\" or \"dfs\"?:")

	# Run the search
	if  (howToSearch == "dfs"): search_path = dfs(field)
	elif(howToSearch == "bfs"): search_path = bfs(field)

	# Print the path
	print(howToSearch.upper(), "Path:\n", search_path, "\n")
	print("Visualized Path:\n")
	drawPath(search_path,field) # Draw the path to the field
	printField(field) # Print the field

# Run the main method
if __name__ == "__main__":
    main()