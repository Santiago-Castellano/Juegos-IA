import  random

def action_random(state):
    list_state = list([list(s) for s in state])
    while True:
        row = random.randint(0,2)
        col = random.randint(0,2)
        if list_state[row][col] == 0:
            return (row,col)

def end_game(state):
    row_one,row_two,row_three = state
    plays = list(set(row_one + row_two + row_three))
    if 0 not in plays:
        return True
    
    main_diagonal = row_one[0] + row_two[1] + row_three[2]
    secondary_diagonal = row_one[2] + row_two[1] + row_three[0]
    
    if abs(main_diagonal) == 3:
        return True

    if abs(secondary_diagonal) == 3:
        return True
    
    for row in (row_one,row_two,row_three):
        if abs(sum(row)) == 3:
            return True
        
    for i in range(3):
        sum_col = row_one[i] + row_two[i] + row_three[i]
        if abs(sum_col) == 3:
            return True
    
    return False


def reverse_state(state,val):
    return get_tuple([[val * val for val in row] for row in state])

def get_tuple(state):
    return tuple([tuple(ns) for ns in state])

def get_list(state):
    return list([list(ns) for ns in state])
