class move:

    def is_castling(self, start, end, moved):
        if self.moved_piece.name == "king" and abs(start.x-end.x) == 2 and abs(start.y-end.y) == 0:
            return True
        return False


    def __init__(self, player, start, end):

        self.was_white_move = player.is_white
        self.start = start
        self.end = end
        self.moved_piece = start.piece
        self.killed_piece = end.piece
        self.was_castling = self.is_castling(self.start, self.end, self.moved_piece)
        if (self.killed_piece != None):
            self.did_kill = True
            self.killed_piece.killed = True
        else:
            self.did_kill = False








    # TODO: check if it is a castling move