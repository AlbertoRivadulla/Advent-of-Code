#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Function to convert the grid of dots to a string
def dotsToString(dots):
    # Get the maximum values of x and y
    maxx = 0
    maxy = 0
    for dot in dots:
        if dot[0] > maxx:
            maxx = dot[0]
        if dot[1] > maxy:
            maxy = dot[1]
    # Add one to each, to have the correct bounds in the lists
    maxx += 1
    maxy += 1

    # Initialize a grid of zeroes
    grid = [ [ 0 ] * maxx for _ in range(maxy) ]
    # Add the dots to the grid
    for dot in dots:
        grid[dot[1]][dot[0]] = 1

    # Convert the grid to a string
    string = ""
    for line in grid:
        for element in line:
            if element == 1:
                string += "#"
            else:
                string += "."
        string += "\n"

    return string

# Function to fold the grid of dots
def foldGrid(dots, instruction):
    # Check if we are folding vertically or horizontally.
    # By defauld, we fold in the x index
    indexFold = 0
    if instruction[0] == "y":
        indexFold = 1

    # Transform each point
    for dot in dots:
        # Check if the dot is located after the folding line
        if dot[indexFold] > instruction[1]:
            dot[indexFold] = 2 * instruction[1] - dot[indexFold]

    return dots

# Function to cound the visible dots
def countDots(dots):
    # Get the dots as a string
    string = dotsToString(dots)

    # Count the amound of dots that are visible
    visibleDots = 0
    for char in string:
        if char == "#":
            visibleDots += 1

    return visibleDots

# Read the dots and fold instructions
dots = []
foldInstructions = []
with open("input.txt", "r") as f:
    for line in f:
        # Read a dot
        dot = re.findall(r"([\d]+),([\d]+)", line)
        if len(dot) != 0:
            dots.append( [ int(dot[0][0]), int(dot[0][1]) ] )
        # Check if it is a fold instruction
        instruction = re.findall(r"^fold along ([xy])=([\d]+)$", line)
        if len(instruction) != 0:
            foldInstructions.append( [ instruction[0][0], int(instruction[0][1]) ] )

# Fold the grid of dots following each instruction
for instruction in foldInstructions[:]:
    dots = foldGrid(dots, instruction)

# Print the final grid of dots
print(dotsToString(dots))

print("Visible dots: {}".format(countDots(dots)))
print("\n----------------\n")
