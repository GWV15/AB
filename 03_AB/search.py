#!/usr/bin/python

# Imports
import sys

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
	return searchFor('s', field)


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
print("Environment:")
printField(field)

c = 's'
print("Character", c, "found at", searchFor(c,field))
c = 'g'
print("Character", c, "found at", searchFor(c,field))
 