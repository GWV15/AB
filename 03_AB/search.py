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
		print(field[i])
	pass

def searchFor(c,field):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == c: return (i,j)

def searchStart(field):
	return searchFor(start, field)

def bfs(field):
  start = searchStart(field)
  frontier = [[start]]
  while len(frontier)>0:
    for path in frontier:
      print("frontier: " ,frontier)
      print("path: " , path)
      node = path[-1]
      if field[node[0]][node[1]] == goal:
        return path
      if field[node[0] + 1][node[1] + 0] != bound:
        print("Right Neighbor found")
        frontier.append(path.append((node[0] + 1, node[1] + 0)))

      if field[node[0] + 0][node[1] + 1] != bound:
        frontier.append(path.append((node[0] + 0, node[1] + 1)))
        print("Top Neighbor found")

      if field[node[0] - 1][node[1] + 0] != bound:
        frontier.append(path.append((node[0] - 1, node[1] + 0)))
        print("Below Neighbor found")

      if field[node[0] + 0][node[1] - 1] != bound:
        frontier.append(path.append((node[0] + 0, node[1] - 1)))
        print("Left Neighbor found")

    frontier.remove(path)
  print (frontier)
  return 0


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
field = [line.rstrip('\n') for line in open(sys.argv[1])]
print("Environment:\n")
printField(field)
print("\n")

c = 's'
print("Character", c, "found at", searchFor(c,field))
c = 'g'
print("Character", c, "found at", searchFor(c,field))

bfs(field)
