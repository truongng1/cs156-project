#! /usr/bin/Team1_Connect_4_Agent.py 

# IMPORTS
import random
import math

# DEFINITIONS
#board = [[' ' for _ in range(cols)] for _ in range(rows)]


# HELPER FUNCTIONS
# Print the Board
def print_board(board):
    """ Prints the connect 4 game board."""
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (len(board[0]) * 2 + 1))
    print(' ' + ' '.join(str(i+1) for i in range(len(board[0]))))
    return



# FUNCTIONS REQUIRED BY THE connect_4_main.py MODULE
def init_agent(player_symbol, board_num_rows, board_num_cols, board):
   """ Inits the agent. Should only need to be called once at the start of a game.
   NOTE NOTE NOTE: Do not expect the values you might save in variables to retain
   their values each time a function in this module is called. Therefore, you might
   want to save the variables to a file and re-read them when each function was called.
   This is not to say you should do that. Rather, just letting you know about the variables
   you might use in this module.
   NOTE NOTE NOTE NOTE: All functions called by connect_4_main.py  module will pass in all
   of the variables that you likely will need. So you can probably skip the 'NOTE NOTE NOTE'
   above. """
   global num_rows, num_cols, my_game_symbol, opponent_piece
   my_game_symbol = player_symbol
   opponent_piece = 'X' if my_game_symbol == 'O' else 'O'
   num_rows = int(board_num_rows)
   num_cols = int(board_num_cols)
   #game_board = board
   
   return True

#Check if the location is valid
def is_valid_location(board, col):
    return board[0][col] == ' '

def get_valid_locations(board):
    return [c for c in range(num_cols) if is_valid_location(board, c)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for r in reversed(range(num_rows)):
        if board[r][col] == ' ':
            return r
    return -1

#Check if the move is winning
def winning_move(board, piece):
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(num_cols - 3):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(num_cols - 3):
        for r in range(3, num_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False
# Score machanism (Rule-based evaluation)
def score_window(window, piece):
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(' ') == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(' ') == 2:
        score += 5
    if window.count(opponent_piece) == 3 and window.count(' ') == 1:
        score -= 80
    return score

def score_position(board, piece):
    score = 0
    # Rule: prioritize center
    center_col = [board[r][num_cols//2] for r in range(num_rows)]
    score += center_col.count(piece) * 3

    # Rule: horizontal
    for r in range(num_rows):
        row_array = [board[r][c] for c in range(num_cols)]
        for c in range(num_cols - 3):
            window = row_array[c:c+4]
            score += score_window(window, piece)

    # Rule: vertical
    for c in range(num_cols):
        col_array = [board[r][c] for r in range(num_rows)]
        for r in range(num_rows - 3):
            window = col_array[r:r+4]
            score += score_window(window, piece)

    # Rule: diagonal
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += score_window(window, piece)
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += score_window(window, piece)
    return score

# Minimax with Alpha Beta
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = winning_move(board, my_piece) or winning_move(board, opponent_piece) or len(valid_locations) == 0

    if depth == 0 or is_terminal:
        if winning_move(board, my_piece):
            return (None, 1_000_000)
        elif winning_move(board, opponent_piece):
            return (None, -1_000_000)
        else:
            return (None, score_position(board, my_piece))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [r.copy() for r in board]
            drop_piece(temp_board, row, col, my_piece)
            _, new_score = minimax(temp_board, depth-1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [r.copy() for r in board]
            drop_piece(temp_board, row, col, opponent_piece)
            _, new_score = minimax(temp_board, depth-1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
   """ Decide your move, i.e., which column to drop a disk. """

   # Insert your agent code HERE to decide which column to drop/insert your disk.
   global num_rows, num_cols, my_piece, opponent_piece
   num_rows = game_rows
   num_cols = game_cols
   my_piece = my_game_symbol
   opponent_piece = 'X' if my_piece == 'O' else 'O'
   valid_locations = get_valid_locations(board)
   if len(valid_locations) == 0:
        return random.randint(1, num_cols)

   best_col, _ = minimax(board, 4, -math.inf, math.inf, True)
   if best_col is None or not is_valid_location(board, best_col):
        best_col = random.choice(valid_locations)

   return best_col + 1  


#####
# MAKE SURE MODULE IS IMPORTED
if __name__ == "__main__":
   print("Team1_Connect_4_Agent.py  is intended to be imported and not executed.") 
else:
   print("Team1_Connect_4_Agent.py  has been imported.")
