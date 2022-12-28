#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Read the positions of the crabs
positions = []
with open("input.txt", "r") as f:
    positions = [ int(position) for position in re.findall(r"([\d]+)", f.readline()) ]

# Find the maximum position
maximumPos = 0
for pos in positions:
    if pos > maximumPos:
        maximumPos = pos

# Find the position that requires minimum fuel spent
positionMinimumFuel = 0
minimumFuel = 0
for thisPosition in range(maximumPos):
    # Compute the amount of fuel spent to get to this position
    thisFuel = 0
    for pos in positions:
        thisFuel += abs( pos - thisPosition )

    # Compare it with the minimum
    if minimumFuel == 0 or minimumFuel > thisFuel:
        minimumFuel = thisFuel
        positionMinimumFuel = thisPosition
    # elif minimumFuel > thisFuel:
    #     minimumFuel = thisFuel
    #     positionMinimumFuel = thisPosition

print("Position that requires the mimimum fuel: {}".format(positionMinimumFuel))
print("Minimum amount of fuel spent: {}".format(minimumFuel))
print("\n----------------\n")

# Find the position that requires minimum fuel spent, with an arithmetic sum
positionMinimumFuel = 0
minimumFuel = 0
for thisPosition in range(maximumPos):
    # Compute the amount of fuel spent to get to this position
    thisFuel = 0
    for pos in positions:
        # thisFuel += abs( pos - thisPosition )
        n = abs( pos - thisPosition )
        thisFuel += n * ( n + 1 ) / 2

    # Compare it with the minimum
    if minimumFuel == 0 or minimumFuel > thisFuel:
        minimumFuel = thisFuel
        positionMinimumFuel = thisPosition

print("Fuel spent follows the arithmetic sum formula:")
print("Position that requires the mimimum fuel: {}".format(positionMinimumFuel))
print("Minimum amount of fuel spent: {}".format(minimumFuel))
