#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import itertools as it

# Read the pattern of seats
seats = []
with open("input.txt", "r") as f:
    for line in f:
        thisRow = []
        for char in line:
            # Empty seat
            if char == "L": 
                thisRow.append(1)
            # No seat
            elif char == ".":
                thisRow.append(0)
        seats.append(thisRow)

def updateSeats(seats):
    # Copy the seats
    copySeats = [ row[:] for row in seats ]

    # Iterate through the different seats
    for i in range(len(seats)):
        # Indices of the adjacent seats in the vertical direction
        indicesi = set( ( max(0, i - 1), i, min(i + 1, len(seats) - 1) ) )
        for j in range(len(seats[i])):
            # Check if there is actually a seat in that position
            if seats[i][j] != 0:
                # Indices of the adjacent seats in the horizontal direction
                indicesj = set( ( max(0, j - 1), j, min(j + 1, len(seats[i]) - 1) ) )

                # First rule
                # Check if the 8 adjacent seats and the current seat are all empty
                nrOccupied = sum( [ seats[i1][j1] == 2 for (i1, j1) in it.product(indicesi, indicesj) ] )
                # The seats becomes occupied
                if nrOccupied == 0:
                    copySeats[i][j] = 2

                # Second rule
                # If the seat is occupied
                if seats[i][j] == 2:
                    # If 4 or more of the adjacent seats are occupied
                    if nrOccupied - 1 >= 4:
                        # The seat becomes empty
                        copySeats[i][j] = 1

    return copySeats

# Iterate until the process stabilizes
iterationsCounter = 0
while True:
    newSeats = updateSeats(seats)
    if newSeats == seats:
        break
    seats = newSeats
    iterationsCounter += 1

# Count the occupied seats
occupiedSeats = 0
for row in seats:
    for seat in row:
        if seat == 2:
            occupiedSeats += 1

print("Total iterations: {}".format(iterationsCounter))
print("Occupied seats: {}".format(occupiedSeats))

print("\n----------\n")


# Read the pattern of seats
seats = []
with open("input.txt", "r") as f:
    for line in f:
        thisRow = []
        for char in line:
            # Empty seat
            if char == "L": 
                thisRow.append(1)
            # No seat
            elif char == ".":
                thisRow.append(0)
        seats.append(thisRow)

def getOccupiedAdjacentSeats(seats, i, j):
    # adjacentIndices = []
    nrOccupied = 0

    # Offsets in each direction
    offsets = ( -1, 0, 1 )

    # Find the next occupied seat in each direction
    for (ioff, joff) in it.product(offsets, offsets):
        # Move along the direction
        step = 1
        while True:
            thisi = i + step * ioff
            thisj = j + step * joff
            # Check if we are in bounds
            if thisi >= 0 and thisi < len(seats) and thisj >= 0 and thisj < len(seats[0]):
                # Check if we found a seat
                if seats[thisi][thisj] != 0:
                    # Check if the seat is occupied
                    if seats[thisi][thisj] == 2:
                        nrOccupied += 1
                    # Break the loop
                    break
                else:
                    # If there is no seat, add one to the step and repeat
                    step += 1

            else:
                # If we are out of bounts, stop
                break

    # return adjacentIndices
    return nrOccupied

def updateSeats2(seats):
    # Copy the seats
    copySeats = [ row[:] for row in seats ]

    # Iterate through the different seats
    for i in range(len(seats)):
        for j in range(len(seats[i])):
            # Check if there is actually a seat in that position
            if seats[i][j] != 0:
                # Count the occupied seats in the eight directions from the current one
                nrOccupied = getOccupiedAdjacentSeats(seats, i, j)

                # First rule
                # Check if the 8 adjacent seats and the current seat are all empty
                if nrOccupied == 0:
                    # The seats becomes occupied
                    copySeats[i][j] = 2

                # Second rule
                # If the seat is occupied
                if seats[i][j] == 2:
                    # If 5 or more of the adjacent seats are occupied
                    if nrOccupied - 1 >= 5:
                        # The seat becomes empty
                        copySeats[i][j] = 1

    return copySeats

# Iterate until the process stabilizes
iterationsCounter = 0
while True:
    newSeats = updateSeats2(seats)
    if newSeats == seats:
        break
    seats = newSeats
    iterationsCounter += 1

# Count the occupied seats
occupiedSeats = 0
for row in seats:
    for seat in row:
        if seat == 2:
            occupiedSeats += 1

print("Total iterations: {}".format(iterationsCounter))
print("Occupied seats: {}".format(occupiedSeats))
