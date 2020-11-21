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

done = False
minimum_heuristics = get_heuristic_for_state(initial_state)
next_minimum_heuristics = minimum_heuristics
operation_map = {(0,1):"right", (1,0):"down", (0,-1):"left", (-1, 0):"up", (0,0):"start"}
while 1 > 0:
    minimum_heuristics = next_minimum_heuristics
    next_minimum_heuristics = -1
    stack_array = deque([initial_state])
    stack_heuristics = deque([get_heuristic_for_state(initial_state)])
    stack_previous_position = deque([initial_zero_position])
    stack_current_zero_position = deque([initial_zero_position])

    visited_states = []
    to_string = lambda y : (",".join([",".join(map(str,x)) for x in y]))
    visited_states.append(to_string(initial_state))

    operations = [(0,1), (1,0), (0, -1), (-1, 0)]
    while len(stack_array) > 0:
        stack_array_ele = stack_array.pop()
        stack_heuristics_ele = stack_heuristics.pop()
        stack_previous_position_ele = stack_previous_position.pop()
        stack_current_zero_position_ele = stack_current_zero_position.pop()
       
        if stack_heuristics_ele > minimum_heuristics:
            if next_minimum_heuristics == -1:
                next_minimum_heuristics = stack_heuristics_ele
            elif next_minimum_heuristics > stack_heuristics_ele:
                next_minimum_heuristics = stack_heuristics_ele
            continue
       
        import numpy
        move = tuple(numpy.subtract(stack_current_zero_position_ele,stack_previous_position_ele))
        moves = moves + 1
        print(str(stack_array_ele) + "    " + str(stack_previous_position_ele) + " ---- " + operation_map[move] + " ---- " + str(stack_current_zero_position_ele))
        moving.append(operation_map[move])
        #import pdb
        #pdb.set_trace()
   
        if stack_array_ele == final_state:
            print("Found")
            print(f"No. of moves = {moves}")
            done = True
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
        stack_heuristics.append(get_heuristic_for_state(stack_array_ele))
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
   
        #random.shuffle(allowed_operations)
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
            stack_heuristics.append(get_heuristic_for_state(stack_array_ele))
            visited_states.append(to_string(stack_array_ele))
            stack_previous_position.append(stack_current_zero_position_ele)
            stack_current_zero_position.append((i,j))
            break
   
        if not added_from_operation:
            stack_array_ele = stack_array.pop()
            stack_heuristics_ele = stack_heuristics.pop()
            stack_previous_position_ele = stack_previous_position.pop()
            stack_current_zero_position_ele = stack_current_zero_position.pop()
           
    if done:
        break

done = time.time()
elapsed = done - start
print(f"Moves are {moving}")
print(f"Time taken to find the solution = {elapsed} seconds")