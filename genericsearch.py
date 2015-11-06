#!/usr/bin/python

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009 

# Imports
import sys
import numpy as np ## INSTALL
from copy import deepcopy
from queue import LifoQueue, Queue, PriorityQueue
from timeit import default_timer as timer

# Constants
bound	= 'x'
goal	= 'g'
start	= 's'
searches = ["bfs","dfs","astar"]

# Class
def MyPriorityQueue(PriorityQueue):
	def get(self):
		return super().get()[-1]


# Functions

# Print the given field
# field - field to print
def printField(field):
	for i in range(len(field)):
		print(''.join(field[i]))

# Search for character in field
# c		- character to find
# field	- search space
def searchFor(c,field):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)

# Returns true if pos in field is a boundary
# pos	- position in field
# field - search space
def isBound(pos,field):
	return field[pos[0]][pos[1]] == bound

# Returns true if pos in field is a Portal
def isPortal(pos,field):
	return field[pos[0]][pos[1]] in [chr(el+ord('0')) for el in range(10)]

# Returns the position of the other point of the input portal position
# pos	- position in field
# field - search space
def searchPortalPoint(pos,field):
	portalnumber = field[pos[0]][pos[1]]
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == portalnumber:
				if not (i == pos[0] and j == pos[1]): 
					return (i,j)

# Returns a list of positions of all portal nodes
# field - search space
def getPortalList(field):
	portallist = []
	for i in range(len(field)):
		for j in range(len(field[i])):
			if isPortal((i,j),field):
				portallist.append((i,j))
	return portallist

# Draws the path in the field
# path	- the path to draw
# field - the field to draw on
def drawPath(path, field):
	tmp = deepcopy(field)
	if path:
		start = path[0]
		goal = path[-1]
		for el in path:
			if el is not start and el is not goal:
				tmp[el[0]][el[1]] = '+'
	return tmp

# This function enables the user to step through iterations and see the current path
# path	- the path to show
# field - search space
def debug(path, field):
	printField(drawPath(path,field))
	print(path)
	input("step")

# Calculate the estimate cost of a given path to the goal position
# When working with portals an optimistic heuristic assumes that the shortest path the minimum of the normal Manhattan distance
# and a shortcut with portals, where the maximum shortcut is given by the 
# Manhattan distance to the nearest portal from the current path + Manhattan distance from the goal to the nearest portal to the goal
# regargless of any more portals taken on the path
# path		- the path
# gool_pos	- the goal position
# field 	- search space
def heuristicCost(path,goal_pos,field):
	PortalList = getPortalList(field)
	if len(PortalList) > 1:
		nearestPortalHead = PortalList[np.argmin([getManhattanDistance(node,path[-1]) for node in PortalList])]
		nearestPortalGoal = PortalList[np.argmin([getManhattanDistance(node,goal_pos) for node in PortalList])]
		return len(path) + min(getManhattanDistance(path[-1],goal_pos),(getManhattanDistance(path[-1],nearestPortalHead)+getManhattanDistance(nearestPortalGoal,goal_pos)))
	return len(path) + getManhattanDistance(path[-1],goal_pos)

# Returns the 4 orthogonal neighbors in 2D Space of a Node
# If the neighbor is a portal the counterpart portalnode gets added instead
# node 	- position in the field
# field - search space
def getNeighbors(node,field):
	w = (node[0] + 1, node[1]  + 0)
	a = (node[0] + 0, node[1]  - 1)
	s = (node[0] - 1, node[1]  + 0)
	d = (node[0] + 0, node[1]  + 1)
	neighborlist = [w,a,s,d]
	for n in neighborlist:
		if isPortal(n,field):
			neighborlist[neighborlist.index(n)] = searchPortalPoint(n,field)
	return neighborlist

# Calculate the Manhattan distance between two points
# pointA	- first point
# pointB	- second point
def getManhattanDistance(pointA, pointB):
	return abs((pointA[0] - pointB[0])) + abs((pointA[1] - pointB[1]))

# Generic Search from a List of Starting Points to a List of Endpoints
# BFS,DFS or A* depends on the given dataStructure
# field 			- search space
# startPosList		- list of possible start positions
# endPosList		- list of possible end positions
# _dataStructure	- data structure for the frontier (decides which search alg. to use)
# _heuristic		- flag: use heuristics
# _debug			- flag: use debugging method
def genericSearch(field, startPosList, endPosList, _dataStructure=Queue, _heuristic=False, _debug=False):
	# Init
	visited = []
	frontier = _dataStructure()
	max_frontier_len = 0

	# Put all start positions in the frontier
	for startPos in startPosList:
		if _heuristic:
			frontier.put((0,[startPos]))
		else:
			frontier.put([startPos])

	# Search as long as the frontier has some entries left
	while not frontier.empty():
		# Remember the biggest frontier
		if frontier.qsize() > max_frontier_len: max_frontier_len = frontier.qsize()

		# Get the next path 
		path = []
		if _heuristic:
			path = frontier.get()[-1]
		else:
			path = frontier.get()

		# Get the node we want to expand
		head = path[-1]

		# Don't visit a node twice
		if head not in visited:
			
			# Remember we were here
			visited.append(head)
			
			# Are we finished?
			if head in endPosList: return path,len(visited),max_frontier_len

			# Iterate over all neighbors
			for neighbor in getNeighbors(head,field):

				# Can we expand in this direction?
				if not isBound(neighbor, field):

					# constuct the new path
					new_path = [n for n in path]
					new_path.append(neighbor)

					# Display the current situation if debug flag is set
					if _debug: debug(field,new_path)

					# Use heuristics if flag is set
					if _heuristic:
						frontier.put((heuristicCost(new_path,endPosList[0],field),new_path))
					else:
						frontier.put(new_path)

	# When the frontier is empty no path was found. Return 0 as path.
	return 0,len(visited),max_frontier_len

# Print statistics collected each search
# time			- time elapsed while searching
# max_frontier	- Max number of elements in frontier while searching
# visit_count	- Number of elements visited
def printSearchInfo(time,max_frontier,visit_count):
	print("Time: ", time)
	print("Biggest frontier had ", max_frontier, " Elements")
	print("The search \"visited\" ", visit_count, " Points")

# Ask a given question, until the given answer matches the allowed ones
# cli_arg				- number of cli-argument, which answers the question. Set to 0 to disable
# first_question		- the first question to ask (only without cli_arg)
# following_question	- if the cli-arg or input of first_question is not in answers, ask this question
# answers				- list of possible answers
def askForAnswer(cli_arg, first_question, following_question, answers=["y","n"]):
	if cli_arg > 1 and len(sys.argv) > cli_arg: answer = sys.argv[cli_arg]
	else: answer = input(firstQuestion + " (" + "|".join(answers) + ") ")
	# Ask until valid answer is given
	while(answer not in answers):
		answer = input(followingQuestion + " (" + "|".join(answers) + ") ")
	return answer

# Main method
def main():
	# Load the field
	if len(sys.argv) >= 2: field = [list(line.rstrip('\n')) for line in open(sys.argv[1])]
	else:
		print("There has to be at least one command line argument. It should be our enviroment.")
		return
	print(sys.argv[1])

	# Print the field
	print("Enviroment")
	printField(field)

	# Some Info
	print("Character", start, "found at", searchFor(start,field))
	print("Character", goal , "found at", searchFor(goal,field), "\n")

	# Ask for debug output
	if "y" == askForAnswer(3, "Do you want to debug and step through the pathfinding?", "I didn't understand you.", ["y","n"]):
		debugFlag = True
	else: debugFlag = False

	howToSearch = askForAnswer(2, "Which search should I use?", "I didn't understand you.", searches)

	# Run the search
	tstart = timer()
	if  (howToSearch == "dfs"  ): search_result = genericSearch(field,[searchFor(start,field)],[searchFor(goal,field)],_dataStructure=LifoQueue,_heuristic=False,_debug=debugFlag)
	elif  (howToSearch == "bfs"  ): search_result = genericSearch(field,[searchFor(start,field)],[searchFor(goal,field)],_dataStructure=Queue,_heuristic=False,_debug=debugFlag)
	elif  (howToSearch == "astar"  ): search_result = genericSearch(field,[searchFor(start,field)],[searchFor(goal,field)],_dataStructure=PriorityQueue,_heuristic=True,_debug=debugFlag)
	tend = timer()
	elapsed_time = tend - tstart
	search_path = search_result[0]

	# Print the path
	print("\nSearch has finished")
	if(search_path == 0):
		print("No Path found")
	else:
		print(howToSearch.upper(), "Path:\n", search_path, "\n")
		print("Visualized Path:\n")
		printField(drawPath(search_path,field)) # Draw the path to the field
		#printSearchInfo()
	if "y" == askForAnswer(4, "Some statistics?", "I didn't understand you.", ["y","n"]):
		printSearchInfo(elapsed_time, search_result[2] ,search_result[1])


# Run the main method
#
# CLI usage:
# If all arguments are given the search does not rely on any further user interaction
# If a given cli-arg does not match the answers, the programm asks interactively
#1 (PATH)		text file containing the field
#2 (searches[])	search algorithm
#3 (y or n)		Step throu the search
#4 (y or n)		Display additional info
#
if __name__ == "__main__":
    main()

