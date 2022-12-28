#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Function to read the seat from a string of input
def readSeat(string):
    # Read the row from the first seven characters
    row = 0
    for i in range(7):
        if string[i] == "B":
            row += 2 ** (6 - i)

    # Read the column
    column = 0
    for i in range(3):
        if string[7 + i] == "R":
            column += 2 ** (2 - i)

    return (row, column)

# Read the entries in the file
seatIDs = []
with open("input.txt", "r") as f:
    for line in f:
        # Get the row and column of the current sead
        (row, column) = readSeat(line)
        # Compute the seat ID
        seatIDs.append( row * 8 + column )

# Sort the seat IDs
seatIDs.sort()

# Get the largest seat ID
# Since the list is sorted, this is simply the last one
largestID = seatIDs[-1]

print("Largest seat ID: {}".format(largestID))
print("\n----------\n")

# Find your seat
mySeat = 0
for i in range(1, len(seatIDs) - 1):
    if seatIDs[i + 1] != seatIDs[i] + 1:
        mySeat = seatIDs[i] + 1
        # Check that the next seat is indeed the corresponding one
        assert( seatIDs[i + 1] == mySeat + 1 )

print("My seat: {}".format(mySeat))
