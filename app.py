import streamlit as st
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
CELL_SIZE = WIDTH // 8

# Piece symbols for better visualization
piece_symbols = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

# Initial chessboard state
board = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
]

# Game variables
current_player = 'w'  # 'w' for white, 'b' for black
selected_square = None

# Function to draw the board
def draw_board(screen, board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    font = pygame.font.SysFont(None, CELL_SIZE)
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            piece = board[row][col]
            if piece != ' ':
                text = font.render(piece_symbols[piece], True, pygame.Color("black"))
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4))

# Function to handle user input
def handle_click(pos):
    global selected_square, current_player
    col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if selected_square:
        target_square = (row, col)
        if is_valid_move(board, selected_square, target_square, current_player):
            make_move(board, selected_square, target_square)
            current_player = 'b' if current_player == 'w' else 'w'
        selected_square = None
    else:
        selected_square = (row, col)

# Function to check valid move (simplified)
def is_valid_move(board, source, target, current_player):
    row_source, col_source = source
    row_target, col_target = target
    piece = board[row_source][col_source]

    # Check if target square is empty or contains opponent's piece
    if (board[row_target][col_target] == ' ' or
        board[row_target][col_target].islower() != piece.islower()):

        # Pawn moves (considering first move for pawns)
        if piece == 'P' and current_player == 'w':
            if row_target - row_source == -1 and col_target == col_source:
                return True
            elif row_target - row_source == -2 and row_source == 6 and col_target == col_source and board[row_source - 1][col_source] == ' ':
                return True
            elif row_target - row_source == -1 and abs(col_target - col_source) == 1 and board[row_target][col_target].islower():
                return True

        elif piece == 'p' and current_player == 'b':
            if row_target - row_source == 1 and col_target == col_source:
                return True
            elif row_target - row_source == 2 and row_source == 1 and col_target == col_source and board[row_source + 1][col_source] == ' ':
                return True
            elif row_target - row_source == 1 and abs(col_target - col_source) == 1 and board[row_target][col_target].isupper():
                return True

        # Rook moves (excluding castling for simplicity)
        elif piece in ['R', 'r']:
            if row_source == row_target:
                for col in range(min(col_source, col_target) + 1, max(col_source, col_target)):
                    if board[row_source][col] != ' ':
                        return False
                return True
            elif col_source == col_target:
                for row in range(min(row_source, row_target) + 1, max(row_source, row_target)):
                    if board[row][col_source] != ' ':
                        return False
                return True

        # Bishop moves
        elif piece in ['B', 'b']:
            if abs(row_target - row_source) == abs(col_target - col_source):
                row_step = 1 if row_target > row_source else -1
                col_step = 1 if col_target > col_source else -1
                for i in range(1, abs(row_target - row_source)):
                    if board[row_source + i * row_step][col_source + i * col_step] != ' ':
                        return False
                return True

        # Queen moves (combining bishop and rook moves)
        elif piece in ['Q', 'q']:
            if row_source == row_target:
                for col in range(min(col_source, col_target) + 1, max(col_source, col_target)):
                    if board[row_source][col] != ' ':
                        return False
                return True
            elif col_source == col_target:
                for row in range(min(row_source, row_target) + 1, max(row_source, row_target)):
                    if board[row][col_source] != ' ':
                        return False
                return True
            elif abs(row_target - row_source) == abs(col_target - col_source):
                row_step = 1 if row_target > row_source else -1
                col_step = 1 if col_target > col_source else -1
                for i in range(1, abs(row_target - row_source)):
                    if board[row_source + i * row_step][col_source + i * col_step] != ' ':
                        return False
                return True

        # Knight moves
        elif piece in ['N', 'n']:
            if (abs(row_target - row_source) == 2 and abs(col_target - col_source) == 1) or \
               (abs(row_target - row_source) == 1 and abs(col_target - col_source) == 2):
                return True

        # King moves (excluding castling for simplicity)
        elif piece in ['K', 'k']:
            if abs(row_target - row_source) <= 1 and abs(col_target - col_source) <= 1:
                return True

    return False

# Function to make a move
def make_move(board, source, target):
    row_source, col_source = source
    row_target, col_target = target
    board[row_target][col_target] = board[row_source][col_source]
    board[row_source][col_source] = ' '  # Empty source square

# Streamlit app
st.title("Chess Game")

if st.button("Reset Game"):
    st.session_state['board'] = np.copy(board)
    st.session_state['current_player'] = 'w'
    st.session_state['selected_square'] = None

if 'board' not in st.session_state:
    st.session_state['board'] = np.copy(board)
    st.session_state['current_player'] = 'w'
    st.session_state['selected_square'] = None

clicked = None

# Handle user input via Streamlit
for row in range(8):
    cols = st.columns(8)
    for col in range(8):
        piece = st.session_state['board'][row][col]
        if cols[col].button(piece_symbols.get(piece, ' '), key=f"{row}-{col}"):
            clicked = (row, col)

if clicked:
    handle_click(clicked)

# Draw the board using Pygame and display it in Streamlit
draw_board(screen, st.session_state['board'])

# Convert the Pygame surface to an image format for Streamlit
board_image = pygame.surfarray.array3d(screen)
board_image = np.transpose(board_image, (1, 0, 2))
st.image(board_image)
