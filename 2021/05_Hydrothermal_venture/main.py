#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Read all the lines in the input
horizontalLines = []
verticalLines = []
diagonalLines = []
maxX = 0
maxY = 0
with open("input.txt", "r") as f:
    for line in f:
        coordinates = [ int(coord) for coord in
                        re.findall(r"([\d]+),([\d]+)\s->\s([\d]+),([\d]+)", line)[0] ]

        # Check if the line is horizontal
        if coordinates[1] == coordinates[3]:
            horizontalLines.append( [ [ coordinates[0], coordinates[1] ],
                                      [ coordinates[2], coordinates[3] ] ] )

        # Check if the line is vertical
        elif coordinates[0] == coordinates[2]:
            verticalLines.append( [ [ coordinates[0], coordinates[1] ],
                                    [ coordinates[2], coordinates[3] ] ] )

        # Otherwise, the line is horizontal
        else:
            # Check if it is 45 degrees
            if abs( (coordinates[0] - coordinates[2]) / (coordinates[1] - coordinates[3]) ) == 1:
                diagonalLines.append( [ [ coordinates[0], coordinates[1] ],
                                        [ coordinates[2], coordinates[3] ] ] )

        # Update the maximum values of the coordinates
        if coordinates[0] > maxX:
            maxX = coordinates[0]
        if coordinates[2] > maxX:
            maxX = coordinates[2]
        if coordinates[1] > maxY:
            maxY = coordinates[1]
        if coordinates[3] > maxY:
            maxY = coordinates[3]

# Initialize the map
# diagram = np.zeros( ( maxY, maxX ) )
diagram = [ [ 0 ] * (maxX + 1) for i in range(maxY + 1) ]

# Add the horizontal lines
for line in horizontalLines:
    # Get the minimum and maximum values of X
    minX = min(line[0][0], line[1][0])
    maxX = max(line[0][0], line[1][0])
    # Mark all points in the line
    for x in range(minX, maxX + 1):
        diagram[line[0][1]][x] += 1

# Add the vertical lines
for line in verticalLines:
    # Get the minimum and maximum values of Y
    minY = min(line[0][1], line[1][1])
    maxY = max(line[0][1], line[1][1])
    # Mark all points in the line
    for y in range(minY, maxY + 1):
        diagram[y][line[0][0]] += 1

# Add the diagonal lines
for line in diagonalLines:
    # Get the minimum and maximum values of X
    minX = min(line[0][0], line[1][0])
    maxX = max(line[0][0], line[1][0])
    # Compute the slope
    slope = ( (line[1][1] - line[0][1]) / (line[1][0] - line[0][0]) )
    # Mark all points in the line
    for x in range(minX, maxX + 1):
        y = int( line[0][1] + slope * ( x - line[0][0] ) )
        diagram[y][x] += 1

# Count the number of points where at least two lines overlap
overlapCount = 0
for y in range(len(diagram)):
    for x in range(len(diagram)):
        if diagram[y][x] >= 2:
            overlapCount += 1

print("Number of points where at least two lines overlap: {}".format(overlapCount))

