import json

from flask import Flask, render_template, request, jsonify

import Game
import GameStatus
import Player
from Board import board

app = Flask(__name__)

initialized = False
def initialize_game():
    # global game_board
    game_board = board()
    print("created game_board")

    p1 = Player.player(True, game_board.get_spot_xy(4, 0))
    p2 = Player.player(False, game_board.get_spot_xy(4, 7))
    handle_moves = Game.game(p1, p2, game_board)
    return game_board, p1, p2, handle_moves


@app.route('/web', methods = ['POST', 'GET'])
def initial_page():
    global initialized
    global handle_moves, game_board
    if request.method == 'GET':
        print(f"init is {initialized}")
        if initialized == False:
            game_board, p1, p2, handle_moves = initialize_game()
            initialized = True
        else:
            pass
    if request.method == 'POST':
        game_board, p1, p2, handle_moves = initialize_game()
        initialized = True


    return render_template('index.html', message='Hello, World!, balu, meeeh')

@app.route('/reset')
def reset_game():
    global handle_moves, game_board
    game_board = board()
    game_board, p1, p2, handle_moves = initialize_game()

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


@app.route('/about')
def about():
    return "this is my flask app, "


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
        print("inside make move")
        data = request.get_json()

        # Access the moves from the JSON data
        first_click = data['firstClick']
        second_click = data['secondClick']

        start_x = int(first_click['col'])
        start_y = int(first_click['row'])
        end_x = int(second_click['col'])
        end_y = int(second_click['row'])

        start_spot = game_board.get_spot_xy(start_x, start_y)
        print(start_x, start_y)
        print(start_spot.piece)
        end_spot = game_board.get_spot_xy(end_x, end_y)

        if start_spot.piece is not None and start_spot != end_spot:  # has a piece at first clicked place
            color = "black"
            if start_spot.piece.white:
                color = "white"
            color_piece = {"color": color,
                           "piece": start_spot.piece.name,
                           "piece_2": 'x'}
            ret = handle_moves.record_and_do_move(start_spot, end_spot)

            print("Selected piece:", start_spot.piece.name, "at position:", start_spot.x, start_spot.y)
            print("Move to position:", end_spot.x, end_spot.y)

            if (ret == False):
                color_piece = {'error': 'Invalid move',
                               'piece': 'x',
                               "piece_2": 'x'}
            if handle_moves.isCastling:
                color_piece = {"color": color,
                               "piece": start_spot.piece.name,
                               "piece_2": "rook",
                               "row": end_spot.y,
                               "col": (end_spot.x + 1) / 2 + 1,
                               "img_col": (int(((end_spot.x + 1) / 2 + 1) / 3)) * 7}

            return jsonify(color_piece), 200

        else:
            print("wuttttttt????????????")
            print(start_spot.piece)
            print(start_spot.x, " , ", start_spot.y)
            print("move wierd")
            # Return an error response with a 400 status code

            error_response = {'error': 'Invalid move',
                              'piece': 'x'}
            return jsonify(error_response), 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
