'''
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
'''

class GameState():
    def __init__(self):
        # Board is an 8x8 two-dimensional list, each element of the list has two characters/
        # First character represents the colour of the piece, 'b' or 'w'.
        # Second character represents the type of the piece, 'R', 'N', 'B', 'Q', 'K', or 'P'
        # '--' represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],      
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]]
        self.whiteToMove = True
        self.moveLog = []