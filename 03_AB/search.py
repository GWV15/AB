#!/usr/bin/python

# Imports
import sys

# Constants
bound	= 'x'
goal	= 'g'
start	= 's'

# Functions
def printField(field):
	for i in range(len(field)):
		print(''.join(field[i]))
	pass

def searchFor(c,field):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)

def searchStart(field):
	return searchFor(start, field)

def bfs(field):
  #find start and goal position
  start_pos = searchStart(field)
  goal_pos= searchFor(goal,field)
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
      if node == goal_pos:
        return path
      #try to expand each path in all directions which havent been visited yet and are not boundaries
      for n in neighbors:
        if (field[n[0]][n[1]] != bound) and all(n not in path for path in frontier):
          path_found = [e for e in path]
          path_found.append(n)
          frontier.append(path_found)

    frontier.remove(path)
  return 0

def updateField(field, path):
  start = path[0]
  goal = path[-1]
  for el in path:
    if el is not start and el is not goal:
      field[el[0]][el[1]] = '+'

#    0    5   10   15  19
#    |    |    |    |   |     
# 00-xxxxxxxxxxxxxxxxxxxx
#    x                  x
#    x       xxx        x
#    x       x xxxxx    x
#    x   s     x        x
# 05-x       x x  xxxxxxx
#    x  xx xxxxx        x
#    x      x      g    x
#    x      x           x
# 09-xxxxxxxxxxxxxxxxxxxx

# loading the field
field = [list(line.rstrip('\n')) for line in open(sys.argv[1])]
print("Environment:\n")
printField(field)
print("\n")

c = 's'
print("Character", c, "found at", searchFor(c,field))
c = 'g'
print("Character", c, "found at", searchFor(c,field))

print("BFS Path:\n")
print(bfs(field))
print("\n")

print("Visualized Path:\n")
updateField(field,bfs(field))
printField(field)
