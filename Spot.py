

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
        flag1 = False
        flag2 = False
        flag3 = False
        flag4 = False
        for i in range(1, 8):
            if self.x + i < 8 and self.y + i < 8 and not flag1:
                if board.get_spot_xy(self.x + i, self.y + i).piece is not None:
                    flag1 = True
                check_and_append(self.x + i, self.y + i, ["bishop", "queen"])
            if self.x - i >= 0 and self.y - i >= 0 and not flag2:
                if board.get_spot_xy(self.x - i, self.y - i).piece is not None:
                    flag2 = True
                check_and_append(self.x - i, self.y - i, ["bishop", "queen"])
            if self.x + i < 8 and self.y - i >= 0 and not flag3:
                if board.get_spot_xy(self.x + i, self.y - i).piece is not None:
                    flag3 = True
                check_and_append(self.x + i, self.y - i, ["bishop", "queen"])
            if self.x - i >= 0 and self.y + i < 8 and not flag4:
                if board.get_spot_xy(self.x - i, self.y + i).piece is not None:
                    flag4 = True
                check_and_append(self.x - i, self.y + i, ["bishop", "queen"])

        # Straight threats
        flag1 = False
        flag2 = False
        flag3 = False
        flag4 = False
        for i in range(1, 8):
            if self.x + i < 8 and not flag1:
                if board.get_spot_xy(self.x + i, self.y).piece is not None and not flag1:
                    print("woooooooooooooooo")
                    flag1 = True
                    check_and_append(self.x + i, self.y, ["rook", "queen"])

            if self.x - i >= 0 and not flag2:
                if board.get_spot_xy(self.x - i, self.y).piece is not None and not flag2:
                    print("woooooooooooooooo")
                    flag2 = True
                    check_and_append(self.x - i, self.y, ["rook", "queen"])

            if self.y + i < 8 and not flag3:
                if board.get_spot_xy(self.x, self.y + i).piece is not None and not flag3:
                    print("woooooooooooooooo")
                    flag3 = True
                    check_and_append(self.x, self.y + i, ["rook", "queen"])

            if self.y - i >= 0 and not flag4:
                if board.get_spot_xy(self.x, self.y - i).piece is not None and not flag4:
                    print("woooooooooooooooo")
                    flag4 = True
                    check_and_append(self.x, self.y - i, ["rook", "queen"])
            # check_and_append(self.x, self.y + i, ["rook", "queen"])
            # check_and_append(self.x, self.y - i, ["rook", "queen"])
            # check_and_append(self.x + i, self.y, ["rook", "queen"])
            # check_and_append(self.x - i, self.y, ["rook", "queen"])

        # Knight threats
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        for dx, dy in knight_moves:
            x, y = self.x + dx, self.y + dy
            if 0 < x < 8 and 0 < y < 8:
                check_and_append(x, y, ["knight"])

        # Pawn threats
        if white:
            check_and_append(self.x - 1, self.y + 1, ["pawn"])
            check_and_append(self.x + 1, self.y + 1, ["pawn"])
        else:
            check_and_append(self.x - 1, self.y - 1, ["pawn"])
            check_and_append(self.x + 1, self.y - 1, ["pawn"])

        print("threats are ", array_t)
        for i in array_t:
            print(i.piece.name, "at pos: ", i.x, i.y, "is threatning ", self.x, self.y, " spot")

        if len(array_t) > 0:
            return True
