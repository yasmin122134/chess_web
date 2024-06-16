from Piece import piece

# Define the Pawn class, which inherits from the Piece class
class pawn(piece):

    # Set the name of the piece
    name = "pawn"

    # Initialize the Pawn instance
    def __init__(self, white):
        # Call the parent class's initializer
        super().__init__(white)

        # Set the direction of movement based on the color of the piece
        if (self.white):
            self.forward = 1
        else:
            self.forward = -1

    # Define the movement rules for the Pawn piece
    def can_move(self, start, end, board):

        # Check if the piece is moving forward
        if (end.y - start.y == self.forward):
            # Check if the piece is moving diagonally to capture an opponent's piece
            if (abs(end.x - start.x) == 1):
                if (end.piece is not None and end.piece.white != self.white):
                    return True
            # Check if the piece is moving straight forward
            elif (end.x == start.x):
                if (end.piece == None):
                    return True
        # Check if the piece is making its initial two-square move
        if (end.x == start.x and end.y - start.y == 2 * self.forward):
            if (board.get_spot_xy(start.x, start.y + self.forward).piece == None and board.get_spot_xy(start.x, start.y + self.forward*2
                                                                                                       ).piece == None):
                if ((self.white == True and start.y == 1) or (self.white == False and start.y == 6)):
                    return True
        else:
            return False