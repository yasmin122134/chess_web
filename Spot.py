

class spot:

    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y


    def threatened(self, white, board):
        array_t = []

        def check_and_append(x, y, piece_names):
            try:
                spot = board.get_spot_xy(x, y)
                if spot.piece is not None and spot.piece.name in piece_names and spot.piece.white != white:
                    array_t.append(spot)
            except IndexError:
                pass

        # Diagonal threats
        for i in range(1, 8):
            if self.x + i < 8 and self.y + i < 8:
                check_and_append(self.x + i, self.y + i, ["bishop", "queen"])
            if self.x - i >= 0 and self.y - i >= 0:
                check_and_append(self.x - i, self.y - i, ["bishop", "queen"])
            if self.x + i < 8 and self.y - i >= 0:
                check_and_append(self.x + i, self.y - i, ["bishop", "queen"])
            if self.x - i >= 0 and self.y + i < 8:
                check_and_append(self.x - i, self.y + i, ["bishop", "queen"])

        # Straight threats
        for i in range(1, 8):
            check_and_append(self.x, self.y + i, ["rook", "queen"])
            check_and_append(self.x, self.y - i, ["rook", "queen"])
            check_and_append(self.x + i, self.y, ["rook", "queen"])
            check_and_append(self.x - i, self.y, ["rook", "queen"])

        # Knight threats
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        for dx, dy in knight_moves:
            x, y = self.x + dx, self.y + dy
            if 0 < x < 8 and 0 < y < 8:
                check_and_append(x, y, ["knight"])

        return array_t
