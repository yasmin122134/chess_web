from enum import Enum

class game_status(Enum):
    ACTIVE = 1
    BLACK_WIN = 2
    WHITE_WIN = 3
    FORFEIT = 4
    STALEMATE = 5
    RESIGNATION = 6
