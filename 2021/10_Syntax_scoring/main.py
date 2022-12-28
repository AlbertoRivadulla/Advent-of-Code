#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

charClosingToOpening = { ")": "(",
                         "]": "[",
                         "}": "{",
                         ">": "<" }

charOpeningToClosing = { v: k for k, v in charClosingToOpening.items() }

closingChars = ( ")", "]", "}", ">" )

corruptCharScores = { ")": 3,
                      "]": 57,
                      "}": 1197,
                      ">": 25137 }

incompleteCharScores = { ")": 1,
                         "]": 2,
                         "}": 3,
                         ">": 4 }

def computeCorruptedCodeScore(code):
    # Create a list to use as a stack for the characters in the code
    stackOpening = [ code[0] ]

    # Read the different characters in the code
    for char in code[1:]:
        # Check if the character is one of the closing characters
        if char in closingChars:
            # Check if the character coincides with the last character in the stack
            if charClosingToOpening[char] == stackOpening[-1]:
                # If it coincides remove it from the stack, as this pair is closed
                stackOpening.pop()
            # Othewise, the pair is corrupt, so return the score of the corresponging char
            else:
                return corruptCharScores[char], stackOpening

        # Otherwise it is an opening character, so add it to the stack
        else:
            stackOpening.append(char)

    # If ths stack is empty, the code is correct. Return zero
    return 0, stackOpening

def computeIncompleteScore(stackOpening):
    # Initialize the score
    score = 0
    for charOpening in stackOpening[::-1]:
        # Get the closing char
        closingChar = charOpeningToClosing[charOpening]

        # Multiply the score by 5
        score *= 5
        # Add the score corresponding to the closing char
        score += incompleteCharScores[closingChar]

    return score

# Read the codes in the file
scoreCorrupted = 0
scoresIncomplete = []
with open("input.txt", "r") as f:
    for line in f:
        # Compute the score of the current code
        score, stackOpening = computeCorruptedCodeScore(line.strip())
        scoreCorrupted += score

        # If the score is 0, the code is incomplete. So complete it
        if score == 0:
            thisScore = computeIncompleteScore(stackOpening)
            scoresIncomplete.append(thisScore)

# Sort the scores of the incomplete lines
scoresIncomplete.sort()
# Take the element in the middle
scoreIncomplete = scoresIncomplete[ len(scoresIncomplete) // 2 ]

print("Score of the corrupted lines: {}".format(scoreCorrupted))
print("\n----------------\n")
print("Score of the incomplete lines: {}".format(scoreIncomplete))
