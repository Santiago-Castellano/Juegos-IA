import  os
import  random
from collections import  defaultdict
from numpy import  argmax,save,load
from IA.TaTeTi.helps import  action_random,end_game, get_list,get_tuple,reverse_state


q_values = defaultdict(float)
GAMMA = 0.9
ALPHA = 0.1
EPSILON = 0.5
EPISODES = 100000000

BOARD = (
    (0,0,0),
    (0,0,0),
    (0,0,0),
)


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


def get_reward(state,action):
    plays = []
    x,y = action
    plays.append(sum(state[x]))
    col = [state[0][y],state[1][y],state[2][y]]
    plays.append(sum(col))

    if x == y:
        main_diagonal = state[0][0],state[1][1],state[2][2]
        plays.append(sum(main_diagonal))

    if (x + y) == 2:
        secondary_diagonal = state[0][2],state[1][1],state[2][0]
        plays.append(sum(secondary_diagonal))

    result=0
    for sum_play in plays:
        if sum_play == -1 or sum_play == 3:
           result +=  6 + sum_play 
        else:
            result += sum_play
    
    return result

def step_state(state,action, value):
    x,y = action
    new_state = get_list(state)
    new_state[x][y] = value

    return get_tuple(new_state),get_reward(reverse_state(new_state,value),action), end_game(new_state)



def train():
    for e in range(EPISODES):
        is_episade_done = False
        actual_state = BOARD
        play_with = 1
        while not is_episade_done:

            selected_action, q_actual_state_action = select_action_and_value(reverse_state(actual_state,play_with))

            new_state, reward, is_episade_done = step_state(actual_state,selected_action,play_with)

            _, q_new_state_best_action = select_best_action_and_value(reverse_state(new_state,play_with))

            new_value = q_actual_state_action + ALPHA * (reward + GAMMA*q_new_state_best_action-q_actual_state_action)

            q_values[(reverse_state(actual_state,play_with),selected_action)]=new_value

            actual_state = new_state
            play_with *= -1
    save('q_lergning.npy',q_values)

def loadFile():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    q_val = load(dir_path+'/q_lergning.npy',allow_pickle=True).item()

    return q_val


def play_IA(state):
    dic = loadFile()
    actions = available_actions(state)
    q_values_state = [dic.get((get_tuple(state),action),0.0) for action in actions]

    best_action = argmax(q_values_state)
    best_q_value = q_values_state[best_action]

    return actions[best_action]

if __name__ == '__main__':
    train()