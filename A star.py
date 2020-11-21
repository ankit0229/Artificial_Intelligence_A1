# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:09:48 2019

@author: ANKIT
"""
import time
from collections import deque
moving = []
side = int(input("Enter matrix side :"))
print("Enter %s X %s matrix for initial_state:" % (side, side))
initial_state = []
for i in range(side):
    initial_state.append(list(map(int, input().split())))
print("Enter %s X %s matrix for final_state:" % (side, side))
final_state = []
for i in range(side):
    final_state.append(list(map(int, input().split())))
    
moves = -1
n = len(initial_state)
initial_zero_position = (-1, -1)
start = time.time()

for i, row in enumerate(initial_state):
    for j, element in enumerate(row):
        if element == 0:
            initial_zero_position = (i, j)

# Get the heuristics.
map_for_final_state = dict()
for i,row in enumerate(final_state):
    for j,ele in enumerate(row):
        map_for_final_state[final_state[i][j]] = (i,j)
def get_heuristic_for_state(current_state):
    map_for_current_state = dict()
    for i,row in enumerate(current_state):
        for j,ele in enumerate(row):
            map_for_current_state[current_state[i][j]] = (i,j)
    total_heristics = 0
    for key in map_for_current_state:
        total_heristics += (abs(map_for_current_state[key][0] - map_for_final_state[key][0]) +
                            abs(map_for_current_state[key][1] - map_for_final_state[key][1]))
    return total_heristics


state_array = [initial_state]
state_heuristics = [get_heuristic_for_state(initial_state)]
state_previous_position = [initial_zero_position]
state_current_zero_position = [initial_zero_position]

visited_states = []
to_string = lambda y : (",".join([",".join(map(str,x)) for x in y]))
visited_states.append(to_string(initial_state))

# Gives pos of the minimum heuristics.
def get_minimum_heuristics_position(state_heuristics):
    if len(state_heuristics) == 0:
        return -1
    minim = state_heuristics[0]
    pos = 0
    for i,heuristics in enumerate(state_heuristics):
        if heuristics < minim:
            minim = heuristics
            pos = i
    return pos

operation_map = {(0,1):"right", (1,0):"down", (0,-1):"left", (-1, 0):"up", (0,0):"start"}

import random
operations = [(0,1), (1,0), (0, -1), (-1, 0)]
while len(state_array) > 0:
    # Choose the state with minimum heuristics.
    minimum_heuristics_pos = get_minimum_heuristics_position(state_heuristics)
    state_array_ele = state_array[minimum_heuristics_pos]
    state_heuristics_ele = state_heuristics[minimum_heuristics_pos]
    state_previous_position_ele = state_previous_position[minimum_heuristics_pos]
    state_current_zero_position_ele = state_current_zero_position[minimum_heuristics_pos]
    del state_array[minimum_heuristics_pos]
    del state_heuristics[minimum_heuristics_pos]
    del state_previous_position[minimum_heuristics_pos]
    del state_current_zero_position[minimum_heuristics_pos]
   
    import numpy
    move = tuple(numpy.subtract(state_current_zero_position_ele,state_previous_position_ele))
    moves = moves + 1
    print(str(state_array_ele) + "    " + str(state_previous_position_ele) + " ---- " + operation_map[move] + " ---- " + str(state_current_zero_position_ele))
    moving.append(operation_map[move])
    #import pdb
    #pdb.set_trace()
   
    if state_array_ele == final_state:
        print("Found")
        break
   
    # Add possible moves
    allowed_operations = map(lambda x: tuple(map(sum, zip(x, state_current_zero_position_ele))),
                             operations)
    allowed_operations = list(filter(lambda x: x[0] >=0 and x[1] >= 0 and
                                          x[0] < n and x[1] < n and
                                          x != state_previous_position_ele,
                                allowed_operations))
   
    if len(allowed_operations) == 0:
        break
   
    added_from_operation = False
   
    # Set priority for allowed_opertaions
    high_allowed_operations = []
    low_allowed_operations = []
    for i,j in allowed_operations:
        if state_array_ele[i][j] != final_state[i][j]:
            high_allowed_operations.append((i,j))
        else:
            low_allowed_operations.append((i,j))
    allowed_operations = []
    allowed_operations.extend(high_allowed_operations)
    allowed_operations.extend(low_allowed_operations)
   
    #random.shuffle(allowed_operations)
    x,y = state_current_zero_position_ele
    for i, j in allowed_operations:
        temp = state_array_ele[i][j]
        state_array_ele[i][j] = state_array_ele[x][y]
        state_array_ele[x][y] = temp
       
        if to_string(state_array_ele) in visited_states:
            temp = state_array_ele[i][j]
            state_array_ele[i][j] = state_array_ele[x][y]
            state_array_ele[x][y] = temp
            continue
       
        visited_states.append(to_string(state_array_ele))
        state_array.append([row[:] for row in state_array_ele])
        state_heuristics.append(get_heuristic_for_state(state_array_ele))
        state_previous_position.append(state_current_zero_position_ele)
        state_current_zero_position.append((i,j))
        temp = state_array_ele[i][j]
        state_array_ele[i][j] = state_array_ele[x][y]
        state_array_ele[x][y] = temp

done = time.time()
elapsed = done - start
print(f"No. of moves = {moves}")
print(f"Moves are {moving}")
print(f"Time taken to find the solution = {elapsed} seconds")