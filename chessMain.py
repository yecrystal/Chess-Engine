'''
This is the main driver file. It will be responsible for handling user input and displaying the current GameState object.
'''

import pygame as p
from chessEngine import GameState, Move

WIDTH = HEIGHT = 512
DIMENSION = 8 # Dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animations
IMAGES = {}  # Initialize IMAGES as a dictionary

'''
Initialize a global dictionary of images. this will be called exactly once in the main.
'''
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ' ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Can access an image by saying 'IMAGES['wp']'
    
'''
The main driver for the code. This will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made

    loadImages() # Only once before the while loop
    running = True
    sqSelected = () # No square is selected initially, keep track of last click of the user (tuple: (row, col)))
    playerClicks = [] # Keep track of the player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: 
                location = p.mouse.get_pos() # Get (x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # The user clicked the same square twice
                    sqSelected = () # Deselect
                    playerClicks = [] # Clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append for both 1st and 2nd clicks
                if len(playerClicks) == 2: # After 2nd click
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotiation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () # Reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            # Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs.board)  # Pass gs.board instead of gs to the drawGameState function
        clock.tick(MAX_FPS)
        p.display.flip()
'''
Responsible for all graphics within the current game state. Top left square is always light.
'''
def drawGameState(screen, board):
    drawBoard(screen) # Draw the squares on the board
    drawPieces(screen, board) # Draw pieces on top of the squares

'''
Draw the squares on the board
'''
def drawBoard(screen):
    colours = [p.Color("white"), p.Color("pink")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c)%2)]
            p.draw.rect(screen, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # Not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
