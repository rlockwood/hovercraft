import time
from collections import deque
import sys
import os

maze = [["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#",".",".",".",".","."],
		["#","*","#","#","#","#","#",".",".",".",".",".",".",".","#",".",".",".",".","."],
		["#",".","#","#","#","#",".",".",".",".",".","#","#",".","#",".",".",".",".","."],
		["#",".",".",".",".",".",".","#","#","#","#","#","#",".","#",".",".",".",".","."],
		[".",".",".","#","#","#","#","#","#",".",".",".","#",".","#",".",".",".",".","."],
		[".","#",".","#","#","#","#","#","#",".",".",".","#",".","#",".",".",".",".","."],
		[".",".",".","#","#","#","#","#","#",".",".",".","#",".","#",".","#","#","#","."],
		["#","#","#","#",".",".","#","#",".",".",".",".","#",".","#",".","#","#","#","."],
		["#","#",".",".",".",".","#","#",".",".",".",".","#",".","#",".","#","#","#","."],
		["#",".",".",".",".",".","#","#",".",".",".",".","#",".","#",".","#","#","#","."],
		[".",".",".",".",".",".",".","#",".",".","#",".","#",".","#",".","#","#","#","."],
		["#",".",".",".","#",".",".","#",".",".","#",".","#",".","#",".","#","#","#","."],
		[".",".",".",".","#",".",".","#",".",".","#",".",".",".","#",".","#","#","#","."],
		[".",".",".",".","#",".",".",".",".",".","#",".",".",".","#",".","#","#","#","."],
		[".",".",".",".","#",".",".",".",".",".","#",".",".","#","#",".","#","#","#","."],
		[".",".",".",".","#","#","#","#","#","#","#","#","#","#",".",".","#","#","#","."],
		[".","#",".","#","#","#","#","#","#","#","#","#","#","#",".",".","#","#","#","."],
		[".","#","#","#","#","#","#","#","#","#","#","#","#","#",".",".","#","#","#","."],
		[".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","#","@",".","#"],
		["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"]]

foundnodes = {}

frontiernodes = deque()

startnode = None

vehiclestate = None


def printmaze():

	outstring = ""

	for j in range(len(maze)):
		for i in range(len(maze[j])):
			if vehiclestate[0] == i and vehiclestate[1] == j:
				outstring += "@"
			else:
				outstring += maze[j][i]
		outstring += "\n"

	print(outstring)


def iswall(x, y):
	return x < 0 or y < 0 or y >= len(maze) or x >= len(maze[y]) or maze[y][x] == "#"

#shamelessly ripped off from http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
def ismovelegal(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        if iswall(*coord):
        	return False
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    return True

def addmove(currnode, movecommand):

	newnode = None

	if movecommand == "left":
		newnode =                (currnode[0] - currnode[2], currnode[1] - currnode[3], currnode[2] + 1, currnode[3]    )
	elif movecommand == "right":
		newnode =                (currnode[0] - currnode[2], currnode[1] - currnode[3], currnode[2] - 1, currnode[3]    )
	elif movecommand == "up":
		newnode =                (currnode[0] - currnode[2], currnode[1] - currnode[3], currnode[2],     currnode[3] + 1)
	elif movecommand == "down":
		newnode =                (currnode[0] - currnode[2], currnode[1] - currnode[3], currnode[2],     currnode[3] - 1)
	elif movecommand == "hold":
		newnode =                (currnode[0] - currnode[2], currnode[1] - currnode[3], currnode[2],     currnode[3]    )



	if newnode not in foundnodes and ismovelegal((newnode[0], newnode[1]), (currnode[0], currnode[1])):
		foundnodes[newnode] = movecommand
		frontiernodes.append(newnode)
	
	return newnode == startnode



def search():
	currnode = frontiernodes.popleft()

	return addmove(currnode, "left") or addmove(currnode, "right") or addmove(currnode, "up") or addmove(currnode, "down") or addmove(currnode, "hold")

def move():

	global vehiclestate

	currmove = foundnodes[vehiclestate]

	if currmove == "left":
		vehiclestate = (vehiclestate[0], vehiclestate[1], vehiclestate[2] - 1, vehiclestate[3])
	elif currmove == "right":
		vehiclestate = (vehiclestate[0], vehiclestate[1], vehiclestate[2] + 1, vehiclestate[3])
	elif currmove == "up":
		vehiclestate = (vehiclestate[0], vehiclestate[1], vehiclestate[2], vehiclestate[3] - 1)
	elif currmove == "down":
		vehiclestate = (vehiclestate[0], vehiclestate[1], vehiclestate[2], vehiclestate[3] + 1)
	elif currmove == "hold":
		pass
	elif currmove == "finish":
		return True

	vehiclestate = (vehiclestate[0] + vehiclestate[2], vehiclestate[1] + vehiclestate[3], vehiclestate[2], vehiclestate[3])

	return False


# tuple is structured (x, y, dx, dy)
# valid moves are left, right, up, down, hold, and finish

startfound = False
endfound = False
for j in range(len(maze)):
	for i in range(len(maze[j])):
		if maze[j][i] == "*":
			#maze[j][i] = "."
			foundnodes[(i, j, 0, 0)] = "finish"
			frontiernodes.append((i, j, 0, 0))
			endfound = True
		elif maze[j][i] == "@":
			maze[j][i] = "."
			startnode = (i, j, 0, 0)
			startfound = True

		if startfound and endfound:
			break

if not startfound and not endfound:
	print("start or end not found in maze")
	sys.exit()

pathfound = False

while not pathfound:
	pathfound = search()
	print("nodes: {}/{}".format(len(frontiernodes), len(foundnodes)))

vehiclestate = startnode
printmaze()

print("READY")
input()

userinput = None

while userinput != "q" and userinput != "Q":
	vehiclestate = startnode

	gameover = False

	while not gameover:
		gameover = move()
		os.system("cls")
		printmaze()
		print(vehiclestate)
		time.sleep(1.0 / 15.0)

	userinput = input("type q to quit: ")


