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

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Initialize game
game_board = board()
print("created game_board")
p1 = Player.player(True, game_board.get_spot_xy(4, 0), 0)
p2 = Player.player(False, game_board.get_spot_xy(4, 7), 0)
handle_moves = Game.game(p1, p2, game_board)

# Initialize sessions
sessions = {}

@app.route('/web', methods=['POST', 'GET'])
def initial_page():
    return render_template('index.html')

@socketio.on('connecting')
def connect():
    emit('init_board', jsonify(chessboard_state()).json)

@app.route("/main_manu")
def main_manu():
    return render_template('mainManu.html')

# Route for generating and storing session identifier
@app.route('/generate_session', methods=['GET'])
def generate_session():
    session_id = str(uuid.uuid4())
    response = jsonify(session_id=session_id)

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

@socketio.on('reset_game')
def reset_game():
    global game_board, handle_moves
    game_board = board()
    handle_moves = Game.game(p1, p2, game_board)
    emit('update_board', jsonify(chessboard_state()).json, broadcast=True)

@app.route('/api')
def chessboard_state():
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

@socketio.on('make_moves')
def make_moves(data):
    first_click = data['firstClick']
    second_click = data['secondClick']
    player = handle_moves.current_turn
    session_id = request.cookies.get(f'{player.is_white} white session_id')

    start_x = int(first_click['col'])
    start_y = int(first_click['row'])
    end_x = int(second_click['col'])
    end_y = int(second_click['row'])
    print(f"start_x: {start_x}, start_y: {start_y}, end_x: {end_x}, end_y: {end_y}")

    start_spot = game_board.get_spot_xy(start_x, start_y)
    end_spot = game_board.get_spot_xy(end_x, end_y)

    if start_spot.piece is not None and start_spot != end_spot and session_id == player.session_id:
        print("valid move")
        move = handle_moves.record_and_do_move(start_spot, end_spot)
        emit('update_board', jsonify(chessboard_state()).json, broadcast=True)

        if not move:
            print("actually invalid move")
            error_response = chessboard_state()
            error_response['status'] = 'Invalid move'

            emit('update_board', jsonify(error_response).json, broadcast=True)
            # return jsonify(error_response), 403
        if handle_moves.status == GameStatus.game_status.WHITE_WIN:
            ret = chessboard_state()
            ret['color'] = 'white'
            ret['status'] = 'win'
            emit('update_board', jsonify(ret).json, broadcast=True)
            # return jsonify(ret), 200
        if handle_moves.status == GameStatus.game_status.BLACK_WIN:
            ret = chessboard_state()
            ret['color'] = 'black'
            ret['status'] = 'win'
            emit('update_board', jsonify(ret).json, broadcast=True)
            # return jsonify(ret), 200
    else:
        error_response = chessboard_state()
        error_response['status'] = 'Invalid move'
        emit('update_board', jsonify(error_response).json, broadcast=True)
        # return jsonify(error_response), 403

@socketio.on('get_board_state')
def get_board_state():
    emit('update_board', jsonify(chessboard_state()).json)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
