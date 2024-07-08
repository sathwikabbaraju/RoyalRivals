# server.py
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Initialize the chess board (assuming chess_logic.py handles this)
from chess_logic import initialize_board, is_valid_move, make_move

board = initialize_board()

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({'board': board})

@socketio.on('move')
def handle_move(data):
    source = tuple(map(int, data['source'].split('-')))
    target = tuple(map(int, data['target'].split('-')))
    if is_valid_move(source, target):
        make_move(source, target)
        emit('board_update', {'board': board}, broadcast=True)
    else:
        emit('invalid_move', {'error': 'Invalid move'})

if __name__ == '__main__':
    socketio.run(app)
