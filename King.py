from Piece import piece


class king(piece):  # kill me now the king is exhausting
    name = "king"
    start_rook_spot = None
    end_rook_spot = None

    def __init__(self, white):
        super().__init__(white)
        self.moved = False

    def can_move(self, start, end, board):
        self.needs_to_castle = False

        # check if same color
        if end.piece is not None and end.piece.white == self.white:
            return False
        x = abs(end.x - start.x)
        y = abs(end.y - start.y)
        if end.threatened(self.white, board):
            return False

        if x == 2 and y == 0 and self.is_valid_castling(start, end, board):
            self.needs_to_castle = True
            return True

        # king can move only one step anywhere
        if (x > 1 or y > 1):
            return False

        # TODO: check if end is thretend, return false if so and add to if statement above

        self.moved = True
        return True

    # TODO: add castling shit, see coments for details

    # TODO: create a function that checks if a spot is threatend by the oposite color

    def is_valid_castling(self, start, end, board):
        # path is clear and not treatend, rook on the side we need hasn't moved,
        rook_y = start.y
        print("rook y is ", rook_y)
        end_rook_x = 0
        start_rook_x = 0
        start_check = 0
        end_check = 0

        if end.x == 1:
            end_rook_x = 2
            print("end rook x is ", end_rook_x)

            start_rook_x = 0
            print("start rook x is ", start_rook_x)

            start_check = 1
            end_check = 3

        if end.x == 5:
            end_rook_x = 4
            print("end rook x is ", end_rook_x)

            start_rook_x = 7
            print("start rook x is ", start_rook_x)

            start_check = 4
            end_check = 7

        self.start_rook_spot = board.get_spot_xy(start_rook_x, rook_y)
        print("spot has ", self.start_rook_spot.piece, " piece")

        self.end_rook_spot = board.get_spot_xy(end_rook_x, rook_y)

        if self.start_rook_spot.piece is None:
            print("no rook any more")
            return False
        elif self.start_rook_spot.piece.name == "rook" and self.start_rook_spot.piece.moved:
            print("rook already moved")
            return False
        if self.moved:
            print("king moved already")
            return False

        for i in range(start_check, end_check, 1):
            # if board.get_spot_xy(i, rook_y).piece is not None or board.get_spot_xy(i, rook_y).threatened(self.white,
            #                                                                                              board):
            if board.get_spot_xy(i, rook_y).piece is not None:
                print("way not clear")
                return False

        # if start.threatened(self.white, board) or self.end_rook_spot.threatened(self.white, board) or end.threatened(
        #         self.white, board):
        #     print("way threatened")
        #     return False
        self.needs_to_castle = True
        return True
