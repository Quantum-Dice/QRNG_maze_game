import turtle as t
import qrnglib

# Test the QRNG API 
print(f" {'TEST QRNG init (0 => success)' :30}  {qrnglib.qrng_init()} " )
print(f" {'QRNG urand (double 0.0 - 1.0)' :30}  {qrnglib.qrng_urand()}" )
print(f" {'TEST QRNG get status ' :30}  {qrnglib.qrng_get_status()}" )
if qrnglib.qrng_get_status() != 0:
    print(""" 
    QRNG not initialized, try any of the following: 
    1. Ensure the QRNG hardware is plugged in
    2. Try running the application as a super user (i.e. with 'sudo')   
    """)
    exit() 


# INITIALIZING

screen = t.Screen()
screen.title("Turtle Maze")
t.speed(0)


# WALL ARRAY GENERATION

import numpy as np

wall = np.zeros((400,400))
wall[380:, 380:] = 2

# PATH GENERATION

height = 20
width = 20

array = np.zeros((width, height, 5), dtype=int)

def opposite_direction(direction):
    if direction == 1:
        return 2  # up, opposite is down
    elif direction == 2:
        return 1  # down, opposite is up
    elif direction == 3:
        return 4  # left, opposite is right
    else:
        return 3  # right, opposite is left

difficulty = [1,0] # Rough measure of length of path from beginning to end

def is_valid(x, y):
    return x >= 0 and x < width and y >= 0 and y < height

# Main thing

def generate_maze(y, x):
    array[y, x, 0] = 1  # Mark first cell as visited

    # Shuffle the directions to visit neighbors in random order (until success)
    directions = [(0, -1, 1), (0, 1, 2), (-1, 0, 3), (1, 0, 4)] #up, down, left, right
    qrnglib.qrng_shuffle(directions)

    for dx, dy, d_index in directions:
        new_x, new_y = x + dx, y + dy
        if is_valid(new_x, new_y) and array[new_y, new_x, 0] == 0:
            if new_x == 19 and new_y == 0:
                difficulty[1] = difficulty[0]
            array[y, x, d_index] = 1  # Make connection to other cell
            array[new_y, new_x, opposite_direction(d_index)] = 1 # Make connection from other cell
            difficulty[0] += 1
            generate_maze(new_y, new_x)

    # Check if all neighbors have been visited
    visited_neighbors = sum(array[y, x, 1:])
    if visited_neighbors < 4:
        return

    # Backtrack and continue generation from other cells
    for dx, dy, d_index in directions:
        new_x, new_y = x + dx, y + dy
        if is_valid(new_x, new_y) and array[new_y, new_x, 0] == 1:
            generate_maze(new_y, new_x)


# Start maze generation from the bottom-left corner (start)
generate_maze(19, 0)

# Nice little bit to display the maze for debugging purposes
'''
for y in range(height):
    for x in range(width):
        print(array[y, x, 1:], end=' ')
    print()
'''

# TURN MAZE ARRAY INTO WALLS

t.penup()
t.goto(-200,-200)
t.fillcolor('red')
t.begin_fill()
for i in range(4):
    t.forward(20)
    t.left(90)
t.end_fill()
t.goto(180,180)
t.fillcolor('green')
t.begin_fill()
for i in range(4):
    t.forward(20)
    t.left(90)
t.end_fill()

def drawcell(x,y,u,d,l,r):
    t.goto(x * 20 - 200, 200 - y * 20)
    if u == 0:
        t.pendown()
        for i in range(20):
            wall[399 - y * 20][x * 20 + i] = 1
    t.forward(20)
    t.right(90)
    t.penup()
    if r == 0:
        t.pendown()
        for i in range(20):
            wall[399 - y * 20 - i][x * 20 + 19] = 1
    t.forward(20)
    t.right(90)
    t.penup()
    if d == 0:
        t.pendown()
        for i in range(20):
            wall[399 - y * 20 - 19][x * 20 + i] = 1
    t.forward(20)
    t.right(90)
    t.penup()
    if l == 0:
        t.pendown()
        for i in range(20):
            wall[399 - y * 20 - i][x * 20] = 1
    t.forward(20)
    t.right(90)
    t.penup()
    

for y in range(height):
    for x in range(width):
        up = array[y][x][1]
        down = array[y][x][2]
        left = array[y][x][3]
        right = array[y][x][4]

        drawcell(x,y,up,down,left,right)

# SEND TURTLE TO START

t.goto(-190, -190)
t.left(90)

# MOVEMENT

moving_forward = False
moving_backward = False
turning_left = False
turning_right = False

def start_forward():
    global moving_forward
    moving_forward = True

def stop_forward():
    global moving_forward
    moving_forward = False

def start_backward():
    global moving_backward
    moving_backward = True

def stop_backward():
    global moving_backward
    moving_backward = False

def start_left():
    global turning_left
    turning_left = True

def stop_left():
    global turning_left
    turning_left = False

def start_right():
    global turning_right
    turning_right = True

def stop_right():
    global turning_right
    turning_right = False

import time

time_start = time.time()

prev_x_pos = int(t.pos()[0] + 200)
prev_y_pos = int(t.pos()[1] + 200)

def update():
    global prev_x_pos, prev_y_pos

    x_pos = int(t.pos()[0] + 200)
    y_pos = int(t.pos()[1] + 200)
    
    if wall[y_pos - 1][x_pos - 1] == 0:
        if moving_forward:
            t.forward(1)
        if moving_backward:
            t.backward(1)
        if turning_left:
            t.left(5)
        if turning_right:
            t.right(5)
    elif wall[y_pos - 1][x_pos - 1] == 2:
        time_total = time.time() - time_start
        print("Complete.")
        print(f"Difficulty: {int(difficulty[1] / 4)}%") # skew of distribution due to distances < 40 not being possible
        print(f"Time: {int(time_total)} seconds.")
        score = int((100 * difficulty[1]) // time_total)
        print(f"Score: {score}.")
        exit()
    else:
        t.goto(prev_x_pos - 200, prev_y_pos - 200)

    prev_x_pos = x_pos
    prev_y_pos = y_pos
    
    screen.ontimer(update, 1)



screen.onkeypress(start_forward, "Up")
screen.onkeyrelease(stop_forward, "Up")
screen.onkeypress(start_backward, "Down")
screen.onkeyrelease(stop_backward, "Down")
screen.onkeypress(start_left, "Left")
screen.onkeyrelease(stop_left, "Left")
screen.onkeypress(start_right, "Right")
screen.onkeyrelease(stop_right, "Right")

update()

screen.listen()

t.done()
