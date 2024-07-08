# chess_logic.py

import pygame
import numpy as np
import asyncio
import websockets

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

# Initialize Pygame
pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))

# Function to draw the board
def draw_board():
    global screen
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

# Function to handle move validation
def is_valid_move(source, target):
    global board, current_player
    row_source, col_source = source
    row_target, col_target = target
    piece = board[row_source][col_source]

    # Function to handle move validation
def is_valid_move(source, target):
    global board, current_player
    row_source, col_source = source
    row_target, col_target = target
    piece = board[row_source][col_source]

    # Check if the source and target are within board bounds
    if not (0 <= row_source < 8 and 0 <= col_source < 8 and 0 <= row_target < 8 and 0 <= col_target < 8):
        return False

    # Check if the source and target are not the same
    if source == target:
        return False

    # Check if the piece at source belongs to the current player
    if piece.isupper() and current_player != 'w':
        return False
    if piece.islower() and current_player != 'b':
        return False

    # Pawn moves
    if piece == 'P':  # White pawn
        if col_source == col_target and row_target == row_source - 1 and board[row_target][col_target] == ' ':  # Single move forward
            return True
        elif col_source == col_target and row_target == row_source - 2 and row_source == 6 and board[row_source - 1][col_target] == ' ' and board[row_target][col_target] == ' ':  # Double move from starting position
            return True
        elif abs(col_source - col_target) == 1 and row_target == row_source - 1 and board[row_target][col_target].islower():  # Capture diagonally
            return True

    elif piece == 'p':  # Black pawn
        if col_source == col_target and row_target == row_source + 1 and board[row_target][col_target] == ' ':  # Single move forward
            return True
        elif col_source == col_target and row_target == row_source + 2 and row_source == 1 and board[row_source + 1][col_target] == ' ' and board[row_target][col_target] == ' ':  # Double move from starting position
            return True
        elif abs(col_source - col_target) == 1 and row_target == row_source + 1 and board[row_target][col_target].isupper():  # Capture diagonally
            return True

    # Rook moves
    elif piece in ['R', 'r']:
        if row_source == row_target:  # Horizontal move
            for col in range(min(col_source, col_target) + 1, max(col_source, col_target)):
                if board[row_source][col] != ' ':
                    return False
            return True
        elif col_source == col_target:  # Vertical move
            for row in range(min(row_source, row_target) + 1, max(row_source, row_target)):
                if board[row][col_source] != ' ':
                    return False
            return True

    # Knight moves
    elif piece in ['N', 'n']:
        if (abs(row_target - row_source) == 2 and abs(col_target - col_source) == 1) or \
           (abs(row_target - row_source) == 1 and abs(col_target - col_source) == 2):
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
        if row_source == row_target:  # Horizontal move
            for col in range(min(col_source, col_target) + 1, max(col_source, col_target)):
                if board[row_source][col] != ' ':
                    return False
            return True
        elif col_source == col_target:  # Vertical move
            for row in range(min(row_source, row_target) + 1, max(row_source, row_target)):
                if board[row][col_source] != ' ':
                    return False
            return True
        elif abs(row_target - row_source) == abs(col_target - col_source):  # Diagonal move
            row_step = 1 if row_target > row_source else -1
            col_step = 1 if col_target > col_source else -1
            for i in range(1, abs(row_target - row_source)):
                if board[row_source + i * row_step][col_source + i * col_step] != ' ':
                    return False
            return True

    # King moves
    elif piece in ['K', 'k']:
        if abs(row_target - row_source) <= 1 and abs(col_target - col_source) <= 1:
            return True

    return False  # Default to invalid move if no valid conditions met


    # return True  # Replace with actual validation logic

# Function to make a move
def make_move(source, target):
    global board
    row_source, col_source = source
    row_target, col_target = target
    board[row_target][col_target] = board[row_source][col_source]
    board[row_source][col_source] = ' '  # Empty source square

# WebSocket server handler
async def chess_server(websocket, path):
    global selected_square, current_player

    try:
        async for message in websocket:
            data = message.split(',')
            action = data[0]

            if action == 'move':
                source = (int(data[1]), int(data[2]))
                target = (int(data[3]), int(data[4]))

                if is_valid_move(source, target):
                    make_move(source, target)
                    current_player = 'b' if current_player == 'w' else 'w'

                # Send updated board state to clients
                await websocket.send(','.join(['board'] + [','.join(row) for row in board]))

    except websockets.exceptions.ConnectionClosed:
        print(f"Connection with {websocket.remote_address} closed")

# Main function to start the server
def main():
    start_server = websockets.serve(chess_server, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Chess server started. Listening on ws://localhost:8765")
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    main()
