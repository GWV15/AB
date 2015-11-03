#!/usr/bin/python

# GWV 15/16 Abgabe - Zettel 3
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009 

# Imports
import sys
from timeit import default_timer as timer
import queue

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
			field[el[0]][el[1]] = 'o'

def heuristic(pos,goal_pos):
	return abs((pos[0] - goal_pos[0])) + abs((pos[1] - goal_pos[1]))

def A_star_search(field, start, goal):

	frontier = queue.PriorityQueue()
	frontier.put([start], 0)
	visited = [start]

	#repeat while frontier is not empty:
	while not frontier.empty():

		current_path = frontier.get()

		# Last node of path
		head = current_path[-1]
		# Get the neighborhood
		north = (head[0] + 1, head[1])
		south = (head[0] - 1, head[1])
		west  = (head[0], head[1] - 1)
		east  = (head[0], head[1] + 1)

		# Iterate over the neighborhood
		for next_node in [north,east,south,west]:
			# Don't go back
			if next_node in visited or isBound(next_node, field): continue
			else:
				visited.append(next_node)
				# Create new path
				new_path = [node for node in current_path]
				new_path.append(next_node)
				# Calculate the estimated cost
				estimate = len(new_path) + heuristic(next_node,goal)
				# Insert the new Path into the Queue
				frontier.put(new_path, estimate)

				if next_node == goal: return new_path
	return "No path found"

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

	tstart = timer()
	search_path = A_star_search(field, searchFor(start,field), searchFor(goal,field))
	tend = timer()
	elapsed_time = tend - tstart

	# Print the path
	print("Elapsed time: ", elapsed_time)
	print("A* Path:\n", search_path, "\n")
	print("Visualized Path:\n")
	drawPath(search_path,field) # Draw the path to the field
	printField(field) # Print the field

# Run the main method
if __name__ == "__main__":
    main()