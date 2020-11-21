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


queue_array = deque([initial_state])
queue_previous_position = deque([initial_zero_position])
queue_current_zero_position = deque([initial_zero_position])

visited_states = []
to_string = lambda y : (",".join([",".join(map(str,x)) for x in y]))
visited_states.append(to_string(initial_state))

operation_map = {(0,1):"right", (1,0):"down", (0,-1):"left", (-1, 0):"up", (0,0):"start"}

import random
operations = [(0,1), (1,0), (0, -1), (-1, 0)]
while len(queue_array) > 0:
    queue_array_ele = queue_array.popleft()
    queue_previous_position_ele = queue_previous_position.popleft()
    queue_current_zero_position_ele = queue_current_zero_position.popleft()
   
    import numpy
    move = tuple(numpy.subtract(queue_current_zero_position_ele,queue_previous_position_ele))
    moves = moves + 1
    print(str(queue_array_ele) + "    " + str(queue_previous_position_ele) + " ---- " + operation_map[move] + " ---- " + str(queue_current_zero_position_ele))
    moving.append(operation_map[move])
       
    if queue_array_ele == final_state:
        print("Found")
        break
   
    # Add possible moves
    allowed_operations = map(lambda x: tuple(map(sum, zip(x, queue_current_zero_position_ele))),
                             operations)
    allowed_operations = list(filter(lambda x: x[0] >=0 and x[1] >= 0 and
                                          x[0] < n and x[1] < n and
                                          x != queue_previous_position_ele,
                                allowed_operations))
   
    if len(allowed_operations) == 0:
        break
   
    added_from_operation = False
   
    # Set priority for allowed_opertaions
    high_allowed_operations = []
    low_allowed_operations = []
    for i,j in allowed_operations:
        if queue_array_ele[i][j] != final_state[i][j]:
            high_allowed_operations.append((i,j))
        else:
            low_allowed_operations.append((i,j))
    allowed_operations = []
    allowed_operations.extend(high_allowed_operations)
    allowed_operations.extend(low_allowed_operations)
   
    x,y = queue_current_zero_position_ele
    for i, j in allowed_operations:
        temp = queue_array_ele[i][j]
        queue_array_ele[i][j] = queue_array_ele[x][y]
        queue_array_ele[x][y] = temp
       
        if to_string(queue_array_ele) in visited_states:
            temp = queue_array_ele[i][j]
            queue_array_ele[i][j] = queue_array_ele[x][y]
            queue_array_ele[x][y] = temp
            continue
       
        queue_array.append([row[:] for row in queue_array_ele])
        visited_states.append(to_string(queue_array_ele))
        queue_previous_position.append(queue_current_zero_position_ele)
        queue_current_zero_position.append((i,j))
        temp = queue_array_ele[i][j]
        queue_array_ele[i][j] = queue_array_ele[x][y]
        queue_array_ele[x][y] = temp

done = time.time()
elapsed = done - start
print(f"No. of moves = {moves}")
print(f"Moves are {moving}")
print(f"Time taken to find the solution = {elapsed} seconds")