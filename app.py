import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask import request
from flask_socketio import SocketIO, emit
import uuid
import Game
import GameStatus
import Player
from Board import board
import threading
import time
import random

# Initialize Flask application
app = Flask(__name__)
# Initialize SocketIO with Flask app
socketio = SocketIO(app, async_mode='eventlet')

# Initialize game board and players
game_board = board()
p1 = Player.player(True, game_board.get_spot_xy(4, 0), 0)
p2 = Player.player(False, game_board.get_spot_xy(4, 7), 0)
# Initialize game with players and board
handle_moves = Game.game(p1, p2, game_board)

# Initialize sessions dictionary
sessions = {}

# Route for initial page
@app.route('/web', methods=['POST', 'GET'])
def initial_page():
    return render_template('index.html')

# SocketIO event for connecting
@socketio.on('connecting')
def connect():
    emit('init_board', jsonify(chessboard_state()).json)

# Route for main menu
@app.route("/main_manu")
def main_manu():
    return render_template('mainManu.html')

# List of messages
messages = ["Message 1", "Message 2", "Message 3"]

# Function to update message thread
def update_message_thread():
    while True:
        message = random.choice(messages)
        socketio.emit('update_massage', message)
        time.sleep(5)

# Route for generating and storing session identifier
@app.route('/generate_session', methods=['GET'])
def generate_session():
    # Generate session ID
    session_id = str(uuid.uuid4())
    response = jsonify(session_id=session_id)

    # Assign session ID to players
    if p1.session_id == 0:
        p1.session_id = session_id
        response.set_cookie(f'{p1.is_white} white session_id', session_id)
        response.set_cookie(f'{not p1.is_white} white session_id', "-1")
    else:
        if p2.session_id == 0:
            p2.session_id = session_id
            response.set_cookie(f'{p2.is_white} white session_id', session_id)
            response.set_cookie(f'{not p2.is_white} white session_id', "-1")

    return response, 200

# SocketIO event for resetting game
@socketio.on('reset_game')
def reset_game():
    global game_board, handle_moves
    game_board = board()
    handle_moves = Game.game(p1, p2, game_board)
    emit('update_board', jsonify(chessboard_state()).json, broadcast=True)

# Route for getting chessboard state
@app.route('/api')
def chessboard_state():
    # Create dictionary with board state
    board_dict = {
        "spot_matrix": [[{
            "piece_name": game_board.get_spot_xy(j, i).piece.name if game_board.get_spot_xy(j, i).piece else 'x',
            "color": game_board.get_spot_xy(j, i).piece.white if game_board.get_spot_xy(j, i).piece else 'x',
            "col": game_board.get_spot_xy(j, i).x,
            "row": game_board.get_spot_xy(j, i).y,
        } for j in range(8)] for i in range(8)],
        'status': handle_moves.status.name,
        'turn': 'white' if handle_moves.current_turn.is_white else 'black'
    }
    return board_dict

# SocketIO event for making moves
@socketio.on('make_moves')
def make_moves(data):
    # Extract click data
    first_click = data['firstClick']
    second_click = data['secondClick']

    # Determine current player
    player = handle_moves.current_turn

    # Retrieve session ID from cookies
    session_id = request.cookies.get(f'{player.is_white} white session_id')

    # Extract and convert click positions to integer coordinates
    start_x = int(first_click['col'])
    start_y = int(first_click['row'])
    end_x = int(second_click['col'])
    end_y = int(second_click['row'])

    # Get starting and ending spots on game board
    start_spot = game_board.get_spot_xy(start_x, start_y)
    end_spot = game_board.get_spot_xy(end_x, end_y)

    # Check if move is valid and session ID matches
    if start_spot.piece is not None and start_spot != end_spot and session_id == player.session_id:
        # Record and execute move
        move = handle_moves.record_and_do_move(start_spot, end_spot)

        # Update all clients with new board state
        emit('update_board', jsonify(chessboard_state()).json, broadcast=True)

        # Check if move is invalid or game has been won
        if not move:
            error_response = chessboard_state()
            error_response['status'] = 'Invalid move'
            emit('update_board', jsonify(error_response).json, broadcast=True)
        if handle_moves.status == GameStatus.game_status.WHITE_WIN:
            ret = chessboard_state()
            ret['color'] = 'white'
            ret['status'] = 'win'
            emit('update_board', jsonify(ret).json, broadcast=True)
        if handle_moves.status == GameStatus.game_status.BLACK_WIN:
            ret = chessboard_state()
            ret['color'] = 'black'
            ret['status'] = 'win'
            emit('update_board', jsonify(ret).json, broadcast=True)
    else:
        # If move is invalid, notify clients
        error_response = chessboard_state()
        error_response['status'] = 'Invalid move'
        emit('update_board', jsonify(error_response).json, broadcast=True)

# SocketIO event for getting board state
@socketio.on('get_board_state')
def get_board_state():
    emit('update_board', jsonify(chessboard_state()).json)

# Main function
if __name__ == '__main__':
    # Start background thread to update message
    message_thread = threading.Thread(target=update_message_thread)
    message_thread.daemon = True
    message_thread.start()

    # Run Flask app with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)