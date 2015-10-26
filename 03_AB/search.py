#!/usr/bin/python

import sys

lines = [line.rstrip('\n') for line in open(sys.argv[1])]

goal = 'g'

def bfs(space):
  start = searchstart(space)
  frontier = [[start]]
  while len(frontier)>0:
    for path in frontier:
      frontier.remove(path)
      node = path[-1]
      if space[node[0]][node[1]] = goal:
        return path
      if space[node[0]+1][node[1]+0] != x:
        frontier.append(path.append(node[0]+1,node[1]+0))
      if space[node[0]+0][node[1]+1] != x:
        frontier.append(path.append(node[0]+0,node[1]+1))
      if space[node[0]-1][node[1]+0] != x:
        frontier.append(path.append(node[0]-1,node[1]+0))
      if space[node[0]+0][node[1]-1] != x:
        frontier.append(path.append(node[0]+0,node[1]-1))
  # index out of bounds muss noch ausgeschlossen werden
  return 0
