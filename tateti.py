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

        for value in range(-3,3):
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

def end_game(board):
    row_one,row_two,row_three = board
    total = 0
    for row in (row_one,row_two,row_three):
        total += abs(sum(row))
        if abs(sum(row)) == 3:
            return True, 'IA' if sum(row) > 0 else 'Player'
        
    for i in range(3):
        sum_col = row_one[i] + row_two[i] + row_three[i]
        total += abs(row_one[i]) + abs(row_two[i]) + abs(row_three[i])
        if abs(sum_col) == 3:
            return True, 'IA' if sum_col > 0 else 'Player'

    main_diagonal = row_one[0] + row_two[1] + row_three[2]
    secondary_diagonal = row_one[2] + row_two[1] + row_three[0]
    
    total += abs(row_one[0]) + abs(row_two[1]) + abs(row_three[2]) + abs(row_one[2]) + abs(row_two[1]) + abs(row_three[0])

    if abs(main_diagonal) == 3:
        return True, 'IA' if main_diagonal > 0 else 'Player'

    if abs(secondary_diagonal) == 3:
        return True, 'IA' if secondary_diagonal > 0 else 'Player'
    
    return (False, '') if total != 24 else (True,'tied')

def draw_board(board):
    for row in board:
        print('-----------')
        text=''
        for col in row:
            if col == 1:
                text += 'X--'
            elif col == 0:
                text += ' --'
            else:
                text += 'O--'
        print(text)

def input_player():
    row = -1
    col = -1
    while row not in range(3) or col not in range(3):
        if row not in range(3):
            try:
                row = int(input("Please enter a row (0,1,2): "))
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
        if col not in range(3):
            try:
                col = int(input("Please enter a col (0,1,2): "))
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
    return row,col

def input_random_IA(board):
    while True:
        row = random.randint(0,2)
        col = random.randint(0,2)
        if board[row][col] == 0:
            return (row,col)
        
if __name__ == '__main__':
    finish = False
    state = INITIAL
    board= None
    print("You play whit O")
    while not finish:
        row,col = input_player()
        _,board = state
        board[row][col] = -1
        finish,win = end_game(board)
        if not finish:
            input_IA = input_random_IA(board)
            state = (input_IA),board
            problem = TaTeTiProblem(state)
            result = hill_climbing(problem)
            next_play_IA, board = result.state
            board[next_play_IA[0]][next_play_IA[1]] = 1
            
            draw_board(board)
            finish,win = end_game(board)
    print("El ganador es: "+ win)
    draw_board(board)

    #print("### ESTADO DEL JUEGO###")
    #print("Proxima jugada de la IA: fila: "+str(prox_jugada[0])+" col: " +str(prox_jugada[1]))
    #draw_board(tablero)

