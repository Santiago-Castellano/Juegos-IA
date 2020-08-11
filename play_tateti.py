import random
import os
from tateti import play_IA


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

def input_player(board):
    row = -1
    col = -1
    while (row not in range(3) or col not in range(3)):
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
        if row in range(3) and col in range(3) and board[row][col] != 0:
            print("box locked.  Try again...")
            row = -1
            col = -1
            
    return row,col

def play_again():
    letter = ''
    while letter not in ('Y','N','y','n'):
        letter = input("Play again: Y/N ")
    return letter in ('Y','y')



if __name__ == '__main__':
    play = True
    while play:
        os.system('clear')
        finish = False
        state = (0,0),([0,0,0],[0,0,0],[0,0,0])
        board= [0,0,0],[0,0,0],[0,0,0]
        print("You play whit O")
        play_player = random.randint(0,10) > 5
        while not finish:
            if play_player:
                row,col = input_player(board)
                _,board = state
                board[row][col] = -1
                os.system('clear')
            else:
                next_play_IA, board = play_IA(board)
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
