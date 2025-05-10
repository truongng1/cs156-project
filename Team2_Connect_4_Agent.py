#! /usr/bin/Team2_Connect_4_Agent.py 

# IMPORTS
import random

# DEFINITIONS
# board = [[' ' for _ in range(cols)] for _ in range(rows)]

# HELPER FUNCTIONS
# Print the Board
def print_board(board):
    """ Prints the connect 4 game board."""
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (len(board[0]) * 2 + 1))
    print(' ' + ' '.join(str(i+1) for i in range(len(board[0]))))

# Check if the game is game is over by a team winning or draw - Reasoning
def game_over(board):

    if check_win(board, my_game_symbol):
        return my_game_symbol
    if check_win(board, opponent_symbol):
        return opponent_symbol
    

    for col in range(num_cols):
        if board[0][col] == ' ':
            return False  # Game is not over
    return 'Draw'

# Check if a player has won - Reasoning
def check_win(board, symbol):
    # Check all directions to see if symbol has 4 in a row
    for row in range(num_rows):
        for col in range(num_cols):
            if board[row][col] == symbol:
                if col + 3 < num_cols and all(board[row][col + i] == symbol for i in range(4)):
                    return True
            
                if row + 3 < num_rows and all(board[row + i][col] == symbol for i in range(4)):
                    return True
            
                if row + 3 < num_rows and col + 3 < num_cols and all(board[row + i][col + i] == symbol for i in range(4)):
                    return True
                
                if row - 3 >= 0 and col + 3 < num_cols and all(board[row - i][col + i] == symbol for i in range(4)):
                    return True
    return False

# Hueristic Evaluation Function which returns a score to show if the board is good for the player or not. - Reasoning
def evaluate(board):
    if check_win(board, my_game_symbol):
        return 100  
    if check_win(board, opponent_symbol):
        return -100  
    
    # Huerstic function calculated by counting number of 2-in-a-row and 3-in-a-row opportunities for the player and opponent.
    score = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if board[row][col] == my_game_symbol:
                score += count_opportunities(board, row, col, my_game_symbol)

            if board[row][col] == opponent_symbol:
                score -= count_opportunities(board, row, col, opponent_symbol)
    return score

def count_opportunities(board, row, col, symbol):
    opportunities = 0
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)] 
    for dr, dc in directions:
        count = 0
        for i in range(1, 4):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == symbol:
                count += 1
            else:
                break
        if count >= 2:
            opportunities += count
    return opportunities

# Minimax Search Algorithm - Search
def minimax(board, depth, is_maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate(board)

    if is_maximizing_player:
        max_eval = -float('inf')
        for col in range(num_cols):
            if valid_move(board, col):
                make_move(board, col, my_game_symbol)
                eval = minimax(board, depth-1, False)
                undo_move(board, col)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(num_cols):
            if valid_move(board, col):
                make_move(board, col, opponent_symbol)
                eval = minimax(board, depth-1, True)
                undo_move(board, col)
                min_eval = min(min_eval, eval)
        return min_eval


def valid_move(board, col):
    return board[0][col] == ' '


def make_move(board, col, symbol):
    for row in range(num_rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            break


def undo_move(board, col):
    for row in range(num_rows):
        if board[row][col] != ' ':
            board[row][col] = ' '
            break

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
    global num_rows, num_cols, game_board, my_game_symbol, opponent_symbol
    num_rows = int(board_num_rows)
    num_cols = int(board_num_cols)
    game_board = board
    my_game_symbol = player_symbol
    opponent_symbol = 'O' if my_game_symbol == 'X' else 'X'
    return True


def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
    """ Decide your move, i.e., which column to drop a disk."""
    best_move = None
    best_value = -float('inf')

    for col in range(game_cols):
        if valid_move(board, col):
            make_move(board, col, my_game_symbol)
            move_value = minimax(board, 4, False)  
            undo_move(board, col)

            if move_value > best_value:
                best_value = move_value
                best_move = col

    return best_move + 1  



def connect_4_result(board, winner, looser):
    """The Connect 4 manager calls this function when the game is over.
    If there is a winner, the team name of the winner and looser are the
    values of the respective argument variables. If there is a draw/tie,
    the values of winner = looser = 'Draw'."""

    # Check if a draw
    if winner == "Draw":
        print(">>> I am player TEAM2 <<<")
        print(">>> The game resulted in a draw. <<<\n")
        return True

    print(">>> I am player TEAM2 <<<")
    print("The winner is " + winner)
    if winner == "Team2":
        print("YEAH!!  :-)")
    else:
        print("BOO HOO HOO  :~(")
    print("The looser is " + looser)
    print()

    # print("The final board is")   # Uncomment if you want to print the game board.
    # print(board)  # Uncomment if you want to print the game board.

    # Insert your code HERE to do whatever you like with the arguments.

    return True


#####
# MAKE SURE MODULE IS IMPORTED
if __name__ == "__main__":
   print("Team2_Connect_4_Agent.py  is intended to be imported and not executed.") 
else:
   print("Team2_Connect_4_Agent.py  has been imported.")
