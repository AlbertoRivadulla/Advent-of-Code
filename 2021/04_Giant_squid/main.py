#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Numbers drawn
drawnNumbers = []
# Boards
boards = []
# Marks on boards
boardMarks = []

# Read the file
with open("input.txt", "r") as f:
    # Read the first line for the numbers drawn
    line = f.readline()
    drawnNumbers = [ int(nr) for nr in re.findall(r"(\d+),", line) ]

    # Read the boards
    thisBoard = []
    lineCount = 0
    for line in f:
        # If the line is empty, continue
        if line == "\n":
            continue
        # Add this line to the current board
        thisBoard.append( [ int(nr) for nr in re.findall(r"(\d+)\s", line) ] )
        lineCount += 1

        # Every 5 lines, the board is complete, so save it in the list of boards
        # and restart it
        if lineCount == 5:
            lineCount = 0
            boards.append( np.array( thisBoard ) )
            boardMarks.append( np.zeros( ( 5, 5 ), dtype=int ) )
            # boardMarks.append( np.zeros( ( 5, 5 ), dtype=bool ) )
            thisBoard = []

def checkNumberBoard(number, board, boardMark):
    # Find the indices of the number in the board
    indices = np.where(board == number)
    # Check if this list of indices is not empty
    if indices[0].size == 1:
        # Mark the boardMark
        boardMark[indices[0][0], indices[1][0]] = 1
        return

def checkBoardWon(boardMark):
    # Sum the marks in both directions
    sumAxis0 = np.sum(boardMark, axis = 0)
    sumAxis1 = np.sum(boardMark, axis = 1)

    # If any of the sums evaluate to 5, the board won
    if (5 in sumAxis0) or (5 in sumAxis1):
        return True

    # Otherwise, the board didn't win
    return False

# Iterate through the drawn numbers, until one board wins
# Index of the winning board
winner = -1
winnerNumber = 0
# Array to know whether a board has already been completed
completedMask = np.zeros( ( len(boards) ), dtype = bool )
# Index of the last board to win
last = -1
lastNumber = 0
for number in drawnNumbers:
    # Iterate through the boards
    for i in range(len(boards)):
        # Check if the number is in the board, if it has not won yet
        if not completedMask[i]:
            checkNumberBoard(number, boards[i], boardMarks[i])
        # Check if the current board has won
        if checkBoardWon(boardMarks[i]):
            # If this is the first board to win, save its index
            if np.sum(completedMask) == 0:
                winner = i
                winnerNumber = number
            # If this is the last board to be completed, save it
            if np.sum(completedMask) == len(boards) - 1:
                last = i
                lastNumber = number
            # print(np.sum(completedMask))
            # print(i)
            # print()
            # Mark this board as completed
            completedMask[i] = True
    # Check if all boards have been completed
    if np.sum(completedMask) == len(boards):
        break

def computeScore(number, board, boardMark):
    # Find the sum of all unmarked numbers in the board
    score = number * np.sum( board[boardMark == 0] )

    return score

# Compute the score of the winning board
winningScore = computeScore(winnerNumber, boards[winner], boardMarks[winner])

print("Score of the winning board: {}".format(winningScore))
print("\n-------------\n")

# Compute the score of the last board
lastScore = computeScore(lastNumber, boards[last], boardMarks[last])

print("Score of the last board: {}".format(lastScore))
