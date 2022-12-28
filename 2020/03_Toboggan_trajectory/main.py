#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Function to convert a line of the map to a list of 0 (no tree) or 1 (tree)
def readMapLine(string):
    result = [0] * ( len(string) - 1 )
    for i in range(len(result)):
        # Check if the current character of the string corresponds to a tree
        if string[i] == "#":
            result[i] = 1

    return result

# Read the map
treeMap = []
with open("input.txt", "r") as f:
    for line in f:
        # Read this line as a series of zeroes and ones, and append it to the 
        # map
        treeMap.append( readMapLine(line) )

# Function to compute the number of trees encountered with a given slope
def countTreesSlope(dx, dy):
# Start at the top left
    x = 0
    y = 0
    treeCount = 0
    while y < len(treeMap):
        # Check if there is a tree at the current position
        if treeMap[y][x] == 1:
            treeCount += 1
        # Move 3 to the right, cyclicly
        x = (x + dx) % len(treeMap[0])
        # Move 1 down
        y += dy

    return treeCount

# Compute the number of trees encountered in the trajectory:
#   right 3, down 1
treeCount = countTreesSlope(3, 1)

print("Trees encountered: {}".format(treeCount))
print("\n----------\n")

# Transverse the map in different slopes
slopes = [ [ 1, 1 ], [ 3, 1 ], [ 5, 1 ], [ 7, 1 ], [ 1, 2 ] ]
treeCounts = [ countTreesSlope(dx, dy) for (dx, dy) in slopes ]

# Multiply the counts together
productTreeCounts = 1
for count in treeCounts:
    productTreeCounts *= count

print("Product of trees encountered: {}".format(productTreeCounts))


