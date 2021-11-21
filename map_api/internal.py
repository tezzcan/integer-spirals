def prepare_table(x,y):
    table = [[None] * x for j in range(y)] # create a table with x columns and y rows
    directions = [(0,1),(1,0),(0,-1),(-1,0)] # right, down, left, up
    direction_index = 0 # what direction currently we are going

    current_x, current_y = 0,0 # current location in table that we are inserting numbers into

    for i in range(0,y*x):
        table[current_y][current_x] = i
        next_y = current_y + directions[direction_index][0]
        next_x = current_x + directions[direction_index][1]

        if next_y < 0 or next_y >= y or next_x < 0 or next_x >= x or table[next_y][next_x] != None:
            direction_index = (direction_index + 1) % 4

            next_y = current_y + directions[direction_index][0]
            next_x = current_x + directions[direction_index][1]
        
        current_y = next_y
        current_x = next_x
    
    return table