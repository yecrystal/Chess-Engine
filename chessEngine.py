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
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
  
    '''
    Takes a move as a parameter and executes it (this will not work for castline, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # Swap players
        # Update the king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
    

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # Make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Switch turns back
            # Update the king's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: # Only 1 check, block check, or move king
                moves = self.getAllPossibleMoves()
                # To block a check, you must move a piece into one of th esquares between the enemy piece and king
                check = self.checks[0] # Check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # Enemy piece causing the check
                validSquares = [] # Squares the pieces can move to
                # If knight, must capture or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Returns if the player is in check, a list of pins and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] # Squares where the allied pinned piece is and direction pinned from
        checks = [] # Squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColour = "b"
            allyColour = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColour = "w"
            allyColour = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]        
        # Check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # Reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColour:
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or check possible in this direction
                            break
                elif endPiece[0] == enemyColour:
                    type = endPiece[1]
                    # 5 possibilities here in this complex conditional
                    # 1) Orthogonally away from king and piece is a rook
                    # 2) Diagonally away from king and piece is a bishop
                    # 3) 1 square away diagonally from kind and piece is a pawn
                    # 4) Any direction and piece is a queen
                    # 5) Any direction 1 sqaure away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                    if (0 <= j <= 3 and type == 'R') or \
                        (4 <= j <= 7 and type == 'B') or \
                        (i == 1 and type == 'p' and ((enemyColour == 'w' and 6 <= j <= 7) or (enemyColour == 'b' and 4 <= j <= 5))) or \
                        (type == 'Q') or (i == 1 and type == 'K'):
                        if possiblePin == (): # No piece blocking, so check
                            inCheck = True
                            checks.append((endRow, endCol, d[0], d[1]))
                            break
                        else: # Piece blocking so pin
                            pins.append(possiblePin)
                            break
                    else: # Enemy piece not applying check
                        break
            else:
                break # Off board
        # Check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColour and endPiece[1] == 'N': # Enemy knight attacking king
                        inCheck = True
                        checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # Number of rows
            for c in range(len(self.board[r])): # Number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move functions based on piece type
        return moves
                
    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # White pawn moves
            if self.board[r - 1][c] == "--": # ! square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r-1][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # Captures
            if c - 1 >= 0: # Captures to the left, also make sure that it doesn't go off the board
                if self.board[r - 1][c - 1][0] == 'b': # Enemy piece to c apture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7: # captures to the right
                if self.board[r - 1][c + 1][0] == 'b': # Enemy piece to capute
                     moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else: # Black pawn moves
            if self.board[r + 1][c] == "--": # ! square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--': # 2 square moves
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # Captures
            if c - 1 >= 0: # Caoture to left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7: # Caoture to right 
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        # Pass pawn promotions later     

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Up, left, down, right
        enemyColour = "b" if self.whiteToMove else "w" 
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColour: # Enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece invalid
                        break
                else: # Off board
                    break

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColour = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour: # Not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # 4 diagonals
        enemyColour = "b" if self.whiteToMove else "w" 
        for d in directions:
            for i in range(1, 8): # Bishop can move max of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # Is it on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColour: # Enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece invalid
                        break
                else: # Off board
                    break

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColour = "w" if self.whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColour: # Not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    # Maps keys to values
    # Key : Value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6":2, "7": 1, "8": 0} 

    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
            
    ''' 
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotiation(self):
        # Can change to real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

