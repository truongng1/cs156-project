import numpy as np
import pygame
import sys
import math
import time
pygame.font.init()


ROW_COUNT = 6
COL_COUNT = 7
height = (ROW_COUNT +1) * 100
width = COL_COUNT * 100
radius = 45

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")

def create_board():
    board = np.zeros((6,7))
    return board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location (board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for r in range (ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    # print the board upside down as connect 4 is played from bottom to top
    print(np.flip(board, 0)) 

def winning_condition(board, piece): 
    # Check all horizontal locations for win
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Check all vertical location for win
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Check all diagonal location from the left to right for win
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Check all diagonal location from the right to left for win
    for r in range(3, ROW_COUNT):
        for c in range(COL_COUNT - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def draw_board(board, winner=None):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(screen, (0,0,255), (c*100,r*100+100,100,100))
            pygame.draw.circle(screen, (0,0,0), (int(c*100+50),int(r*100+50+100)), radius)
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (255,0,0), (int(c*100+50),height-int(r*100+50)), radius) # RED
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (255,255,0), (int(c*100+50),height-int(r*100+50)), radius) # YELLOW
    
    # Display winner if game is over
    if winner:
        font = pygame.font.Font(None, 74)
        text = font.render(f'Player {winner} Wins!', True, (255,255,255))
        text_rect = text.get_rect(center=(width/2, 50))
        screen.blit(text, text_rect)
    
    pygame.display.update()


board = create_board()
draw_board(board)
game_over = False
turn = 0


# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            # RED and YELLOW circle motion on top
            pygame.draw.rect(screen, (0,0,0), (0,0, width, 100))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, (255,0,0), (posx, int(100/2)), radius)
            else:
                pygame.draw.circle(screen, (255,255,0), (posx, int(100/2)), radius)
            pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0,0,0), (0,0, width, 100)) # Clear the top row
            # Player 1 turn
            if turn == 0:
                posx = event.pos[0]
                selection = int(math.floor(posx/100))
                if is_valid_location(board, selection):
                     row = get_next_open_row(board, selection)
                     drop_piece(board, row, selection, 1)
                     if winning_condition(board, 1):
                         print("Player 1 wins!")
                         game_over = True
                         draw_board(board, winner=1)
                     else:
                         draw_board(board)
                         print_board(board)
            # Player 2 turn
            else:
                posx = event.pos[0]
                selection = int(math.floor(posx/100))

                if is_valid_location(board, selection):
                     row = get_next_open_row(board, selection)
                     drop_piece(board, row, selection, 2)
                     if winning_condition(board, 2):
                         print("Player 2 wins!")
                         game_over = True
                         draw_board(board, winner=2)
                     else:
                         draw_board(board)
                         print_board(board)
            turn += 1
            turn = turn % 2
            
        draw_board(board)
       
        if game_over:
            pygame.time.wait(3000)  # Wait for 3 seconds before closing
            pygame.quit()
            sys.exit()
