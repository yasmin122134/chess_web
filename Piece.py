class piece:

    # white = True

    def __init__(self, white=False):
        self.killed = False
        self.white = white
        self.needs_to_castle = False


    def can_move(self, start, end, board):
        pass

