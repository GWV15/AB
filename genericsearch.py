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
bound_char	 = 'x'
goal_char	 = 'g'
start_char	 = 's'
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
def searchFor(field,c):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)


# Returns true if pos in field is a boundary
# field - search space
# pos	- position in field
def isBound(field,pos):
	return field[pos[0]][pos[1]] == bound_char


# Returns true if pos in field is a Portal
def isPortal(field,pos):
	return field[pos[0]][pos[1]] in [chr(el+ord('0')) for el in range(10)]


# Returns the position of the other point of the input portal position
# field - search space
# pos	- position in field
def searchPortalPoint(field,pos):
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
			if isPortal(field,(i,j)):
				portallist.append((i,j))
	return portallist

def getDimensions(field):
	return (len(field), len(field[0]))


# Draws the path in the field
# field - the field to draw on
# path	- the path to draw
def drawPath(field,path):
	tmp = deepcopy(field)
	if path:
		start = path[0]
		goal = path[-1]
		for el in path:
			if el is not start and el is not goal:
				tmp[el[0]][el[1]] = '+'
	return tmp


# This function enables the user to step through iterations and see the current path
# field - search space
# path	- the path to show
def debug(field,path):
	printField(drawPath(field,path))
	print(path)
	input("step")


# Calculate the estimate cost of a given path to the goal position
# When working with portals an optimistic heuristic assumes that the shortest path the minimum of the normal Manhattan distance
# and a shortcut with portals, where the maximum shortcut is given by the 
# Manhattan distance to the nearest portal from the current path + Manhattan distance from the goal to the nearest portal to the goal
# regargless of any more portals taken on the path
# field 	- search space
# path		- the path
# gool_pos	- the goal position
def heuristicCost(field,path,goal_pos):
	PortalList = getPortalList(field)
	if len(PortalList) > 1:
		nearestPortalHead = PortalList[np.argmin([getManhattanDistance(node,path[-1]) for node in PortalList])]
		nearestPortalGoal = PortalList[np.argmin([getManhattanDistance(node,goal_pos) for node in PortalList])]
		return len(path) + min(getManhattanDistance(path[-1],goal_pos),(getManhattanDistance(path[-1],nearestPortalHead)+getManhattanDistance(nearestPortalGoal,goal_pos)))
	return len(path) + getManhattanDistance(path[-1],goal_pos)


# Returns the 4 orthogonal neighbors in 2D Space of a Node
# If the neighbor is a portal the counterpart portalnode gets added instead
# field - search space
# node 	- position in the field
def getNeighbors(field,node):
	w = (node[0] + 1, node[1]  + 0)
	a = (node[0] + 0, node[1]  - 1)
	s = (node[0] - 1, node[1]  + 0)
	d = (node[0] + 0, node[1]  + 1)
	neighborlist = [w,a,s,d]
	for n in neighborlist:
		if isPortal(field,n):
			neighborlist[neighborlist.index(n)] = searchPortalPoint(field,n)
	return neighborlist


# Calculate the Manhattan distance between two points
# pointA	- first point
# pointB	- second point
def getManhattanDistance(pointA, pointB):
	return abs((pointA[0] - pointB[0])) + abs((pointA[1] - pointB[1]))


# Generic Search from a List of Starting Points to a List of Endpoints
# BFS,DFS or A* depends on the given dataStructure
# field 			- search space
# start_pos_list	- list of possible start positions
# end_pos_list		- list of possible end positions
# _dataStructure	- data structure for the frontier (decides which search alg. to use)
# _heuristic		- flag: use heuristics
# _debug			- flag: use debugging method
def genericSearch(field, start_pos_list, end_pos_list, _dataStructure=Queue, _heuristic=False, _debug=False):
	# Init
	visited = []
	frontier = _dataStructure()
	max_frontier_len = 0

	# Put all start positions in the frontier
	for startPos in start_pos_list:
		if _heuristic:
			frontier.put((0,[startPos]))
		else:
			frontier.put([startPos])

	tstart = timer()

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
			if head in end_pos_list:
				tend = timer()
				elapsed_time = tend - tstart
				return [path, len(visited), max_frontier_len, elapsed_time]

			# Iterate over all neighbors
			for neighbor in getNeighbors(field,head):

				# Can we expand in this direction?
				if not isBound(field,neighbor):

					# constuct the new path
					new_path = [n for n in path]
					new_path.append(neighbor)

					# Display the current situation if debug flag is set
					if _debug: debug(field,new_path)

					# Use heuristics if flag is set
					if _heuristic:
						frontier.put((heuristicCost(field,new_path,end_pos_list[0]),new_path))
					else:
						frontier.put(new_path)

	# When the frontier is empty no path was found. Return 0 as path.
	tend = timer()
	elapsed_time = tend - tstart
	return [0, len(visited), max_frontier_len, elapsed_time]


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
def askForAnswer(cli_arg,first_question,following_question,answers=["y","n"]):

	if cli_arg > 1 and len(sys.argv) > cli_arg: answer = sys.argv[cli_arg]

	else: answer = input(first_question + " (" + "|".join(answers) + ") ")

	# Ask until valid answer is given
	while(answer not in answers):
		answer = input(following_question + " (" + "|".join(answers) + ") ")

	if answers == ["y","n"]:
		if answer == "y": return True
		else: return False
	else: return answer


def loadEnvironment(file_path):
	try: field_txt = open(file_path, "r")
	except IOError:
		print("Error: File ", file_path," does not appear to exist.")
		return 1
	else: return [list(line.rstrip('\n')) for line in field_txt]


def runSearch(field,algorithm,debug):# Run the search
	if algorithm not in searches:
		print("Given search is not defined")
		return []
	start_list = [searchFor(field,start_char)]
	goal_list = [searchFor(field,goal_char)]
	if algorithm == "astar": return genericSearch(field,start_list,goal_list,_dataStructure=PriorityQueue,_heuristic=True	,_debug=debug)
	elif algorithm == "dfs": return genericSearch(field,start_list,goal_list,_dataStructure=LifoQueue,	_heuristic=False,_debug=debug)
	elif algorithm == "bfs": return genericSearch(field,start_list,goal_list,_dataStructure=Queue,		_heuristic=False,_debug=debug)


# Main method
def main():
	# Load the field
	try: field = loadEnvironment(sys.argv[1])
	except IndexError:
		print("There hast to be at least one command line argument (path to environment)")
		return 1

	# Print the field
	print("Environment")
	printField(field)

	# Some Info
	print("Character", start_char, "found at", searchFor(field,start_char),
		"\nCharacter", goal_char, "found at", searchFor(field,goal_char))

	# Ask for debug output
	debugFlag	= askForAnswer(3, "Do you want to debug and step through the pathfinding?", "I didn't understand you.")
	howToSearch	= askForAnswer(2, "Which search should I use?", "I didn't understand you.", searches)

	# sr = [path, size of visited[], max-size of frontier & elapsed time]
	sr = runSearch(field,howToSearch,debugFlag)
	print("\nSearch has finished")

	# Print the path
	if len(sr) == 4:
		if(sr[0] == 0): print("No Path found")
		else:
			print(howToSearch.upper(), "Path:\n", sr[0], "\n", "Visualized Path:\n")
			printField(drawPath(field,sr[0])) # Draw the path to the field

		if askForAnswer(4, "Some statistics?", "I didn't understand you."):
			printSearchInfo(sr[3], sr[2] ,sr[1])

		return 0
	else:
		print("Something went horribly wrong")
		return 1


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

