# import sys
# import pygame
# import Game
# import GameStatus
# import Player
# from Board import board
# import numpy as np
# import Spot
# import Rook
# import King
# import Knight
# import Queen
# import Bishop
# import Spot
#
#
#
# game_board = board()
#
# p1 = Player.player(True, game_board.get_spot_xy(4, 0))
# p2 = Player.player(False, game_board.get_spot_xy(4, 7))
# handle_moves = Game.game(p1, p2, game_board)
#
#
#
# #  # based on the first and second move in the jason object:
# start_spot = game_board.get_spot_xy(x, y)
# end_spot = game_board.get_spot_xy(x, y)
#
# if (start_spot.piece is not None and start_spot != end_spot):  # has a piece at first clicked place
#     handle_moves.record_and_do_move(start_spot, end_spot)
#     print("Selected piece:", start_spot.piece.name, "at position:", start_spot.x, start_spot.y)
#     print("Move to position:", end_spot.x, end_spot.y)
#
# click_positions = []  # Clear the click positions for the next pair of clicks
#
#
#
# if handle_moves.status == 2:
#     print("black wins!!!")
# else:
#     print("white wins!!!")
#
