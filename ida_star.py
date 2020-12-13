### Importing libraries
from cube import make_move, scramble
from queue import PriorityQueue
import numpy as np
from datetime import datetime
import time

################
#--- OTHERS ---#
################

### Initial cube display
initial_array = np.array([
    ['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W'],
    ['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G'],
    ['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R'],
    ['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B'],
    ['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O'],
    ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']
])

### Manhattan distance helper
array = np.array([
    [[0, 0, 2], [1, 0, 2], [2, 0, 2]],
    [[0, 0, 1], [1, 0, 1], [2, 0, 1]],
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    [[0, 0, 2], [0, 1, 2], [0, 2, 2]],
    [[0, 0, 1], [0, 1, 1], [0, 2, 1]],
    [[0, 0, 0], [0, 1, 0], [0, 2, 0]],
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
    [[0, 1, 0], [1, 1, 0], [2, 1, 0]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],
    [[2, 0, 0], [2, 0, 1], [2, 0, 2]],
    [[2, 1, 0], [2, 1, 1], [2, 1, 2]],
    [[2, 2, 0], [2, 2, 1], [2, 2, 2]],
    [[2, 0, 2], [1, 0, 2], [0, 0, 2]],
    [[2, 1, 2], [1, 1, 2], [0, 1, 2]],
    [[2, 2, 2], [1, 2, 2], [0, 2, 2]],
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],
    [[0, 2, 1], [1, 2, 1], [2, 2, 1]],
    [[0, 2, 2], [1, 2, 2], [2, 2, 2]],
])

##########################
#--- AUXILIAR CLASSES ---#
##########################

### State class for each cube movement
class State:
    def __init__(self):
        self.cube = None
        self.g = 0
        self.h = 0
        self.parent = None
        self.move = None

### Modified priority queue for better usage
class my_priority_queue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item

############################
#--- AUXILIAR FUNCTIONS ---#
############################

### Check if current state is goal
def is_goal(curr):
    if curr.h != 0:
        return False
    return True

### Unroll all movements to reach current state
def unroll(curr):
    movements = []
    while curr.parent is not None:
        parent = curr.parent
        movements.append(curr.move)
        curr = parent
    return movements

### Check if child is not it's own grandparent
def is_grandparent_child(child, parent):
    curr = parent.parent
    while curr is not None:
        if np.array_equal(curr.cube, child): 
            return True
        curr = curr.parent
    return False

### Check if child is already on the priority queue
def is_child_in_queue(child, queue):
    for curr_item in queue.queue:
        if np.array_equal(curr_item[2].cube, child):
            return True
    return False

###
def to_linear_array(arr):
    linear_array = []
    indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
    for i in indexes:
        for j in range(len(arr[i])):
            linear_array.append(arr[i][j])
    return np.array(linear_array)

###
def to_main_array(arr):
    main_array = []
    indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
    for i in indexes:
        main_array.append(arr[i*3:(i+1)*3])
    return np.array(main_array)

########################
#--- MAIN ALGORITHM ---#
########################

### IDA* algorithm
def IDA(start):
    start.h = corner_edge_sum_max(start.cube)
    cost_limit = start.h
    nodes = 0
    queue = my_priority_queue()
    branching_factors = list()
    while True:
        minimum = None
        queue.put(start, start.h)
        while not queue.empty():
            curr = queue.get()
            if is_goal(curr):
                print('Goal Height:', curr.g)
                print("Nodes Generated:", nodes)
                print("Movements to Solve: ", unroll(curr))
                return unroll(curr)
            b = 0
            nodes = nodes + 12
            for i in range(12):
                new = State()
                new.cube = np.array(curr.cube)
                new.g = curr.g + 1
                new.parent = curr
                new.move = make_move(new.cube, i + 1)
                new.h = corner_edge_sum_max(new.cube)

                if new.g + new.h > cost_limit:
                    if minimum is None or new.g + new.h < minimum:
                        minimum = new.g + new.h
                    continue
                if curr.parent is not None and (is_grandparent_child(new.cube, curr) or is_child_in_queue(new.cube, queue)):
                    continue
                queue.put(new, new.h)
                b = b + 1
            if b != 0:
                branching_factors.append(b)
        cost_limit = minimum

### Calculate the Manhattan distance for each piece on the cube
def manhattan_distance(cube, i, z, corner):
    c1 = array[i, z]
    center = None
    for c in [1, 4, 7, 10, 13, 16]:
        if cube[i, z] == cube[c, 1]:
            center = c
            break
    if corner:
        c_t = array[center - 1, 0]
        d1 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        c_t = array[center - 1, 2]
        d2 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        c_t = array[center + 1, 0]
        d3 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        c_t = array[center + 1, 2]
        d4 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        return min(d1, d2, d3, d4)
    else:
        c_t = array[center - 1, 1]
        d1 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        c_t = array[center, 0]
        d2 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        c_t = array[center, 2]
        d3 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        c_t = array[center + 1, 1]
        d4 = abs(c1[0] - c_t[0]) + abs(c1[1] - c_t[1]) + abs(c1[2] - c_t[2])
        return min(d1, d2, d3, d4)

### Calculate max between corners sum or edges sum
def corner_edge_sum_max(cube):
    corners = 0
    edges = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners += manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges += manhattan_distance(cube, i, 1, False)
        else:
            edges += manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return max(corners / 8, edges / 12)


#########################
#--- TIMER FUNCTIONS ---#
#########################

def init_timer():
    time.ctime()
    fmt = '%H:%M:%S'
    start = time.strftime(fmt)
    print("Started process")
    return fmt, start

def end_timer(fmt, start):
    time.ctime()
    end = time.strftime(fmt)
    print("Time taken(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))


######################
#--- MAIN PROCESS ---#
######################

def main(array):
    curr = State()
    #scrambled_list = scramble(array, scramble_moves)
    curr.cube = np.array(array)
    #print(curr.cube)
    #print("Movements to Scramble: ", scrambled_list)
    solution_list = IDA(curr)
    return solution_list


#if __name__ == "__main__":
#    fmt, start = init_timer()
#    main(5)
#    end_timer(fmt, start)
