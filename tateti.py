import random
from simpleai.search import SearchProblem, hill_climbing, hill_climbing_random_restarts
import os


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
        result = 0
        pos,board = list(state)
        row_one,row_two,row_three = list(board)
        sum_row = 0
        row = []
        if pos[0] == 0:
            row = row_one.copy()
        elif pos[0] == 1:
            row = row_two.copy()
        else:
            row = row_three.copy()

        row[pos[1]] = 1
        main_diagonal = []
        secondary_diagonal = []

        sum_main_diagonal = 0
        sum_secondary_diagonal = 0

        if pos[0] == pos[1]:
            if pos[0] == 0:
                main_diagonal = 1,row_two[1],row_three[2]
            elif pos[0] == 1:
                main_diagonal = row_one[0],1,row_three[2]
            else:
                main_diagonal = row_one[0],row_two[1],1


        if (pos[0] == 2 and pos[1] == 0) or (pos[0] == 0 and pos[1] == 2) or ((pos[0] == 1 and pos[1] == 1)):
            if pos[0] == 0:
                secondary_diagonal = 1,row_two[1],row_three[1]
            elif pos[0] == 1:
                secondary_diagonal = row_one[2],1,row_three[1]
            else:
                secondary_diagonal = row_one[2],row_two[1],1
        
        sum_secondary_diagonal = sum(secondary_diagonal)
        sum_main_diagonal = sum(main_diagonal)
       
        sum_row = sum(row)
        sum_col = row_one[pos[1]] + row_two[pos[1]] + row_three[pos[1]]
        
        """
            SUMAR UNICAMENTE LOS SCTORES DE L APOS DONDE ESTA JUGANDO Y NO TODOS LAS POSIBILIDADES
        """
        #EVITAR QUE ME GANE
        if sum_row == -1:
            result +=  3 if 0 not in (row) else 0
            
        if sum_col == -1:
            result += 3 if 0 not in (row_one[pos[1]],row_two[pos[1]],row_three[pos[1]]) else 0
    
        if sum_main_diagonal == -1:
            result += 3 if 0 not in (main_diagonal) else 0

        if sum_secondary_diagonal == -1:
            result += 3 if 0 not in (secondary_diagonal) else 0

        #INTENTAR GANAR
        for value in (2,3):
            if sum_row == value:
                result +=  value
                
            if sum_col == value:
                result += value
        
            if sum_main_diagonal == value:
                result += value

            if sum_secondary_diagonal == value:
                result += value
        #GANAR

            
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
        print('--------+--------+--------')
        text=''
        for col in row:
            if col == 1:
                text += '    X   |'
            elif col == 0:
                text += '        |'
            else:
                text += '    O   |'
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

def play_again():
    letter = ''
    while letter not in ('Y','N','y','n'):
        letter = input("Play again: Y/N ")
    return letter in ('Y','y')

def input_random_IA(board):
    while True:
        row = random.randint(0,2)
        col = random.randint(0,2)
        if board[row][col] == 0:
            return (row,col)
        
if __name__ == '__main__':
    play = True
    while play:
        os.system('clear')
        finish = False
        state = (0,0),([0,0,0],[0,0,0],[0,0,0])
        board= None
        print("You play whit O")
        play_player = True
        while not finish:
            if play_player:
                row,col = input_player()
                _,board = state
                board[row][col] = -1
                os.system('clear')
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
        
        play = play_again()

