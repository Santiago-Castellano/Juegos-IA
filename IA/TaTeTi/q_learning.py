from collections import  defaultdict   
from numpy import  argmax,save
import  random
from tateti import  play_IA
GAMMA = 0.9
ALPHA = 0.1
EPSILON = 0.5
EPISODES = 4


BOARD = (
    (0,0,0),
    (0,0,0),
    (0,0,0),
)

def action_random(state):
    list_state = list([list(s) for s in state])
    while True:
        row = random.randint(0,2)
        col = random.randint(0,2)
        if list_state[row][col] == 0:
            return (row,col)

def available_actions(state):
    actions = []
    for row_index,row in enumerate(state):
        for  col_index,col in enumerate(row):
            if col == 0:
                actions.append((row_index,col_index))
        
    return actions


def select_random_action_and_value(state):
    random_action = action_random(state)
    q_random_action = q_values.get((state,random_action),0.0)

    return random_action, q_random_action

def select_best_action_and_value(state):
    actions = available_actions(state)
    q_values_state = [q_values.get((state,action),0.0) for action in actions]
    if len(q_values_state) == 0:
        return (), 0
        
    best_action = argmax(q_values_state)
    best_q_value = q_values_state[best_action]
    
    return actions[best_action], best_q_value

def select_action_and_value(state):
    if random.random() < EPSILON:
        action, q_value_action = select_random_action_and_value(state)
    else:
        action, q_value_action = select_best_action_and_value(state)
    
    return action, q_value_action

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

def step_state(state,action):
    x,y = action
    new_state = list([list(s) for s in state])
    new_state[x][y] = 1
    plays = []
    plays.append(sum(new_state[x]))
    col = [new_state[0][y],new_state[1][y],new_state[2][y]]
    plays.append(sum(col))

    if x == y:
        main_diagonal = new_state[0][0],new_state[1][1],new_state[2][2]
        plays.append(sum(main_diagonal))

    if (x + y) == 2:
        secondary_diagonal = new_state[0][2],new_state[1][1],new_state[2][0]
        plays.append(sum(secondary_diagonal))
    
    result=0
    for sum_play in plays:
        if sum_play == 3:
            result =1

    return tuple([tuple(ns) for ns in new_state]),result, end_game(state)


if __name__ == '__main__':
    q_values = defaultdict(float)
    for e in range(EPISODES):
        is_episade_done = False
        actual_state = BOARD
        while not is_episade_done:

            selected_action, q_actual_state_action = select_action_and_value(actual_state)
            
            new_state, reward, is_episade_done = step_state(actual_state,selected_action)
            
            _, q_new_state_best_action = select_best_action_and_value(new_state)
            
            new_value = q_actual_state_action + ALPHA * (reward + GAMMA*q_new_state_best_action-q_actual_state_action)
            
            q_values[(actual_state,selected_action)]=new_value
            
            if not is_episade_done:
                new_x,new_y = action_random(new_state)
                list_new_state = list([list(ns) for ns in new_state])
                list_new_state[new_x][new_y] = -1
                new_state = tuple([tuple(ls) for ls in list_new_state])
                is_episade_done = end_game(new_state)

            actual_state = new_state
    save('q_lergning.npy',q_values)  

