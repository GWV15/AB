#!/usr/bin/python
# -*- coding: utf-8 -*-

# GWV 15/16 Abgabe
# Tobergte, Budde, Oslani, Bauregger
#
# Johannes Twiefel | Montags 12 - 14 Uhr | F-009 

### Imports			##############################
import sys
import numpy as np ## INSTALL
import time
from copy import deepcopy
from queue import LifoQueue, Queue, PriorityQueue
from timeit import default_timer as timer

import ncursessearch as gui

### Constants		##############################
goal_char	= 'g'
start_char	= 's'
bound_char	= 'x'
searches = ["bfs","dfs","astar"]

### Class			##############################
def MyPriorityQueue(PriorityQueue):
	def get(self):
		return super().get()[-1]


### Functions		##############################
#####################################################################################
# Print the given field
# field - field to print
def print_field(field):
	for i in range(len(field)):
		print(' '.join(field[i]))
#####################################################################################



#####################################################################################
# Search for character in field
# c		- character to find
# field	- search space
def search_for_character(field,c):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)
#####################################################################################



#####################################################################################
# Returns true if pos in field is a boundary
# field - search space
# pos	- position in field
def is_bound(field,pos):
	return field[pos[0]][pos[1]] == bound_char
#####################################################################################



#####################################################################################
# Returns true if pos in field is a Portal
def is_portal(field,pos):
	return field[pos[0]][pos[1]] in [chr(el+ord('0')) for el in range(10)]
#####################################################################################



#####################################################################################
# Returns the position of the other point of the input portal position
# field - search space
# pos	- position in field
def search_portal_point(field,pos):
	portalnumber = field[pos[0]][pos[1]]
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == portalnumber:
				if not (i == pos[0] and j == pos[1]): 
					return (i,j)
#####################################################################################



#####################################################################################
# Returns a list of positions of all portal nodes
# field - search space
def get_portal_list(field):
	portallist = []
	for i in range(len(field)):
		for j in range(len(field[i])):
			if is_portal(field,(i,j)):
				portallist.append((i,j))
	return portallist

def get_dimensions(field):
	return (len(field), len(field[0]))
#####################################################################################



#####################################################################################
# Draws the path in the field
# field - the field to draw on
# path	- the path to draw
#def draw_path(field,path):
#	tmp = deepcopy(field)
#	if path:
#		start = path[0]
#		goal = path[-1]
#		for index in range(len(path)):
#			el = path[index]
#			if el is not start and el is not goal:
#				tmp[el[0]][el[1]] = '+'
#	return tmp

# def draw_path(field,path):
# 	tmp = deepcopy(field)
# 	for index in range(len(path)):
# 		el = path[index]
# 		if el is not path[0] and el is not path[-1]:
# 			for neighbor in get_neighbors(field,el):
# 				if is_portal(field,neighbor) and neighbor == path[index+1]: portal = True
# 				else: portal = False
# 					#Portalsprung
# 			if   path[index+1][1] == path[index][1]-1 or (portal and is_portal(field,(path[index][0]  ,path[index][1]-1))): char = '\u2190' #left
# 			elif path[index+1][0] == path[index][0]-1 or (portal and is_portal(field,(path[index][0]-1,path[index][1]  ))): char = '\u2191' #up
# 			elif path[index+1][1] == path[index][1]+1 or (portal and is_portal(field,(path[index][0]  ,path[index][1]+1))): char = '\u2192' #right
# 			elif path[index+1][0] == path[index][0]+1 or (portal and is_portal(field,(path[index][0]+1,path[index][1]  ))): char = '\u2193' #down
# 			else:
# 				char = '+'
# 			tmp[el[0]][el[1]] = char
# 	return tmp

def draw_path(field,path):
	#tmp = deepcopy(field)
	tmp=[['' for j in range(len(field[0]))] for i in range(len(field))]
	for index in range(len(path[1:])):
		if   path[index+1][1] == path[index][1]-1: char = '\u2190' #left
		elif path[index+1][0] == path[index][0]-1: char = '\u2191' #up
		elif path[index+1][1] == path[index][1]+1: char = '\u2192' #right
		elif path[index+1][0] == path[index][0]+1: char = '\u2193' #down
		else: char = 'P'
		tmp[path[index][0]][path[index][1]] = char

	tmp[path[0][0]][path[0][1]] = start_char
	tmp[path[-1][0]][path[-1][1]] = goal_char
	return tmp
#####################################################################################



#####################################################################################
# Draws the visited points
# field		- the field to draw on
# visited	- list of visited points
def draw_visited(field,visited):
	#tmp = deepcopy(field)
	tmp=[['' for j in range(len(field[0]))] for i in range(len(field))]
	for point in visited:
		tmp[point[0]][point[1]] = 'o'
	return tmp
#####################################################################################



#####################################################################################
# This function enables the user to step through iterations and see the current path
# field 	- search space
# path		- the path to show
# visited	- list of visited points (optional)
def debug(field,path,visited=[],neighbors=[],curses=None):
	print(path)
	print_field(draw_path(field,path))
	#if visited: print_field(draw_visited(field,visited))
	input("step")
#####################################################################################



#####################################################################################
# Calculate the estimate cost of a given path to the goal position
# When working with portals an optimistic heuristic assumes that the shortest path the minimum of the normal Manhattan distance
# and a shortcut with portals, where the maximum shortcut is given by the 
# Manhattan distance to the nearest portal from the current path + Manhattan distance from the goal to the nearest portal to the goal
# regargless of any more portals taken on the path
# field 	- search space
# path		- the path
# gool_pos	- the goal position
def heuristic_cost(field,path,goal_pos):
	PortalList = get_portal_list(field)
	if len(PortalList) > 1:
		nearestPortalHead = PortalList[np.argmin([get_manhattan_distance(node,path[-1]) for node in PortalList])]
		nearestPortalGoal = PortalList[np.argmin([get_manhattan_distance(node,goal_pos) for node in PortalList])]
		return len(path) + min(get_manhattan_distance(path[-1],goal_pos),(get_manhattan_distance(path[-1],nearestPortalHead)+get_manhattan_distance(nearestPortalGoal,goal_pos)))
	return len(path) + get_manhattan_distance(path[-1],goal_pos)
#####################################################################################



#####################################################################################
# Returns the 4 orthogonal neighbors in 2D Space of a Node
# If the neighbor is a portal the counterpart portalnode gets added instead
# field - search space
# node 	- position in the field
def get_neighbors(field,node):
	w = (node[0] + 1, node[1]  + 0)
	a = (node[0] + 0, node[1]  - 1)
	s = (node[0] - 1, node[1]  + 0)
	d = (node[0] + 0, node[1]  + 1)
	neighborlist = [w,a,s,d]
	for n in neighborlist:
		if is_portal(field,n):
			neighborlist[neighborlist.index(n)] = search_portal_point(field,n)
	return neighborlist
#####################################################################################



#####################################################################################
# Calculate the Manhattan distance between two points
# pointA	- first point
# pointB	- second point
def get_manhattan_distance(pointA, pointB):
	return abs((pointA[0] - pointB[0])) + abs((pointA[1] - pointB[1]))
#####################################################################################



#####################################################################################
# Generic Search from a List of Starting Points to a List of Endpoints
# BFS,DFS or A* depends on the given dataStructure
# field 			- search space
# start_pos_list	- list of possible start positions
# end_pos_list		- list of possible end positions
# _dataStructure	- data structure for the frontier (decides which search alg. to use)
# _heuristic		- flag: use heuristics
# _debug			- flag: use debugging method
def generic_search(field, start_pos_list, end_pos_list, _dataStructure=Queue, _heuristic=False, _debug=False, _curses=None):
	# Init
	visited = []
	frontier = _dataStructure()

	# Put all start positions in the frontier
	for startPos in start_pos_list:
		if _heuristic: frontier.put((0,[startPos]))
		else: frontier.put([startPos])

	# Search as long as the frontier has some entries left
	while not frontier.empty():
		# Get the next path 
		path = []
		if _heuristic: path = frontier.get()[-1]
		else: path = frontier.get()

		# Get the node we want to expand
		head = path[-1]

		# Don't visit a node twice
		if head not in visited:
			
			# Remember we were here
			visited.append(head)
			
			# Are we finished?
			if head in end_pos_list:
				return [path, visited] #TODO

			# Iterate over all neighbors
			neighbors = get_neighbors(field,head)
			for neighbor in neighbors:

				# Can we expand in this direction?
				if not is_bound(field,neighbor):

					# constuct the new path
					new_path = [n for n in path]
					new_path.append(neighbor)

					# Display the current situation if debug flag is set
					#if _debug: debug(field,new_path)
					if _debug: debug(field,new_path,visited,neighbors) #TODO

					# Use heuristics if flag is set
					if not _heuristic: frontier.put(new_path)
					else: frontier.put((heuristic_cost(field,new_path,end_pos_list[0]),new_path))

	# Start time measurement
	tend = timer()
	elapsed_time = tend - tstart
	
	# When the frontier is empty no path was found. Return 0 as path.
	return [0, len(visited), max_frontier_len, elapsed_time]
#####################################################################################



#####################################################################################
# Print statistics collected each search
# time			- time elapsed while searching
# max_frontier	- Max number of elements in frontier while searching
# visit_count	- Number of elements visited
def printSearchInfo(time,max_frontier,visit_count, disableTime):
	if not disableTime: print("Time: ", time)
	print("Biggest frontier had ", max_frontier, " Elements")
	print("The search \"visited\" ", visit_count, " Points")
#####################################################################################



#####################################################################################
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
#####################################################################################



#####################################################################################
def load_environment(file_path):
	try: field_txt = open(file_path, "r")
	except IOError:
		print("Error: File ", file_path," does not appear to exist.")
		return 1
	else: return [list(line.rstrip('\n')) for line in field_txt]
#####################################################################################



#####################################################################################
def run_search(field,algorithm,debug,curses=None):# Run the search
	if algorithm not in searches:
		print("Given search is not defined")
		return []
	start_list = [search_for_character(field,start_char)]
	goal_list = [search_for_character(field,goal_char)]
	if algorithm == "astar": return generic_search(field,start_list,goal_list,_dataStructure=PriorityQueue,	_heuristic=True	,_debug=debug,_curses=curses)
	elif algorithm == "dfs": return generic_search(field,start_list,goal_list,_dataStructure=LifoQueue,		_heuristic=False,_debug=debug,_curses=curses)
	elif algorithm == "bfs": return generic_search(field,start_list,goal_list,_dataStructure=Queue,			_heuristic=False,_debug=debug,_curses=curses)
#####################################################################################



#####################################################################################
### Main method
#####################################################################################
def main():
	# Load the field
	try: field = load_environment(sys.argv[1])
	except IndexError:
		print("There hast to be at least one command line argument (path to environment)")
		return 1

	# Print the field
	print("Environment")
	print_field(field)

	#gui.init_gui(field,get_dimensions(field),searches)
	#guiResult = gui.start_gui()
	guiResult = False
	if not guiResult:
		#gui.end_gui()
		print("foo")
	else:
		howToSearch = guiResult[0]
		debugging = guiResult[1]
		if debugging == "no": debugFlag = False
		else: debugFlag = True

		sr = run_search(field,howToSearch,debugFlag)
		#updateEnvironment(path,field_path,field_visited,neighbors)
		gui.updateEnvironment(sr[0],draw_path(field,sr[0]),draw_visited(field,sr[1]),[])
		
		#input()

		gui.end_gui()
		#return "bar"


	# Some Info
	print("Character", start_char, "found at", search_for_character(field,start_char),
		"\nCharacter", goal_char , "found at", search_for_character(field,goal_char))

	# Ask for search and debug output
	howToSearch	= askForAnswer(2, "Which algorithm should I use?", "I didn't understand you.", searches)
	debugFlag	= askForAnswer(3, "Do you want to debug and step through the pathfinding?", "I didn't understand you.")
	# sr = [path, size of visited[], max-size of frontier & elapsed time]
	sr = run_search(field,howToSearch,debugFlag)
	print("\nSearch has finished")

	print(sr[0])
	print_field(draw_path(field,sr[0]))

	# Print the path
	if len(sr) == 4:
		if(sr[0] == 0): print("No Path found")
		else:
			print(howToSearch.upper(), "Path:\n", sr[0], "\n", "Visualized Path:\n")
			print_field(draw_path(field,sr[0])) # Draw the path to the field

		#if askForAnswer(4, "Some statistics?", "I didn't understand you."):
		#	printSearchInfo(sr[3], sr[2] ,sr[1], debugFlag)

		return 0
	else:
		print("Something went horribly wrong")
		print(sr[0])
		return 1

### Start ##############################
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
	print(main())

