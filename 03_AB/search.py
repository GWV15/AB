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
def printField(field):

	# Draw the field
	print("Environment:\n")

	for i in range(len(field)):
		print(''.join(field[i]))

	print("\n")

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

		for nextNode in [north,east,south,west]:
			# Test nextNode if it is a 'x' and whether it is already in the stack
			if not isBound(nextNode,field) and all(nextNode not in p for p in frontier):
				# Copy the path and add nextNode to it
				new_path = [node for node in path] 
				new_path.append(nextNode)

				# Are we finished?
				if new_path[-1] == tuple_goal: return new_path 

				# Add the newfound to the frontier
				frontier.append(new_path)
		# Remove the old path
		frontier.remove(path)

# Draws the path in the field
# path	- the path to draw
# field - the field to draw on
def drawPath(path, field):
	start = path[0]
	goal = path[-1]
	for el in path:
		if el is not start and el is not goal:
			field[el[0]][el[1]] = '+'

# Main method
def main():
	# Loading the field
	if len(sys.argv) == 2:
		field = [list(line.rstrip('\n')) for line in open(sys.argv[1])]
	else:
		print("There has to be exactly one command line argument. It should be our enviroment.")
		return

	printField(field)

	# Some Info
	print("Character", start, "found at", searchFor(start,field))
	print("Character", goal, "found at", searchFor(goal,field))

	bfs_path = bfs(field)
	dfs_path = dfs(field)

	print("BFS Path:\n")
	print(bfs_path)
	print("\n")

	print("DFS Path:\n")
	print(dfs_path)
	print("\n")


	whattodraw = ""
	while(whattodraw != "dfs" and whattodraw != "bfs"):
		whattodraw = input("Should I draw the \"bfs\" or \"dfs\"?:")

	if(whattodraw == "dfs"):
		print("Visualized Path:\n")
		drawPath(dfs_path,field)
		printField(field)
	else:
		print("Visualized Path:\n")
		drawPath(bfs_path,field)
		printField(field)


# Main
if __name__ == "__main__":
    main()