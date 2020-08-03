import random
from simpleai.search import SearchProblem, hill_climbing, hill_climbing_random_restarts


INITIAL = (0,0),([0,0,0],[0,0,0],[0,0,0])

class TaTeTiProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        pos,board = state
        for row_index,row in enumerate(board):
            for  col_index,col in enumerate(row):
                if col == 0:
                    if row_index != pos[0] and col_index != pos[1]:
                        available_actions.append((row_index,col_index))
        
        return available_actions

    def result(self, state, action):
        row,col = action
        _,board = state
        new_state = (row,col),board
        
        return new_state

    def value(self, state):
        pos,board = list(state)
        row_one,row_two,row_three = board
        row_one = row_one.copy()
        row_two = row_two.copy()
        row_three = row_three.copy()
        if pos[0] == 0:
            row_one[pos[1]] = 1
        if pos[0] == 1:
            row_two[pos[1]] = 1
        if pos[0] == 2:
            row_three[pos[1]] = 1

        for value in range(-2,2):
            if sum(row_one) == value or sum(row_two) == value or sum(row_three) == value:
                return value
            
            for i in range(3):
                sum_col = row_one[i] + row_two[i] + row_three[i]
                if sum_col == value:
                    return value

            main_diagonal = row_one[0] + row_two[1] + row_three[2]
            secondary_diagonal = row_one[2] + row_two[1] + row_three[0]
            
            if main_diagonal == value:
                return value

            if secondary_diagonal == value:
                return value

    def generate_random_state(self):
        pass

if __name__ == '__main__':
    problem = TaTeTiProblem(INITIAL)
    result = hill_climbing(problem)
    prox_jugada, tablero = result.state

    print("### ESTADO DEL JUEGO###")
    print("Proxima jugada de la IA: fila: "+str(prox_jugada[0])+" col: " +str(prox_jugada[1]))
    print(tablero)
    print('Score: ', -problem.value(result.state))