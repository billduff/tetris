from Tkinter import *
import random
import fileinput
import messenger
import iputils
import re
import json
import jsonutils

standardDelay = 600

def init():
        canvas.quotes = []
        getQuotes()
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
        restart()
        timerFired()
        
def restart():
        #init the clean board
        rows = canvas.data.rows
        cols = canvas.data.cols
        #assigning the color when that cell is empty(does not have block in it)
        canvas.data.emptyColor = "#1C2124"
        board = [([canvas.data.emptyColor] * cols) for row in xrange(rows)]
        canvas.data.board = board
        
        canvas.data.Moved = 0
        canvas.data.isGameOver = False
        canvas.data.score = 0
        canvas.data.canHold = True
        canvas.data.landed = False
        canvas.data.spacePressed = False
        canvas.data.delay = standardDelay
        canvas.data.heldPiece = None
        canvas.data.heldPieceColor = None
        canvas.data.nextPiece = None
        canvas.data.nextPieceColor = None
        canvas.data.shadowPieceColor = "white"
        newNextPiece()
        newFallingPiece()

def getQuotes():
        for line in fileinput.input("eddie_quotes.txt"):
                canvas.quotes.append(line[:-1])

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
                quoteNum = random.randint(0, len(canvas.quotes) - 1)
                canvas.create_text(((cols*20+20)/2), (((rows*20)+20)/2),
                        text = "Game Over\n", fill = "white",
                        font = "Courier 22 bold")
                #display a random Eddie quote when you die, like COD but better
                #x0 y0 x1 y1
                canvas.create_rectangle(20, (((rows*20)+180)/2),
                                                                20+(cols*20), (((rows*20)+290)/2),
                                                                fill = "#1C2124")
                canvas.create_text(25, (((rows*20)+200)/2),
                        anchor = "nw",
                        width = (cols*20),
                        text = "\"" + canvas.quotes[quoteNum] + "\" - Eddie",
                        fill = "white", font = "Courier 12 bold")
   
#to randomly chose a next piece, set its color and position it in the
#middle of the top row         
def newNextPiece():
        index = random.randint(0,6)
        canvas.data.nextPiece = canvas.data.tetrisPieces[index]
        canvas.data.nextPieceColor = canvas.data.tetrisPieceColors[index]
                        
#choose the new falling piece to be the 'next piece'
def newFallingPiece():
        canvas.data.fallingPiece = canvas.data.nextPiece
        canvas.data.fallingPieceColor = canvas.data.nextPieceColor
        #ensuring that the falling piece starts in the middle of the top row
        canvas.data.fallingPieceRow = 0
        canvas.data.fallingPieceCol = canvas.data.cols/2
        #to compensate for it being off to the right
        canvas.data.fallingPieceCol -= canvas.data.fallingPieceCol/2
        canvas.data.fallingPieceRotation = 0
        
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

#OOP this and clean it up later
def shadowPieceIsLegal():
        for row in xrange(len(canvas.data.shadowPiece)):
                for col in xrange(len(canvas.data.shadowPiece[0])):
                        if(canvas.data.shadowPiece[row][col] == True):
                                if(((canvas.data.shadowPieceRow+row) < 0) or
                                        ((canvas.data.shadowPieceCol+col) < 0) or
                                        ((canvas.data.shadowPieceRow+row) >=
                                                len(canvas.data.board)) or
                                        ((canvas.data.shadowPieceCol+col) >=
                                                len(canvas.data.board[0]))):
                                        return False
                                elif(canvas.data.board[(canvas.data.shadowPieceRow+row)]
                                         [(canvas.data.shadowPieceCol+col)] !=
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
         
#Find the point of rotation for falling pieces
def fallingPieceCenter():
        iPiece1 = [[True,True,True,True]]
        iPiece2 = [[True],[True],[True],[True]]
        jPiece1 = [[True,False,False],[True,True,True]]
        jPiece2 = [[False,True],[False,True],[True,True]]
        jPiece3 = [[True,True,True],[False,False,True]]
        jPiece4 = [[True,True],[True,False],[True,False]]
        lPiece1 = [[False,False,True],[True,True,True]]
        lPiece2 = [[True, False],[True,False],[True,True]]
        lPiece3 = [[True,True,True],[True,False,False]]
        lPiece4 = [[True,True],[False,True],[False,True]]
        oPiece = [[True,True],[True,True]]
        sPiece1 = [[False,True,True],[True,True,False]]
        sPiece2 = [[True, False],[True, True], [False,True]]
        tPiece1 = [[False,True,False],[True,True,True]]
        tPiece2 = [[True, False],[True, True],[True, False]]
        tPiece3 = [[True,True,True],[False,True,False]]
        tPiece4 = [[False,True],[True,True],[False,True]]
        zPiece1 = [[True,True,False],[False,True,True]]
        zPiece2 = [[False, True],[True,True],[True, False]]
        #I pieces
        if(canvas.data.fallingPiece == iPiece1):
                if (canvas.data.fallingPieceRotation / 2) == 0:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol+2)
                else:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol+3)
        elif(canvas.data.fallingPiece == iPiece2):
                if (canvas.data.fallingPieceRotation / 2) == 0:
                        return(canvas.data.fallingPieceRow+3, canvas.data.fallingPieceCol + 1)
                else:
                        return(canvas.data.fallingPieceRow+2, canvas.data.fallingPieceCol + 1)
        #J Pieces
        elif(canvas.data.fallingPiece == jPiece1): 
                return(canvas.data.fallingPieceRow +1, canvas.data.fallingPieceCol +1)
        elif(canvas.data.fallingPiece == jPiece2): 
                return(canvas.data.fallingPieceRow+1, canvas.data.fallingPieceCol +1)
        elif(canvas.data.fallingPiece == jPiece3): 
                return(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol +1)
        elif(canvas.data.fallingPiece == jPiece4):
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol)
        # L pieces
        elif(canvas.data.fallingPiece == lPiece1): 
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
        elif(canvas.data.fallingPiece == lPiece2): 
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol)
        elif(canvas.data.fallingPiece == lPiece3): 
                return(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol + 1)
        elif(canvas.data.fallingPiece == lPiece4): 
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
        #O Pieces
        elif(canvas.data.fallingPiece == oPiece): 
                row = canvas.data.fallingPieceRow
                col = canvas.data.fallingPieceCol
                return (row, col)
        #S Pieces
        elif(canvas.data.fallingPiece == sPiece1):
                if (canvas.data.fallingPieceRotation / 2) == 0:
                        return(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol + 1)
                else:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
        elif(canvas.data.fallingPiece == sPiece2):
                if (canvas.data.fallingPieceRotation / 2) == 0:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol)
                else:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
        #T Pieces
        elif(canvas.data.fallingPiece == tPiece1): 
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
        elif(canvas.data.fallingPiece == tPiece2): 
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol)
        elif(canvas.data.fallingPiece == tPiece3): 
                return(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol + 1)
        elif(canvas.data.fallingPiece == tPiece4): 
                return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol+1)
        #Z Pieces
        elif(canvas.data.fallingPiece == zPiece1):
                if (canvas.data.fallingPieceRotation / 2) == 0:
                        return(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol + 1)
                else:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
        elif(canvas.data.fallingPiece == zPiece2):
                if (canvas.data.fallingPieceRotation / 2) == 0:
                        return(canvas.data.fallingPieceRow, canvas.data.fallingPieceCol + 1)
                else:
                        return(canvas.data.fallingPieceRow + 1, canvas.data.fallingPieceCol + 1)
#Falling Piece Center    

def rotateFallingPiece():
        fallingPiece = canvas.data.fallingPiece
        oldRows = len(fallingPiece)
        oldCols = len(fallingPiece[0])
        newRows = oldCols
        newCols = oldRows
        rotatedFallingPiece = [([True] * newCols) for i in xrange(newRows)]
        for row in xrange(oldRows-1,-1,-1): 
                for col in xrange(oldCols):
                        rotatedFallingPiece[col][oldRows-1-row] = fallingPiece[row][col]
                        #To change direction in which pieces rotate (ccw vs. cw): 
                        #(1) Change oldRows-1,-1,-1 to oldRows
                        #(2) Change oldCols to oldCols-1,-1,-1             
                        #(3) change [col][oldRows-1-row] to [oldCols-1-col][row] 
        (oldCenterRow,oldCenterCol) = fallingPieceCenter()
        canvas.data.fallingPiece = rotatedFallingPiece
        (newCenterRow,newCenterCol) = fallingPieceCenter()
        fallingPieceRow = canvas.data.fallingPieceRow
        fallingPieceCol = canvas.data.fallingPieceCol
        canvas.data.fallingPieceRow += (oldCenterRow - newCenterRow)
        canvas.data.fallingPieceCol += (oldCenterCol - newCenterCol)
        canvas.data.fallingPieceRotation = (canvas.data.fallingPieceRotation + 1) % 4
        if (fallingPieceIsLegal() == False):
                canvas.data.fallingPiece = fallingPiece
                canvas.data.fallingPieceRow = fallingPieceRow
                canvas.data.fallingPieceCol = fallingPieceCol

def dropPiece():
        canvas.data.spacePressed = True
        canvas.after_cancel(canvas.data.timerId)
        movePossible = True
        while(movePossible == True):
                drow = 1
                dcol = 0
                canvas.data.score += 4
                movePossible = moveFallingPiece(drow,dcol)
                if(movePossible == True):
                        canvas.data.Moved += 1
        canvas.data.spacePressed = False
        timerFired()

def holdPiece():
        if(canvas.data.canHold == True):
                if (canvas.data.heldPiece == None):
                        canvas.data.heldPiece = canvas.data.fallingPiece
                        canvas.data.heldPieceColor = canvas.data.fallingPieceColor
                        newNextPiece()
                        newFallingPiece()
                else:
                        tempPiece = canvas.data.fallingPiece
                        tempColor = canvas.data.fallingPieceColor
                        canvas.data.fallingPiece = canvas.data.heldPiece
                        canvas.data.fallingPieceColor = canvas.data.heldPieceColor
                        canvas.data.fallingPieceRow = 0
                        canvas.data.fallingPieceCol = canvas.data.cols/2
                        canvas.data.fallingPieceCol -= canvas.data.fallingPieceCol/2
                        canvas.data.heldPiece = tempPiece
                        canvas.data.heldPieceColor = tempColor
                canvas.data.canHold = False #can only use hold once per piece

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

# clear rows 
def removeFullRows():
        rows = canvas.data.rows
        newRow = rows-1
        fullRowCount = 0
        for oldRow in xrange(rows-1,-1,-1):
                if(canvas.data.board[oldRow].count(canvas.data.emptyColor) != 0):
                        copyRow(oldRow,newRow)
                        newRow -= 1
                else:
                        fullRowCount += 1
        for fillRow in xrange(newRow,-1,-1):
                for element in xrange(len(canvas.data.board[0])):
                        canvas.data.board[fillRow][element] = canvas.data.emptyColor
                        
        if fullRowCount != 0:
                canvas.data.score += int(fullRowCount**2)*100    
                canvas.data.connection.sendDict({"lines":fullRowCount}) #Sends the dict as a JSON string to the server

def addManyJunkRows(rows):
        for i in xrange(rows):
                addJunkRow()
        
def addJunkRow():
        # first check if we have been KO'd
        topRowEmpty = True
        for c in xrange(canvas.data.cols):
            if canvas.data.board[0][c] != canvas.data.emptyColor:
                canvas.data.isGameOver = True
                return   

        newJunkRow = (["pink"] * canvas.data.cols)
        newJunkRow[random.randint(0, canvas.data.cols-1)] = canvas.data.emptyColor
        canvas.data.board.pop(0)
        canvas.data.board.append(newJunkRow)

#remakes the game at it current position evertime it is redrawn
def drawGame():
        canvas.create_rectangle(0,0,canvas.data.cols*20 + 140,canvas.data.rows*20
                                                        + 40, fill = "black")
        drawBoard()
        drawShadow()
        drawFallingPiece()

#draw the imaginary piece where a drop would place current falling piece
def drawShadow():
        if(not canvas.data.isGameOver):
                #determine where the shadow piece should go
                canvas.data.shadowPiece = canvas.data.fallingPiece
                canvas.data.shadowPieceRow = canvas.data.fallingPieceRow
                canvas.data.shadowPieceCol = canvas.data.fallingPieceCol
                while(shadowPieceIsLegal() == True):
                        canvas.data.shadowPieceRow += 1
                canvas.data.shadowPieceRow -= 1
                #draw it
                for row in xrange(len(canvas.data.shadowPiece)):
                        for col in xrange(len(canvas.data.shadowPiece[0])):
                                if (canvas.data.shadowPiece[row][col] == True):
                                        drawCell(20+(canvas.data.shadowPieceCol+col)*20,
                                                         20+(canvas.data.shadowPieceRow+row)*20,
                                                         canvas.data.shadowPieceColor)

def drawScore():
        canvas.create_text((canvas.data.cols*22)/2, 10, text = "SCORE = %d" %(canvas.data.score), fill = "white", font = "Courier 16 bold")
        
def drawHeld():
        canvas.create_text((canvas.data.cols*28), 340,
                                                text = "Held Piece:",
                                                fill = "white", font = "Courier 16 bold")
        if(canvas.data.heldPiece != None):
                for row in xrange(len(canvas.data.heldPiece)):
                        for col in xrange(len(canvas.data.heldPiece[0])):
                                if (canvas.data.heldPiece[row][col] == True):
                                        drawCell(30+(canvas.data.cols+col)*20,
                                                         360+(row)*20,
                                                         canvas.data.heldPieceColor)
                                        
def drawNext():
        canvas.create_text((canvas.data.cols*28), 40,
                                                text = "Next Piece:",
                                                fill = "white", font = "Courier 16 bold")
        if(canvas.data.nextPiece != None):
                for row in xrange(len(canvas.data.nextPiece)):
                        for col in xrange(len(canvas.data.nextPiece[0])):
                                if (canvas.data.nextPiece[row][col] == True):
                                        drawCell(30+(canvas.data.cols+col)*20,
                                                         60+(row)*20,
                                                         canvas.data.nextPieceColor)

#initiates the moving and rotation of the falling piece 
def keyPressed(event):
        if(not canvas.data.isGameOver and not canvas.data.spacePressed):
                drow = 0
                dcol = 0
                if(event.keysym == "Left"):
                        dcol = -1
                        moveFallingPiece(drow,dcol)
                elif(event.keysym == "Right"):
                        dcol = 1
                        moveFallingPiece(drow,dcol)
                elif(event.keysym == "Down"):
                        if canvas.data.delay == standardDelay :
                                canvas.data.delay = 60
                                canvas.after_cancel(canvas.data.timerId)
                                timerFired()
                elif(event.keysym == "Up"):
                        rotateFallingPiece()
                elif(event.keysym == "space"):
                        dropPiece()
                elif(event.keysym == "Shift_L" or event.keysym == "Shift_R"
                         or event.keysym == "z" or event.keycode == 131074
                         or event.keycode == 131076):
                        holdPiece()
                redrawAll()
        if(event.char == "r"):
                restart()
                
def keyReleased(event):
        if(event.keysym == "Down"):
                canvas.data.delay = standardDelay

def timerFired():
        if(canvas.data.isGameOver == False):
                movePossible = moveFallingPiece(1, 0)
                if(movePossible == True):
                        canvas.data.score += 1
                        canvas.data.Moved = True
                else:
                        if(not canvas.data.Moved):
                                canvas.data.isGameOver = True
                        placeFallingPiece()
                        newFallingPiece()
                        newNextPiece()
                        canvas.data.canHold = True
                        canvas.data.landed = False
                        canvas.data.Moved = False
                redrawAll()
        canvas.data.timerId = canvas.after(canvas.data.delay, timerFired)
        
        
        # NETWORK CONNECTIONS
        for i in canvas.data.connection._receivedMessages:  
                if jsonutils.isJSON(i):
                        d = jsonutils.jsonToDict(i)
                        if "lines" in d:
                                numLines = d["lines"]    
                                addManyJunkRows(numLines)    
                canvas.data.connection._receivedMessages.remove(i)

def redrawAll():
        canvas.delete(ALL)
        drawGame()
        drawScore()
        drawHeld()
        drawNext()

# to create the root and canvas
def run(room_name):
        rows = 20
        cols = 10
        global canvas
        root = Tk()
        canvas = Canvas(root, width = cols*20 + 140, height = rows*20 + 40)
        canvas.pack()
        root.resizable(width = 0, height = 0)
        root.canvas = canvas.canvas = canvas
        class Struct: pass
        canvas.data = Struct()
        canvas.data.connection = messenger.ClientConnect(iputils.wordsToIP(room_name))
        canvas.data.rows = rows
        canvas.data.cols = cols
        init()
        redrawAll()
        root.bind("<KeyPress>", keyPressed)
        root.bind("<KeyRelease>", keyReleased)
        root.mainloop()
