#! /usr/bin/env python3

import random
import math
import time
import hashlib

# GLOBAL VARIABLES
transposition_table = {}
killer_moves = {}
game_start_time = None
game_end_time = None

# HELPER FUNCTIONS
def print_board(board):
    """ Prints the connect 4 game board."""
    # Representation: Display the current state of game board
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (len(board[0]) * 2 + 1))
    print(' ' + ' '.join(str(i+1) for i in range(len(board[0]))))

def board_to_key(board, maximizingPlayer):
    """ Converts the current board state to a unique key.
    James Jian: 100% implement hashing function to uniquely identify the board state
    """
    key = ''.join(''.join(row) for row in board) + str(maximizingPlayer)
    return hashlib.md5(key.encode()).hexdigest()

def make_move(board, col, piece):
    """ Makes a move on the board by placing piece in selected column.
    Michael Chu: 100% implement the logic to make a move by finding next available row.
    """
    for row in reversed(range(num_rows)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row
    return -1

def undo_move(board, row, col):
    """Undoes last move made on the board 
    Michael Chu: 100% implmemnted to revert move on board by setting the cell to empty
    """
    board[row][col] = ' '

def init_agent(player_symbol, board_num_rows, board_num_cols, board):
    """Initializes the agent with the player's symbol, board dimensions, and board state.
    """
    global num_rows, num_cols, my_game_symbol, opponent_piece, game_start_time
    my_game_symbol = player_symbol
    opponent_piece = 'X' if my_game_symbol == 'O' else 'O'
    num_rows = int(board_num_rows)
    num_cols = int(board_num_cols)
    game_start_time = time.time()
    return True

def is_valid_location(board, col):
    """Checks if column is valid location for move
    Eric Nguyen: 100% implmented to ensure move made only in available column"""
    return board[0][col] == ' '

def get_valid_locations(board):
    """Returns list of valid columns where move can be made
    Amy Do: 100% implmeneted to gather all available columns for a move"""
    return [c for c in range(num_cols) if is_valid_location(board, c)]

def get_ordered_valid_locations(board, depth):
    """ Returns valid columns ordered by potential threats and preferences.
    Eric Nguyen: 50% Implemented to order columns based on winning move potential.
    James Jian: 50% Enhanced with center prioritization and killer move tracking.
    """
    valid_cols = get_valid_locations(board)
    ordered_cols = []
    for col in valid_cols:
        row = make_move(board, col, my_piece)
        if winning_move(board, my_piece):
            undo_move(board, row, col)
            return [col]
        undo_move(board, row, col)
        row = make_move(board, col, opponent_piece)
        if winning_move(board, opponent_piece):
            ordered_cols.append(col)
        undo_move(board, row, col)
    if depth in killer_moves:
        for col in killer_moves[depth]:
            if col in valid_cols and col not in ordered_cols:
                ordered_cols.append(col)
    center = num_cols // 2
    remaining = [c for c in valid_cols if c not in ordered_cols]
    remaining.sort(key=lambda x: abs(x - center))
    ordered_cols.extend(remaining)
    return ordered_cols

def winning_move(board, piece):
    """ Checks if a player has made a winning move.
    Amy Do: 100% Implemented to check horizontal, vertical, and diagonal wins.
    """
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(num_cols - 3):
        for r in range(num_rows - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(num_cols - 3):
        for r in range(3, num_rows):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def score_window(window, piece):
    """ Scores a window of 4 pieces for a potential move.
    Eric Nguyen: 100% Implemented to score the strength of a window of 4 consecutive pieces.
    """
    score = 0
    opp = opponent_piece
    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(' ') == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(' ') == 2:
        score += 10
    if window.count(piece) == 3 and ' ' in window:
        score += 25  # Fork potential
    if window.count(opp) == 3 and window.count(' ') == 1:
        score -= 120
    elif window.count(opp) == 2 and window.count(' ') == 2:
        score -= 15
    return score

def score_position(board, piece):
    """ Scores the entire board for a given piece.
    Amy Do: 100% Implemented to evaluate the overall strength of the board.
    """
    score = 0
    center_col = [board[r][num_cols//2] for r in range(num_rows)]
    score += center_col.count(piece) * 5
    empty_spaces = sum(row.count(' ') for row in board)
    for r in range(num_rows):
        row_array = [board[r][c] for c in range(num_cols)]
        for c in range(num_cols - 3):
            score += score_window(row_array[c:c+4], piece)
    for c in range(num_cols):
        col_array = [board[r][c] for r in range(num_rows)]
        for r in range(num_rows - 3):
            score += score_window(col_array[r:r+4], piece)
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            score += score_window([board[r+i][c+i] for i in range(4)], piece)
            score += score_window([board[r+3-i][c+i] for i in range(4)], piece)
    if empty_spaces < 10:
        score *= 1.2
    return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    """ Minimax algorithm with Alpha-Beta Pruning.
    Eric Nguyen: 50% Implemented the Minimax search algorithm with pruning.
    James Jian: 50% Enhanced with transposition table and killer move heuristic.
    """
    # Main entry to Search method
    # Search is performed by recursively exploring all possible moves and evaluating them
    # using a heuristic score. Alpha-Beta Pruning is used to optimize the search.

    board_key = board_to_key(board, maximizingPlayer)
    valid_locations = get_ordered_valid_locations(board, depth)
    is_terminal = winning_move(board, my_piece) or winning_move(board, opponent_piece) or len(valid_locations) == 0
    if board_key in transposition_table:
        tt_entry = transposition_table[board_key]
        if tt_entry['depth'] == depth:
            if tt_entry['flag'] == 'exact':
                return tt_entry['best_col'], tt_entry['score']
            elif tt_entry['flag'] == 'lower' and tt_entry['score'] >= beta:
                return tt_entry['best_col'], tt_entry['score']
            elif tt_entry['flag'] == 'upper' and tt_entry['score'] <= alpha:
                return tt_entry['best_col'], tt_entry['score']
    if depth == 0 or is_terminal:
        score = score_position(board, my_piece)
        transposition_table[board_key] = {'depth': depth, 'score': score, 'best_col': None, 'flag': 'exact'}
        return None, score
    best_col = None
    if maximizingPlayer:
        value = -math.inf
        for col in valid_locations:
            row = make_move(board, col, my_piece)
            _, new_score = minimax(board, depth-1, alpha, beta, False)
            undo_move(board, row, col)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                killer_moves.setdefault(depth, []).append(col)
                killer_moves[depth] = list(set(killer_moves[depth]))[:3]
                break
        transposition_table[board_key] = {'depth': depth, 'score': value, 'best_col': best_col, 'flag': 'lower' if value >= beta else 'exact'}
        return best_col, value
    else:
        value = math.inf
        for col in valid_locations:
            row = make_move(board, col, opponent_piece)
            _, new_score = minimax(board, depth-1, alpha, beta, True)
            undo_move(board, row, col)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                killer_moves.setdefault(depth, []).append(col)
                killer_moves[depth] = list(set(killer_moves[depth]))[:3]
                break
        transposition_table[board_key] = {'depth': depth, 'score': value, 'best_col': best_col, 'flag': 'upper' if value <= alpha else 'exact'}
        return best_col, value

def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
    """ Main function to determine the best move using Minimax.
    James Jian: 40% Overall design and logic of selecting the best move.
    Eric Nguyen: 30% Implemented Alpha-Beta pruning and optimized the search loop.
    Michael Chu: 30% Enhanced logic for handling game start time and random moves.
    """
    # Main entry to Reasoning method
    # Reasoning here involves choosing the best move based on the Minimax search results.
    global num_rows, num_cols, my_piece, opponent_piece
    num_rows = game_rows
    num_cols = game_cols
    my_piece = my_game_symbol
    opponent_piece = 'X' if my_piece == 'O' else 'O'
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0:
        return random.randint(1, num_cols)
    if all(cell == ' ' for row in board for cell in row):
        # Avoid outer columns (0, 1, 5, 6) for perfect play
        if num_cols == 7:
            return 4  # 1-indexed column 4
    for col in valid_locations:
        row = make_move(board, col, my_piece)
        if winning_move(board, my_piece):
            undo_move(board, row, col)
            return col + 1
        undo_move(board, row, col)
    for col in valid_locations:
        row = make_move(board, col, opponent_piece)
        if winning_move(board, opponent_piece):
            undo_move(board, row, col)
            return col + 1
        undo_move(board, row, col)
    empty_spaces = sum(row.count(' ') for row in board)
    max_time = 5.0 if empty_spaces > 35 else 4.0
    start_time = time.time()
    best_col = random.choice(valid_locations)
    depth = 4
    max_depth = 20
    while depth <= max_depth and time.time() - start_time < max_time:
        col, score = minimax(board, depth, -math.inf, math.inf, True)
        if col is not None:
            best_col = col
        depth += 1
    return best_col + 1

def connect_4_result(board, winner, looser):
    """ Prints the result of the game.
    Michael Chu: 100% Implemented to track the total runtime.
    """
    global game_end_time
    game_end_time = time.time()
    if game_start_time is not None:
        total_time = game_end_time - game_start_time
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        print(f"Total runtime for Team 4: {minutes} min {seconds} sec")
    else:
        print("game_start_time not set properly!")
    print(">>> I am player Team 4 <<<")
    if winner == "Draw":
        print(">>> The game resulted in a draw. <<<\n")
        return True
    if winner == "Team4":
        print("YEAH!!  :-)")
    else:
        print("BOO HOO HOO  :~(")
    return True

if __name__ != "__main__":
    print("Team4_Connect_4_Agent.py has been imported.")
