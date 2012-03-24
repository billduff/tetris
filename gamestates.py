class Gamestate(object):
    def __init__(self, name, board, fallingPiece, lost):
        self.board = board
        self.fallingPiece = fallingPiece
        self.lost = lost
