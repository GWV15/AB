#!/usr/bin/python

import sys

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

field = [line.rstrip('\n') for line in open(sys.argv[1])]

def printField(field):
	for i in range(len(field)):
		print(field[i])
	pass


def searchStart(field):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if field[i][j] == 's': return(i,j)

print("Starting point at", searchStart(field))
 