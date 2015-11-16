#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses
import sys

debug = ["no","man","1s","100ms"]
debugging = debug[0]

searches = []
search = ""

stdscr = None
win_env = None
win_vis = None
win_text = None
win_flag = None
win_keys = None

def init_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.bkgd(curses.color_pair(1))
    stdscr.box()
    stdscr.refresh()
    return stdscr

def init_win(dim,pos,colorid,title):
	#hoehe, breite, topdiff, rightdiff
	win = curses.newwin(dim[0],dim[1],pos[0],pos[1])
	win.bkgd(curses.color_pair(colorid))
	win.box()
	win.addstr(0, 2, title)
	win.refresh()
	return win

#def draw_env_to_win(field,win):
#	for i in range(len(field)):
#		win.addstr(i + 1, 1, ''.join(field[i]))
#	win.refresh()

def draw_env_to_win(field,win,do_not_draw=[' ']):
	for i in range(len(field)):
		for j in range(len(field[i])):
			if not field[i][j] in do_not_draw:
				win.addstr(i + 1, j + 1, field[i][j])
	win.refresh()


def toggleSearch(win):
	global search
	search = getNext(searches, search)
	win.addstr(2,  1, "Search:")
	win.addstr(2, 10, "     ")
	win.addstr(2, 10, search)
	win.refresh()

def toggleDebug(win):
	global debugging
	debugging = getNext(debug, debugging)
	win.addstr(4,  1, "Debug:")
	win.addstr(4, 10, "     ")

	win.addstr(4, 10, debugging)
	win.refresh()

def getNext(xs,item=""):
	if item not in xs:
		index = 0
	else:
		index = xs.index(item) + 1
		if index == len(xs):
			index = 0
	return xs[index]

def updateEnvironment(path,field_path,field_visited,neighbors):
	for point in neighbors:
		field_path[point[0]][point[1]] = "@"
	field_path[path[-1][0]][path[-1][1]] = "X"

	win_env.bkgd(curses.color_pair(1))
	win_vis.bkgd(curses.color_pair(1))

	do_not_draw = [' ','x','1','2','3','4','5']
	draw_env_to_win(field_path,win_env,do_not_draw)
	draw_env_to_win(field_visited,win_vis,do_not_draw)

def init_gui(field,dim,searchlist):

	global searches
	global search
	global stdscr
	global win_env
	global win_vis
	global win_text
	global win_flag
	global win_keys
	
	searches = searchlist
	search = getNext(searches)

	stdscr = init_curses()
	# Window Placement
	#					heigh		width			top				left			col		name
	win_env  = init_win((dim[0]+2	,2*dim[1]-1+2)		,(2				,2)				,2		,"Current Path")
	win_vis  = init_win((dim[0]+2	,2*dim[1]-1+2)		,(2				,dim[1]+2+12)	,2		,"Visited")
	win_text = init_win((10			,dim[1]+2+16)	,(dim[0]+2+2	, 2)			,2		,"")
	win_flag = init_win((10			,16)			,(dim[0]+2+2	,dim[1]+2+16+2)	,2		,"Settings")
	win_keys = init_win((3			,dim[1]+34)		,(dim[0]+4+10	,2)				,2		,"")

	draw_env_to_win(field,win_env)
	draw_env_to_win(field,win_vis)

	toggleSearch(win_flag)
	toggleDebug(win_flag)

	win_text.addstr(1, 1, "Environment is displayed above.")
	win_text.addstr(2, 1, "")
	win_text.refresh()

	win_keys.addstr(1,1, "(a)lgorithm (d)ebug | (s)tart | (q)uit")
	win_keys.refresh()

	stdscr.addstr(5, 25, "Start: s")
	stdscr.addstr(6, 25, "Goal:  g")
	stdscr.addstr(7, 25, "Bound: x")

	stdscr.refresh()

def start_gui():
	while True:
		c = stdscr.getch()
		if   c == ord('a'): toggleSearch(win_flag)
		elif c == ord('d'): toggleDebug(win_flag)
		elif c == ord('q'): return False
		elif c == ord('s'): return search,debugging
		#elif c == ord('l'): loadEnv(win_env,win_vis)
		#elif c == curses.KEY_MOUSE:
		#	id, x, y, z, button = curses.getmouse()
		#	s = "Mouse-Ereignis bei (%d ; %d ; %d), ID= %d, button = %d" % (x, y, z, id, button)
		#	stdscr.addstr(1, 1, s)
		#	stdscr.clrtoeol()
		#	stdscr.refresh()

def end_gui():
	global stdscr
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()