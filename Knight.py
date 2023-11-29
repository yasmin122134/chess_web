from Piece import piece


class knight(piece):
    name = "knight"

    def __init__(self, white):
        self.white = super().__init__(white)
        super().__init__(white)

    def can_move(self, start, end, board):
        if (end.piece != None and end.piece.white == self.white):
            return False

        x = end.x - start.x
        y = end.y - start.y
        xy = abs(x * y)

        if (xy == 2):
            return True
        return False




# some kind of change


