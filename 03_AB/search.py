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
  start = searchStart(field)
  frontier = [[start]]
  while len(frontier)>0:
    for path in frontier:
      node = path[-1]
      w = (node[0] + 1, node[1]  + 0)
      a = (node[0] + 0, node[1]  - 1)
      s = (node[0] - 1, node[1]  + 0)
      d = (node[0] + 0, node[1]  + 1)

      if field[node[0]][node[1]] == goal:
        return path
      if (field[w[0]][w[1]] != bound) and all(w not in path for path in frontier):
        path_found = [e for e in path]
        path_found.append(w)
        frontier.append(path_found)
       
      if (field[a[0]][a[1]] != bound) and all(a not in path for path in frontier):
        path_found = [e for e in path]
        path_found.append(a)
        frontier.append(path_found)

      if (field[s[0]][s[1]] != bound) and all(s not in path for path in frontier):
        path_found = [e for e in path]
        path_found.append(s)
        frontier.append(path_found)

      if (field[d[0]][d[1]] != bound) and all(d not in path for path in frontier):
        path_found = [e for e in path]
        path_found.append(d)
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
