
from Tkinter import *
import random

def init():
    rows = canvas.data.rows
    cols = canvas.data.cols
    #assigning the color when that cell is empty(does not have block in it)
    canvas.data.emptyColor = "#1C2124"
    #making the tetris grid
    board = [([canvas.data.emptyColor] * cols) for row in xrange(rows)]
    # pre-load a few cells with known colors for testing purposes
    canvas.data.board = board
    #designing the seven different tetris pieces using 2d lists that holds the
    #truth-value of if that cell contains the piece
    iPiece = [[True,True,True,True]]
    jPiece = [[True,False,False],
              [True,True,True]]
    lPiece = [[False,False,True],
              [True,True,True]]
    oPiece = [[True,True],
              [True,True]] 
    sPiece = [[False,True,True],
              [True,True,False]]
    tPiece = [[False,True,False],
              [True,True,True]]
    zPiece = [[True,True,False],
              [False,True,True]]
    #all the teris pieces are stored in a 3d list called tetrisPieces
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    #the colors of each of the tetris pieces are assigned in the same order in
    #another list called tetrisPiecesColors
    tetrisPieceColors = ["cyan", "blue", "orange", "yellow", "green", "#F4E",
                         "red"]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors
    #choosing an initial fallingPiece
    canvas.data.countMoves = 0
    canvas.data.isGameOver = False
    canvas.data.score = 0
    newFallingPiece()
    timerFired()
    
#draws each cell in the grid    
def drawCell(row,col,color):
    #creates a border for the cell and the actual cell
    canvas.create_rectangle(row, col, row+20, col+20, fill = "black")
    canvas.create_rectangle(row, col, row+20, col+20, fill = color)

#makes the grid
def drawBoard():
    rows = canvas.data.rows
    cols = canvas.data.cols
    removeFullRows()
    for row in xrange(rows):
        for col in xrange(cols):
            drawCell(20+col*20, 20+row*20,canvas.data.board[row][col])
    if(canvas.data.isGameOver == True):
        canvas.create_text(((cols*20+20)/2), (((rows*20)+20)/2),
            text = "Game Over!!", fill = "white",
            font = "Times 30 bold")
            
#to randomly chose a piece, set its color and position it in the middle of the
#top row   
def newFallingPiece():
    #random.randint(a,b) gives a random number n between a and b such that
    # a <= n <= b
    #chooses a random tetris piece to be the next falling piece
    index = random.randint(0,6)
    canvas.data.fallingPiece = canvas.data.tetrisPieces[index]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[index]
    #ensuring that the falling piece starts in the middle of the top row
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2
    #to compensate for it being off to the right
    canvas.data.fallingPieceCol -= canvas.data.fallingPieceCol/2
    
def drawFallingPiece():
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            if (canvas.data.fallingPiece[row][col] == True):
                drawCell(20+(canvas.data.fallingPieceCol+col)*20,
                         20+(canvas.data.fallingPieceRow+row)*20,
                         canvas.data.fallingPieceColor)
                
def fallingPieceIsLegal():
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                if(((canvas.data.fallingPieceRow+row) < 0) or
                    ((canvas.data.fallingPieceCol+col) < 0) or
                    ((canvas.data.fallingPieceRow+row) >=
                        len(canvas.data.board)) or
                    ((canvas.data.fallingPieceCol+col) >=
                        len(canvas.data.board[0]))):
                    return False
                elif(canvas.data.board[(canvas.data.fallingPieceRow+row)]
                     [(canvas.data.fallingPieceCol+col)] !=
                     canvas.data.emptyColor):
                    return False
    return True

def moveFallingPiece(drow,dcol):
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if(fallingPieceIsLegal() == False):
        canvas.data.fallingPieceRow -= drow
        canvas.data.fallingPieceCol -= dcol
        return False
    return True
     
def fallingPieceCenter():
    row = canvas.data.fallingPieceRow + (len(canvas.data.fallingPiece)/2)
    col = canvas.data.fallingPieceCol + (len(canvas.data.fallingPiece[0])/2)
    return (row,col)
    
def rotateFallingPiece():
    fallingPiece = canvas.data.fallingPiece
    oldRows = len(fallingPiece)
    oldCols = len(fallingPiece[0])
    newRows = oldCols
    newCols = oldRows
    rotatedFallingPiece = [([True] * newCols) for i in xrange(newRows)]
    for row in xrange(oldRows-1,-1,-1):
        for col in xrange(oldCols): 
            rotatedFallingPiece[oldCols-1-col][row] = fallingPiece[row][col]
    (oldCenterRow,oldCenterCol) = fallingPieceCenter()
    canvas.data.fallingPiece = rotatedFallingPiece
    (newCenterRow,newCenterCol) = fallingPieceCenter()
    fallingPieceRow = canvas.data.fallingPieceRow
    fallingPieceCol = canvas.data.fallingPieceCol
    canvas.data.fallingPieceRow += (oldCenterRow - newCenterRow)
    canvas.data.fallingPieceCol += (oldCenterCol - newCenterCol)
    if (fallingPieceIsLegal() == False):
        canvas.data.fallingPiece = fallingPiece
        canvas.data.fallingPieceRow = fallingPieceRow
        canvas.data.fallingPieceCol = fallingPieceCol
        
def dropPiece():
    movePossible = True
    while(movePossible == True):
        drow = 1
        dcol = 0
        canvas.data.score += 2
        movePossible = moveFallingPiece(drow,dcol)
        if(movePossible == True):
            canvas.data.countMoves += 1

def placeFallingPiece():
    fallingPieceRow = canvas.data.fallingPieceRow
    fallingPieceCol = canvas.data.fallingPieceCol
    color = canvas.data.fallingPieceColor
    board = canvas.data.board
    for row in xrange(len(canvas.data.fallingPiece)):
        for col in xrange(len(canvas.data.fallingPiece[0])):
            if (canvas.data.fallingPiece[row][col] == True):
                board[(fallingPieceRow+row)][(fallingPieceCol+col)] = color
                canvas.data.board = board
                
def copyRow(oldRow,newRow):
    for element in xrange(len(canvas.data.board[0])):
        canvas.data.board[newRow][element] = canvas.data.board[oldRow][element]
                
def removeFullRows():
    rows = canvas.data.rows
    newRow = rows-1
    fullRowCount = 0
    for oldRow in xrange(rows-1,-1,-1):
        if(canvas.data.board[oldRow].count("#1C2124") != 0):
            copyRow(oldRow,newRow)
            newRow -= 1
        else:
            fullRowCount += 1
    for fillRow in xrange(newRow,-1,-1):
        for element in xrange(len(canvas.data.board[0])):
            canvas.data.board[fillRow][element] = "#1C2124"
    canvas.data.score += int(fullRowCount**2)*100
        
#remakes the game at it current position evertime it is redrawn
def drawGame():
    canvas.create_rectangle(0,0,canvas.data.cols*20 + 40,canvas.data.rows*20
                            + 40, fill = "black")
    drawBoard()
    drawFallingPiece()
    
def drawScore():
    canvas.create_text((canvas.data.cols*20)/2, 10, text = "SCORE = %d" %(canvas.data.score), fill = "white", font = "Times 16 bold")
    
#initiates the moving and rotation of the falling piece 
def keyPressed(event):
    if(canvas.data.isGameOver == False):
        if(event.keysym == "Left"):
            drow = 0
            dcol = -1
            moveFallingPiece(drow,dcol)
        elif(event.keysym == "Right"):
            drow = 0
            dcol = 1
            moveFallingPiece(drow,dcol)
        elif(event.keysym == "Down"):
            drow = 1
            dcol = 0
            canvas.data.score += 1
            movePossible = moveFallingPiece(drow,dcol)
            if(movePossible == True):
                canvas.data.countMoves += 1
        elif(event.keysym == "Up"):
            rotateFallingPiece()
        elif(event.keysym == "space"):
            dropPiece()
        redrawAll()
    if(event.char == "r"):
        init()
    
def timerFired():
    if(canvas.data.isGameOver == False):
        movePossible = moveFallingPiece(1,0)
        if(movePossible == True):
            canvas.data.countMoves += 1
        else:
            if(canvas.data.countMoves == 0):
                canvas.data.isGameOver = True
            placeFallingPiece()
            newFallingPiece()
            canvas.data.countMoves = 0
        redrawAll()
    delay = 500
    canvas.after(delay, timerFired)
    
def redrawAll():
    canvas.delete(ALL)
    drawGame()
    drawScore()

# to create the root and canvas
def run(rows,cols):
    global canvas
    root = Tk()
    canvas = Canvas(root, width = cols*20 +40, height = rows*20 + 40)
    canvas.pack()
    root.resizable(width = 0, height = 0)
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    init()
    redrawAll()
    root.bind("<Key>", keyPressed)
    root.mainloop()
    
run(20,10)
