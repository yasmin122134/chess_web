import Board
import GameStatus
import Move


class game:
    players = [None, None]
    # board = Board.board()

    def __init__(self, player0, player1, board):
        self.players[0] = player0
        self.players[1] = player1
        self.board = board
        self.status = GameStatus.game_status.ACTIVE
        self.played_moves = []

        if player0.is_white:
            self.current_turn = player0
            print("we started with player 0 as white")
        else:
            self.current_turn = player1
            print("we started with player 1 as white")


        self.EndStatus()
        self.isCastling = False

    def EndStatus(self):
        if (self.status != GameStatus.game_status.ACTIVE):
            self.endst = True
            return True
        else:
            self.endst = False
            return False

    def record_and_do_move(self, start_spot, end_spot):
        self.isCastling = False

        # is invalid move
        if (start_spot.piece == None):
            print("move illegal or impossible")
            return False
            # raise ValueError("move illegal or impossible")
        if (start_spot.piece.white != self.current_turn.is_white):
            print("not your turn!")
            return False
            # raise ValueError("not your turn!")
        if (start_spot.piece.can_move(start_spot, end_spot, self.board) == False):
            print("move illegal or impossible")
            return False
            # raise ValueError("move illegal or impossible")


        if (start_spot.piece.name == "king"):
            self.current_turn.king_spot = end_spot

        # record the move
        moved_piece = start_spot.piece
        self.new_move = Move.move(self.current_turn, start_spot, end_spot)
        self.played_moves.append(self.new_move)

        # move
        self.do_the_move(start_spot, end_spot, moved_piece)

        if start_spot.piece.needs_to_castle == True:
            print("needs to castle move")
            self.isCastling = True
            self.do_the_move(moved_piece.start_rook_spot, moved_piece.end_rook_spot, moved_piece.start_rook_spot.piece)
            if self.current_turn == self.players[0]:
                self.current_turn = self.players[1]
            else:
                self.current_turn = self.players[0]



    def do_the_move(self, start_spot, end_spot, moved_piece):


        killed_piece_spot = end_spot
        killed_piece = end_spot.piece
        self.board.set_spot_xy(None, start_spot.x, start_spot.y)
        self.board.set_spot_xy(moved_piece, end_spot.x, end_spot.y)

        # start_spot = self.board.get_spot_xy(start_spot.x, start_spot.y)
        # end_spot = self.board.get_spot_xy(end_spot.x, end_spot.y)


        # dead pice:
        if (killed_piece != None):
            killed_piece_spot.piece = None

        if killed_piece != None and killed_piece.name == "king":
            if self.current_turn.is_white:
                self.status = GameStatus.game_status.WHITE_WIN
            else:
                self.status = GameStatus.game_status.BLACK_WIN



        # set the current turn to the other player
        if self.current_turn == self.players[0]:
            self.current_turn = self.players[1]
            print("now black's turn - player 1")
            print(f"player 1 is black? {self.players[1].is_white}")
        else:
            self.current_turn = self.players[0]
            print("now white's turn - player 0")
            print(f"player 0 is black? {self.players[0].is_white}")



    # def is_check(self, player):
    #     if player.king_spot.threatened():
    #         return True
    #     return False

    def is_check(self, player):
        pass


    def is_mate(self, player):
        pass