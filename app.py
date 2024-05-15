import json
import uuid
from flask import Flask, render_template, request, jsonify, make_response
import Game
import GameStatus
import Player
from Board import board

app = Flask(__name__)

game_board = board()
print("created game_board")
p1 = Player.player(True, game_board.get_spot_xy(4, 0), 0)
p2 = Player.player(False, game_board.get_spot_xy(4, 7), 0)
handle_moves = Game.game(p1, p2, game_board)

sessions = {}

@app.route('/web', methods = ['POST', 'GET'])
def initial_page():
    return render_template('index.html')


@app.route("/main_manu")
def main_manu():
    return render_template('mainManu.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/")
def openPage():
    return render_template('openPage.html')


# Route for generating and storing session identifier
@app.route('/generate_session', methods=['GET'])
def generate_session():
    print("in generate session")
    session_id = str(uuid.uuid4())

    # Create a JSON response with the session ID
    response = jsonify(session_id=session_id)

    # Set the session ID as a cookie in the response
    if p1.session_id == 0:
        p1.session_id = session_id
        response.set_cookie(f'{p1.is_white} white session_id', session_id)
        response.set_cookie(f'{not p1.is_white} white session_id', "-1")


        print("p1 session id is ", p1.session_id)
        return response, 200
    else:
        if p2.session_id == 0:
            p2.session_id = session_id
            response.set_cookie(f'{p2.is_white} white session_id', session_id)
            response.set_cookie(f'{not p2.is_white} white session_id', "-1")

            print("p2 session id is ", p2.session_id)
            return response, 200


@app.route('/reset')
def reset_game():
    game_board = board()
    print("created game_board")
    handle_moves = Game.game(p1, p2, game_board)

    return chessboard_state()


@app.route('/api')
def chessboard_state():
    print("getting chessboard state from /api")

    board_dict = {
        "spot_matrix": [[{
            "piece_name": game_board.get_spot_xy(j,i).piece.name if game_board.get_spot_xy(j,i).piece else 'x',
            "color": game_board.get_spot_xy(j,i).piece.white if game_board.get_spot_xy(j,i).piece else 'x',
            "col": game_board.get_spot_xy(j,i).x,
            "row": game_board.get_spot_xy(j,i).y,
        } for j in range(8)] for i in range(8)],
    }

    print(board_dict)

    board_json = json.dumps(board_dict)
    return board_json, 200




@app.route('/tile/<tile_name>')
def get_tile(tile_name):
    return render_template('index.html', message=f"You clicked on the {tile_name} tile."), 200


@app.route('/make_moves', methods=['POST', 'GET'])
def make_moves():
    print(f"it is {handle_moves.current_turn.is_white} that it is whites turn")
    if request.method == 'GET':
        print("inside get req")
        # Return the initial state of the chessboard
        # game_board = board()

        return render_template('chess.html')
    elif request.method == 'POST':
        print("inside make move post req")
        data = request.get_json()

        # Access the moves from the JSON data
        first_click = data['firstClick']
        second_click = data['secondClick']
        player = handle_moves.current_turn

        session_id = request.cookies.get(f'{player.is_white} white session_id')

        start_x = int(first_click['col'])
        start_y = int(first_click['row'])
        end_x = int(second_click['col'])
        end_y = int(second_click['row'])

        start_spot = game_board.get_spot_xy(start_x, start_y)
        print(start_x, start_y)
        print(start_spot.piece)
        end_spot = game_board.get_spot_xy(end_x, end_y)

        if start_spot.piece is not None and start_spot != end_spot and session_id == player.session_id:  # has a piece at first clicked place
            color = "black"
            if start_spot.piece.white:
                color = "white"
            color_piece = {"color": color,
                           "piece": start_spot.piece.name,
                           "piece_2": 'x',
                           'status': 'active'}
            ret = handle_moves.record_and_do_move(start_spot, end_spot)

            print("Selected piece:", start_spot.piece.name, "at position:", start_spot.x, start_spot.y)
            print("Move to position:", end_spot.x, end_spot.y)

            if (ret == False):
                color_piece = {'color': 'Invalid move',
                               'piece': 'x',
                               "piece_2": 'x',
                               'status': 'Invalid move'}
            if handle_moves.isCastling:
                color_piece = {"color": color,
                               "piece": start_spot.piece.name,
                               "piece_2": "rook",
                               "row": end_spot.y,
                               "col": (end_spot.x + 1) / 2 + 1,
                               "img_col": (int(((end_spot.x + 1) / 2 + 1) / 3)) * 7,
                               'status': 'castling'}
            if handle_moves.status == GameStatus.game_status.WHITE_WIN:
                color_piece = {'color': 'white',
                               'piece': 'king',
                               "piece_2": 'x',
                               'status': 'win'}
            if handle_moves.status == GameStatus.game_status.BLACK_WIN:
                color_piece = {'color': 'black',
                               'piece': 'king',
                               "piece_2": 'x',
                               'status': 'win'}

            return jsonify(color_piece), 200

        else:
             # Invalid move
            error_response = {'error': 'Invalid move',
                              'color': 'Invalid move',
                              'piece': 'x'}
            return jsonify(error_response), 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
