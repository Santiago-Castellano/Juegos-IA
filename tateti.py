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

        result = 0
        main_diagonal = row_one[0] + row_two[1] + row_three[2]
        secondary_diagonal = row_one[2] + row_two[1] + row_three[0]
        
        for value in (-2,2,3):
            if sum(row_one) == value:
                result += 1 if value > 0 else -1
            if sum(row_two) == value:
                result += 1 if value > 0 else -1
            if sum(row_three) == value:
                result += 1 if value > 0 else -1
            
            for i in range(3):
                sum_col = row_one[i] + row_two[i] + row_three[i]
                if sum_col == value:
                    result += 1 if value > 0 else -1
        
            if main_diagonal == value:
                result += 1 if value > 0 else -1

            if secondary_diagonal == value:
                result += 1 if value > 0 else -1
        
        return result

def end_game(board):
    row_one,row_two,row_three = board
    plays = list(set(row_one + row_two + row_three))
    if 0 not in plays:
        return (True,'tied')
    
    main_diagonal = row_one[0] + row_two[1] + row_three[2]
    secondary_diagonal = row_one[2] + row_two[1] + row_three[0]
    
    if abs(main_diagonal) == 3:
        return True, 'IA' if main_diagonal > 0 else 'Player'

    if abs(secondary_diagonal) == 3:
        return True, 'IA' if secondary_diagonal > 0 else 'Player'
    
    for row in (row_one,row_two,row_three):
        if abs(sum(row)) == 3:
            return True, 'IA' if sum(row) > 0 else 'Player'
        
    for i in range(3):
        sum_col = row_one[i] + row_two[i] + row_three[i]
        if abs(sum_col) == 3:
            return True, 'IA' if sum_col > 0 else 'Player'

    
    return False, ''

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
    play_player = True
    while not finish:
        if play_player:
            row,col = input_player()
            _,board = state
            board[row][col] = -1
        else:
            input_IA = input_random_IA(board)
            state = (input_IA),board
            problem = TaTeTiProblem(state)
            result = hill_climbing(problem)
            next_play_IA, board = result.state
            print("value state: "+ str(result.value))
            board[next_play_IA[0]][next_play_IA[1]] = 1
            
        finish,win = end_game(board)
        if not play_player:
            draw_board(board)
        play_player = not play_player
    print("")
    if win == 'Player':
        print("You WIN!!!! Congratulations")
    elif win == "IA":
        print("You LOST!!!! Try again...")
    else:
        print('TIED, try again...')

    draw_board(board)
