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


stack_array = deque([initial_state])
stack_previous_position = deque([initial_zero_position])
stack_current_zero_position = deque([initial_zero_position])

visited_states = []
to_string = lambda y : (",".join([",".join(map(str,x)) for x in y]))
visited_states.append(to_string(initial_state))

operation_map = {(0,1):"right", (1,0):"down", (0,-1):"left", (-1, 0):"up", (0,0):"start"}

import random
operations = [(0,1), (1,0), (0, -1), (-1, 0)]
while len(stack_array) > 0:
    stack_array_ele = stack_array.pop()
    stack_previous_position_ele = stack_previous_position.pop()
    stack_current_zero_position_ele = stack_current_zero_position.pop()

    import numpy
    move = tuple(numpy.subtract(stack_current_zero_position_ele,stack_previous_position_ele))
    moves = moves + 1
    print(str(stack_array_ele) + "    " + str(stack_previous_position_ele) + " ---- " + operation_map[move] + " ---- " + str(stack_current_zero_position_ele))
    moving.append(operation_map[move])
       
    if stack_array_ele == final_state:
        print("Found")
        break
   
    # Add possible moves
    allowed_operations = map(lambda x: tuple(map(sum, zip(x, stack_current_zero_position_ele))),
                             operations)
    allowed_operations = list(filter(lambda x: x[0] >=0 and x[1] >= 0 and
                                          x[0] < n and x[1] < n and
                                          x != stack_previous_position_ele,
                                allowed_operations))
   
    if len(allowed_operations) == 0:
        break
   
    stack_array.append([row[:] for row in stack_array_ele])
    stack_previous_position.append(stack_previous_position_ele)
    stack_current_zero_position.append(stack_current_zero_position_ele)
   
    added_from_operation = False
   
    # Set priority for allowed_opertaions
    high_allowed_operations = []
    low_allowed_operations = []
    for i,j in allowed_operations:
        if stack_array_ele[i][j] != final_state[i][j]:
            high_allowed_operations.append((i,j))
        else:
            low_allowed_operations.append((i,j))
    allowed_operations = []
    allowed_operations.extend(high_allowed_operations)
    allowed_operations.extend(low_allowed_operations)
   
    x,y = stack_current_zero_position_ele
    for i, j in allowed_operations:
        temp = stack_array_ele[i][j]
        stack_array_ele[i][j] = stack_array_ele[x][y]
        stack_array_ele[x][y] = temp
       
        if to_string(stack_array_ele) in visited_states:
            temp = stack_array_ele[i][j]
            stack_array_ele[i][j] = stack_array_ele[x][y]
            stack_array_ele[x][y] = temp
            continue
       
        added_from_operation = True
        stack_array.append([row[:] for row in stack_array_ele])
        visited_states.append(to_string(stack_array_ele))
        stack_previous_position.append(stack_current_zero_position_ele)
        stack_current_zero_position.append((i,j))
        break
   
    if not added_from_operation:
        stack_array_ele = stack_array.pop()
        stack_previous_position_ele = stack_previous_position.pop()
        stack_current_zero_position_ele = stack_current_zero_position.pop()

done = time.time()
elapsed = done - start
print(f"No. of moves = {moves}")
print(f"Moves are {moving}")
print(f"Time taken to find the solution = {elapsed} seconds")