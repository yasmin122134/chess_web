from Piece import piece



class pawn(piece):

    name = "pawn"
    def __init__(self, white):
        super().__init__(white)
        if (self.white):
            self.forward = 1
        else:
            self.forward = -1


    def can_move(self, start, end, board):

        if (end.y - start.y == self.forward):
            if (abs(end.x - start.x) == 1):
                if (end.piece is not None and end.piece.white != self.white):
                    return True
            elif (end.x == start.x):
                if (end.piece == None):
                    return True
        if (end.x == start.x and end.y - start.y == 2 * self.forward):
            if (board.get_spot_xy(start.x, 2).piece == None and board.get_spot_xy(start.x, 3).piece == None):
                if ((self.white == True and start.y == 1) or (self.white == False and start.y == 6)):
                    return True
        else:
            return False


