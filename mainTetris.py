#################################################
# hw6.py: Tetris!
#
# Your name: Vishesh Pagarani
# Your andrew id: vpagaran
#
# Your partner's name: Joesph Pinon
# Your partner's andrew id: jgpinon
#################################################

import cs112_s20_unit6_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################
#Function will return the game dimensions of the grid. Is mutuable.
def gameDimensions():
    rows, cols, cellSize, margin = 15, 10, 20, 25
    return (rows, cols, cellSize, margin)

#This function will initialize the game 
def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (cols*cellSize) + (2*margin)
    height = (rows*cellSize) + (2*margin)
    runApp(width=width, height=height)

#Class of 'app' will store attributes of the game tetris 
def appStarted(app):
    (rows, cols, cellSize, margin) = gameDimensions()
    app.cols = cols 
    app.rows = rows
    app.cellSize = cellSize 
    app.margin = margin 
    app.emptyColor = "blue"
    app.board = []    #Creates a 2d list of the emptycolor
    for row in range(app.rows):
        rowList = []
        for col in range(app.cols):
            rowList.append(app.emptyColor)
        app.board.append(rowList)
    
    #This below cases test that the list constructed is a 2D list

    # app.board[0][0] = "red" # top-left is red
    # app.board[0][app.cols-1] = "white" # top-right is white
    # app.board[app.rows-1][0] = "green" # bottom-left is green
    # app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray

    #Adding in the piece shapes and pieces color 
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    app.fallingPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece,zPiece]
    app.tetrisPieceColors = ["red","yellow","magenta","pink",
    "cyan","green","orange"]
    app.changePiece = False  #Boolean value; allows shape to be changed
    newFallingPiece(app) #initializes 4 variables from newFallingPiece function
    app.isGameOver = False 
    app.message = "GAME OVER!!"
    app.score = 0
    app.fullRows = 0
    app.isPaused = False 
    app.isBonusMode = False 
    app.timerDelay = 500
   
#This function will greate a cell, given the row 
def drawCell(app, canvas, row, col, color):
    x1 = app.margin + (col*app.cellSize)
    y1 = app.margin + (row*app.cellSize)
    canvas.create_rectangle(x1, y1, x1+app.cellSize, y1+app.cellSize,
    fill=color)

#Function will call draw cell while looping to create a grid   
def drawBoard(app, canvas):
    (rows, cols, cellSize, margin) = gameDimensions()
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

#This will change the shape and color is space is pressed
def keyPressed(app, event):
    if event.key == "r": 
        appStarted(app)
    elif app.isGameOver == True :
        return
    elif event.key == "Left":
        if app.isPaused != True:
             moveFallingPiece(app, 0, -1)
    elif event.key == "Right": 
        if app.isPaused != True:
            moveFallingPiece(app, 0, 1)
    # elif event.key == "Down": moveFallingPiece(app, 1, 0)
    elif event.key == "Up": 
        if app.isPaused != True:
            rotateFallingPiece(app)
    elif event.key == "Space":  #to allow harddrop. Reset back to normal when
        app.timerDelay = 0    #new fallingpiece is called
    elif event.key == "p":
        app.isPaused = not app.isPaused 
    
#This function will place the falling piece
def placeFallingPiece(app):
    for row in range(len(app.tetrisShape)):
        for col in range(len(app.tetrisShape[0])):
            if app.tetrisShape[row][col] == True: 
                startRow = app.startRow + row
                startCol = app.startCol + col
                app.board[startRow][startCol] = app.fill
                removeFullRows(app)

#This function will move the falling picece accordance to time 
def timerFired(app):
    if app.isGameOver == True:
        return 
    if (not app.isPaused):
        doStep(app)
    
def doStep(app):
    moveFallingPiece(app, 1, 0)
    if moveFallingPiece(app, 1, 0) == False:
        placeFallingPiece(app)
        newFallingPiece(app)
        if fallingPiecelsLegal(app) == False:
            app.isGameOver = True
        else:
            app.timerDelay = 250
        
#Given a row, will return the startx, starty of the cell
def getCellBounds(app, row, col):
    x0 = app.margin + (col*app.cellSize)
    x1 = x0 + app.cellSize
    y0 = app.margin + (row*app.cellSize)
    y1 = y0 + app.cellSize
    return x0,y0,x1,y1

#is called in appStarted. Will initializes the fill, startrow, startcol, shape
def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.fallingPieces)-1)
    app.tetrisShape = app.fallingPieces[randomIndex]
    app.fill = app.tetrisPieceColors[randomIndex]
    app.startRow = 0
    x = (app.width-(2*app.margin))/2  #This is to get the xcoord of the row
    app.startCol = int((x)/app.cellSize)-2 #Converts x coord to row num
    
#Function will draw the randomly choosen falling piece
def drawFallingPiece(app, canvas):
    for row in range(len(app.tetrisShape)):
        for col in range(len(app.tetrisShape[row])):
            if app.tetrisShape[row][col] == True: #StartX positions shape
                startRow = app.startRow + row #row would be 0,1,2 since in list
                startCol = app.startCol + col #same case for col
                drawCell(app, canvas, startRow, startCol, app.fill)

#This function will be called by keyPressed to move block
def moveFallingPiece(app, drow, dcol):
    app.startRow += drow
    app.startCol += dcol
    if fallingPiecelsLegal(app)== False: 
        app.startRow -= drow
        app.startCol -= dcol
        return False 
    else: return True 

#This function checks if the move, rotation we made is legal
def fallingPiecelsLegal(app):
    for row in range(len(app.tetrisShape)):
        for col in range(len(app.tetrisShape[0])):
            if app.tetrisShape[row][col] == True:
                startCol = app.startCol + col
                startRow = app.startRow + row
                if app.startRow+len(app.tetrisShape)> app.rows: return False 
                elif startCol<0: return False 
                elif app.startCol+len(app.tetrisShape[0])>app.cols:return False
                elif app.board[startRow][startCol] != app.emptyColor: 
                    return False
    return True 

#This function will rotate the fallingpiece around center axis    
def rotateFallingPiece(app): #len of rows, cols inverse w new shape
    numOldRows, numOldCols = len(app.tetrisShape), len(app.tetrisShape[0])
    numNewCols, numNewRows = numOldRows, numOldCols 
    oldFallingPieces = app.tetrisShape
    newFallingPiece = [[None]*numNewCols for row in range(numNewRows)] 
    for row in range(len(oldFallingPieces)):
        for col in range(len(oldFallingPieces[0])):
            newCol = row 
            newRow = (len(oldFallingPieces[0])-1)-col
            newFallingPiece[newRow][newCol] = app.tetrisShape[row][col]
    
    oldCenterRow, oldCenterCol = (numOldRows//2), (numOldCols//2)
    newRowPos= oldCenterRow - (numNewRows//2)
    newColPos = oldCenterCol - (numNewCols//2)
    
    app.startRow += newRowPos  #This makes sure row, col rotates rnd center
    app.startCol += newColPos

    app.tetrisShape = newFallingPiece 
    if fallingPiecelsLegal(app) == False: #Checks if rotation is legal
        app.tetrisShape = oldFallingPieces
        app.startRow -= newRowPos
        app.startCol -= newColPos

#This function would remove an entire row if it is filled            
def removeFullRows(app):
    newBoard = []
    count = 0
    for row in range(len(app.board)):
        tempList = []
        for col in range(len(app.board[0])):
            tempList.append(app.board[row][col])
        if app.emptyColor in tempList:
            newBoard.append(tempList)
        else:
            count += 1
            app.fullRows += 1
            if count >1:
                app.score += (app.fullRows)**2
            else:
                app.score += 1
    #To replace the empty rows now on top  
    if count>0:
        emptyColorList = []
        for row in range(count):
            for col in range(len(app.board[0])):
                emptyColorList.append(app.emptyColor)
        newBoard.insert(0, emptyColorList)
        app.board = newBoard

#This function is called in redrawAll to draw the score         
def drawScore(app, canvas):
    canvas.create_text(app.width/2, 15, text = f'Score: {app.score}', 
    font = "Arial 10 bold", fill = "black")

#This function responds to app.isPaused. Will create text if pasued
def drawIsPaused(app, canvas):
    if app.isPaused == True:
        canvas.create_text(app.width/2, app.height/2, text = "Paused", 
        fill = "white", font = "Arial 15 bold")

#Redrawall will call all draw functions 
def redrawAll(app, canvas):
    width = (app.cols*app.cellSize) + (2*app.margin)
    height = (app.rows*app.cellSize) + (2*app.margin)
    canvas.create_rectangle(0,0,
    width, height, fill = "Orange")
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    if app.isGameOver == True:  #prints text is app.isGameOver activated 
        canvas.create_text(app.width/2, app.height/2, text = app.message,
        fill = "white", font = "Arial 27 bold")
    drawScore(app, canvas)
    drawIsPaused(app, canvas)
    canvas.create_text(app.width/2, app.height-14, text = "Press r to Restart", 
    font = "Arial 8 bold")


#################################################
# main
#################################################

def main():
    cs112_s20_unit6_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
