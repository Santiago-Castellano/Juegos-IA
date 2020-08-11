import random
from simpleai.search import SearchProblem, hill_climbing
import os


class TaTeTiProblem(SearchProblem):
    def actions(self, state):
        available_actions = []
        _,board = state
        for row_index,row in enumerate(board):
            for  col_index,col in enumerate(row):
                if col == 0:
                    available_actions.append((row_index,col_index))
        
        return available_actions

    def result(self, state, action):
        row,col = action
        _,board = state
        new_state = (row,col),board
        
        return new_state

    def value(self, state):
        result = 0
        (x,y),board_state = list(state)
        board = [[0] * 3] * 3
        for row_index, row in enumerate(board_state):
            board[row_index] = list(row).copy()

        board[x][y] = 1
        plays = []
        #add row
        plays.append((sum(board[x].copy()),board[x].copy()))
        #add col
        col = [board[0][y],board[1][y],board[2][y]]
        plays.append((sum(col),col))

        if x == y:
            main_diagonal = board[0][0],board[1][1],board[2][2]
            plays.append((sum(main_diagonal),main_diagonal))

        if (x + y) == 2:
            secondary_diagonal = board[0][2],board[1][1],board[2][0]
            plays.append((sum(secondary_diagonal),secondary_diagonal))
        
        for sum_play, play in plays:
            if sum_play == -1:
                result +=  3 if 0 not in (play) else 0
            else:
                for value in (2,3):
                    if sum_play == value:
                        result +=  value

        return result


def input_random_IA(board):
    while True:
        row = random.randint(0,2)
        col = random.randint(0,2)
        if board[row][col] == 0:
            return (row,col)

def play_IA(board):
    input_IA = input_random_IA(board)
    state = (input_IA),board
    problem = TaTeTiProblem(state)
    result = hill_climbing(problem)
    next_play_IA, board = result.state
    
    return next_play_IA,board

if __name__ == '__main__':
    pass
