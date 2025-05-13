#!/usr/bin/env python3

# IMPORTS
import random
import math
import time
import hashlib

# GLOBAL VARIABLES
transposition_table = {}
killer_moves = {}  # Store killer moves by depth

# HELPER FUNCTIONS
def print_board(board):
    """ Prints the connect 4 game board."""
    for row in board:
        print('|' + '|'.join(row) + '|')
    print("-" * (len(board[0]) * 2 + 1))
    print(' ' + ' '.join(str(i+1) for i in range(len(board[0]))))
    return

def board_to_key(board):
    """ Convert board to a hashable key for transposition table."""
    return hashlib.md5(str(board).encode()).hexdigest()

# FUNCTIONS REQUIRED BY THE connect_4_main.py MODULE
def init_agent(player_symbol, board_num_rows, board_num_cols, board):
    """ Inits the agent. Should only need to be called once at the start of a game."""
    global num_rows, num_cols, my_game_symbol, opponent_piece
    my_game_symbol = player_symbol
    opponent_piece = 'X' if my_game_symbol == 'O' else 'O'
    num_rows = int(board_num_rows)
    num_cols = int(board_num_cols)
    return True

def is_valid_location(board, col):
    return board[0][col] == ' '

def get_valid_locations(board):
    return [c for c in range(num_cols) if is_valid_location(board, c)]

def get_ordered_valid_locations(board, depth):
    """ Returns valid columns ordered by priority."""
    valid_cols = get_valid_locations(board)
    ordered_cols = []

    # Check for immediate wins or blocks
    for col in valid_cols:
        row = get_next_open_row(board, col)
        if row != -1:
            temp_board = [r.copy() for r in board]
            drop_piece(temp_board, row, col, my_piece)
            if winning_move(temp_board, my_piece):
                return [col]  # Immediate win
            temp_board[row][col] = opponent_piece
            if winning_move(temp_board, opponent_piece):
                ordered_cols.append(col)  # Block opponent win

    # Add killer moves
    if depth in killer_moves:
        for col in killer_moves[depth]:
            if col in valid_cols and col not in ordered_cols:
                ordered_cols.append(col)

    # Add remaining columns, prioritizing center
    center = num_cols // 2
    remaining = [c for c in valid_cols if c not in ordered_cols]
    remaining.sort(key=lambda x: abs(x - center))
    ordered_cols.extend(remaining)

    return ordered_cols

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for r in reversed(range(num_rows)):
        if board[r][col] == ' ':
            return r
    return -1

def winning_move(board, piece):
    # Horizontal
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Vertical
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Positive diagonal
    for c in range(num_cols - 3):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Negative diagonal
    for c in range(num_cols - 3):
        for r in range(3, num_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

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
    center_col = [board[r][num_cols//2] for r in range(num_rows)]
    score += center_col.count(piece) * 3

    for r in range(num_rows):
        row_array = [board[r][c] for c in range(num_cols)]
        for c in range(num_cols - 3):
            window = row_array[c:c+4]
            score += score_window(window, piece)

    for c in range(num_cols):
        col_array = [board[r][c] for r in range(num_rows)]
        for r in range(num_rows - 3):
            window = col_array[r:r+4]
            score += score_window(window, piece)

    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += score_window(window, piece)
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += score_window(window, piece)
    return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    board_key = board_to_key(board)
    valid_locations = get_ordered_valid_locations(board, depth)
    is_terminal = winning_move(board, my_piece) or winning_move(board, opponent_piece) or len(valid_locations) == 0

    # Check transposition table
    if board_key in transposition_table:
        tt_entry = transposition_table[board_key]
        if tt_entry['depth'] >= depth:
            if tt_entry['flag'] == 'exact':
                return tt_entry['best_col'], tt_entry['score']
            elif tt_entry['flag'] == 'lower' and tt_entry['score'] >= beta:
                return tt_entry['best_col'], tt_entry['score']
            elif tt_entry['flag'] == 'upper' and tt_entry['score'] <= alpha:
                return tt_entry['best_col'], tt_entry['score']

    if depth == 0 or is_terminal:
        if winning_move(board, my_piece):
            score = 1_000_000 - depth
            flag = 'exact'
        elif winning_move(board, opponent_piece):
            score = -1_000_000 + depth
            flag = 'exact'
        else:
            score = score_position(board, my_piece)
            flag = 'exact'
        transposition_table[board_key] = {'depth': depth, 'score': score, 'best_col': None, 'flag': flag}
        return None, score

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations) if valid_locations else None
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
                # Store killer move
                if depth not in killer_moves:
                    killer_moves[depth] = []
                if col not in killer_moves[depth]:
                    killer_moves[depth].append(col)
                break
        flag = 'exact' if value < beta else 'lower'
        transposition_table[board_key] = {'depth': depth, 'score': value, 'best_col': best_col, 'flag': flag}
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations) if valid_locations else None
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
                if depth not in killer_moves:
                    killer_moves[depth] = []
                if col not in killer_moves[depth]:
                    killer_moves[depth].append(col)
                break
        flag = 'exact' if value > alpha else 'upper'
        transposition_table[board_key] = {'depth': depth, 'score': value, 'best_col': best_col, 'flag': flag}
        return best_col, value

def what_is_your_move(board, game_rows, game_cols, my_game_symbol):
    """ Decide your move, i.e., which column to drop a disk."""
    global num_rows, num_cols, my_piece, opponent_piece
    num_rows = game_rows
    num_cols = game_cols
    my_piece = my_game_symbol
    opponent_piece = 'X' if my_piece == 'O' else 'O'
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0:
        return random.randint(1, num_cols)

    # Iterative deepening
    max_time = 2.0  # seconds
    start_time = time.time()
    best_col = random.choice(valid_locations)
    max_depth = 20  # Maximum depth to prevent infinite loops
    depth = 1

    while depth <= max_depth and time.time() - start_time < max_time:
        col, score = minimax(board, depth, -math.inf, math.inf, True)
        if col is not None:
            best_col = col
        depth += 1

    if best_col is None or not is_valid_location(board, best_col):
        best_col = random.choice(valid_locations)

    return best_col + 1

def connect_4_result(board, winner, looser):
    """The Connect 4 manager calls this function when the game is over."""
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
    return True

#####
# MAKE SURE MODULE IS IMPORTED
if __name__ == "__main__":
    print("Team1_Connect_4_Agent.py is intended to be imported and not executed.")
else:
    print("Team1_Connect_4_Agent.py has been imported.")