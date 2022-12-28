#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import itertools as it
import numpy as np

def changeDirectionAnticlock(direc, angle):
    rotation = []
    # newDir = direc[:]
    newDir = direc.copy()

    # Get the rotation matrix depending on the angle
    # Notice that the angles are clockwise!
    if angle == 90:
        rotation = ( ( 0, -1 ), ( 1, 0 ) )
    elif angle == 180:
        rotation = ( ( -1, 0 ), ( 0, -1 ) )
    elif angle == 270:
        rotation = ( ( 0, 1 ), ( -1, 0 ) )
    else:
        print("Angle unknown")

    # Change the direction
    newDir[0] = rotation[0][0] * direc[0] + rotation[0][1] * direc[1]
    newDir[1] = rotation[1][0] * direc[0] + rotation[1][1] * direc[1]

    return newDir

# Read the instructions
instructions = []
with open("input.txt", "r") as f:
    for line in f:
        instruction = [ (instr[0], int(instr[1])) for instr in re.findall(r"([A-Z])([\d]+)", line) ][0]
        instructions.append(instruction)

# Position and direction of the ship
position = np.array( [ 0, 0 ] )
direction = np.array( [ 1, 0 ] ) # Start facing east

# Move the ship according to the instructions
for instr in instructions:
    # Move in any of the 4 directions
    if instr[0] == "N":
        position[1] += instr[1]
    elif instr[0] == "S":
        position[1] -= instr[1]
    elif instr[0] == "E":
        position[0] += instr[1]
    elif instr[0] == "W":
        position[0] -= instr[1]

    # Move forward
    elif instr[0] == "F":
        position += instr[1] * direction
        # position[0] += instr[1] * direction[0]
        # position[1] += instr[1] * direction[1]

    # Rotate the ship
    elif instr[0] == "R":
        direction = changeDirectionAnticlock(direction, 360 - instr[1])
    elif instr[0] == "L":
        direction = changeDirectionAnticlock(direction, instr[1])

    else:
        print("Unknown instruction.")

# Compute the Manhattan distance
manhattanDistance = sum(abs(position))

print("Manhattan distance: {}".format(manhattanDistance))
print("\n----------\n")

# Move the ship with the waypoint
shipPosition = np.array( [ 0, 0 ] )
# Position of the waypoint with respect to the ship
waypointPosition = np.array( [ 10, 1 ] )

# Move the waypoint and the ship according to the instructions
for instr in instructions:
    # Move in any of the 4 directions
    if instr[0] == "N":
        waypointPosition[1] += instr[1]
    elif instr[0] == "S":
        waypointPosition[1] -= instr[1]
    elif instr[0] == "E":
        waypointPosition[0] += instr[1]
    elif instr[0] == "W":
        waypointPosition[0] -= instr[1]

    # Rotate the ship
    elif instr[0] == "R":
        # direction = changeDirectionAnticlock(direction, 360 - instr[1])
        waypointPosition = changeDirectionAnticlock(waypointPosition, 360 - instr[1])
    elif instr[0] == "L":
        # direction = changeDirectionAnticlock(direction, instr[1])
        waypointPosition = changeDirectionAnticlock(waypointPosition, instr[1])

    # Move the ship towards the waypoint, and the waypoint also in that direction
    elif instr[0] == "F":
        # Get the direction from the ship to the waypoint, normalized
        # direction = waypointPosition
        # direction /= np.sqrt(np.sum(direction**2))
        # print(np.sqrt(np.sum(direction**2)))
        # print(direction)
        # Move the ship and the waypoint in that direction
        shipPosition += instr[1] * waypointPosition
        # waypointPosition += instr[1] * direction

    else:
        print("Unknown instruction.")

# Compute the Manhattan distance
# manhattanDistance = abs(position[0]) + abs(position[1])
manhattanDistance = sum(abs(shipPosition))

print("Manhattan distance: {}".format(manhattanDistance))
