import Spot
import Pawn
import Rook
import King
import Knight
import Queen
import Bishop


class board:
    spot_matrix = [[None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None]]

    def __init__(self):
        self.reset_board()
        self.isCastling = False

    def get_spot_xy(self, x, y):
        if (x < 0 or x > 7 or y < 0 or y > 7):
            return False
            # raise IndexError("Index out of bound")
        return self.spot_matrix[x][y]

    def get_spot_matrix(self):
        return self.spot_matrix

    def set_spot_xy(self, piece, x, y):
        self.spot_matrix[x][y] = Spot.spot(piece, x, y)

    def reset_board(self):
        # white
        self.spot_matrix[0][0] = Spot.spot(Rook.rook(True), 0, 0)
        self.spot_matrix[1][0] = Spot.spot(Knight.knight(True), 1, 0)
        self.spot_matrix[2][0] = Spot.spot(Bishop.bishop(True), 2, 0)
        self.spot_matrix[3][0] = Spot.spot(King.king(True), 3, 0)
        self.spot_matrix[4][0] = Spot.spot(Queen.queen(True), 4, 0)
        self.spot_matrix[5][0] = Spot.spot(Bishop.bishop(True), 5, 0)
        self.spot_matrix[6][0] = Spot.spot(Knight.knight(True), 6, 0)
        self.spot_matrix[7][0] = Spot.spot(Rook.rook(True), 7, 0)

        # black
        self.spot_matrix[0][7] = Spot.spot(Rook.rook(False), 0, 7)
        self.spot_matrix[1][7] = Spot.spot(Knight.knight(False), 1, 7)
        self.spot_matrix[2][7] = Spot.spot(Bishop.bishop(False), 2, 7)
        self.spot_matrix[3][7] = Spot.spot(King.king(False), 3, 7)
        self.spot_matrix[4][7] = Spot.spot(Queen.queen(False), 4, 7)
        self.spot_matrix[5][7] = Spot.spot(Bishop.bishop(False), 5, 7)
        self.spot_matrix[6][7] = Spot.spot(Knight.knight(False), 6, 7)
        self.spot_matrix[7][7] = Spot.spot(Rook.rook(False), 7, 7)

        # pawns
        for i in range(0, 8):
            self.spot_matrix[i][1] = Spot.spot(Pawn.pawn(True), i, 1)  # white
            self.spot_matrix[i][6] = Spot.spot(Pawn.pawn(False), i, 6)  # black

        # rest has nothing
        for i in range(2, 6):
            for j in range(0, 8):
                self.spot_matrix[j][i] = Spot.spot(None, j, i)

        return self.spot_matrix
