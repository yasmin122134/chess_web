from Piece import piece


class bishop(piece):
    name = "bishop"

    def __init__(self, white):
        super().__init__(white)

    def can_move(self, start, end, board):

        if (end.piece != None and end.piece.white == self.white):
            return False

        x = abs(end.x - start.x)
        y = abs(end.y - start.y)

        if (x == y and self.way_clear(start, end, board)):
            return True

        return False


    def way_clear(self, start, end, board):
        x_step = y_step = 1
        x_index = []
        y_index = []
        if (start.x > end.x):
            x_step = -1
        if start.y > end.y:
            y_step = -1

        for i in range(start.x+x_step, end.x, x_step):
            x_index.append(i)
        for i in range(start.y+y_step, end.y, y_step):
            y_index.append(i)

        print(x_index)
        print(y_index)

        for i in range(len(x_index)):
            temp_spot = board.get_spot_xy(x_index[i], y_index[i])
            print(
                f"Spot to check - x: {temp_spot.x}, y: {temp_spot.y}, piece there: {temp_spot.piece.name if temp_spot.piece is not None else None}")
            if (temp_spot.piece != None):
                return False

        return True
