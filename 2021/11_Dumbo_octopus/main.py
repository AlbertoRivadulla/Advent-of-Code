#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

def printMap(levels):
    print()
    for line in levels:
        print(line)
    print()

def findNeighbors(heightmap, point):
    # Create the tentative list of neighbors
    tentativeNeighbors = [ [ point[0] - 1, point[1] ],
                         [ point[0] - 1, point[1] - 1 ],
                         [ point[0], point[1] - 1 ],
                         [ point[0] + 1, point[1] - 1 ],
                         [ point[0] + 1, point[1] ],
                         [ point[0] + 1, point[1] + 1 ],
                         [ point[0], point[1] + 1 ],
                         [ point[0] - 1, point[1] + 1 ] ]

    # Return only the valid neighbors
    neighbors = []
    for neigh in tentativeNeighbors:
        if neigh[0] < 0 or neigh[0] >= len(heightmap):
            continue
        if neigh[1] < 0 or neigh[1] >= len(heightmap[0]):
            continue
        neighbors.append(tuple(neigh))

    return neighbors

def updateStep(levels):
    # Total number of flahes in the current step
    stepFlashes = 0

    octopusesToFlash = set()
    octopusesThatFlashed = set()

    # Iterate through all of the octopuses
    for i in range(len(levels)):
        for j in range(len(levels[0])):
            # Increase the energy level by one
            levels[i][j] += 1
            # If the energy level is larger than 9, it must flash
            if levels[i][j] > 9:
                octopusesToFlash.add( (i, j) )

    # Iterate until no octopus flashes
    while True:
        # printMap(levels)
        iterationFlashes = 0
        # Octopuses to flash in this iteration
        octopusesToFlashIteration = set()

        # Iterate through all the octopuses that must flash
        for octopus in octopusesToFlash:
            # Get the neighbors of the current octopus
            neighbors = findNeighbors(levels, octopus)
            # Add 1 to each of the neighbors
            for neigh in neighbors:
                if neigh not in octopusesToFlash and neigh not in octopusesThatFlashed:
                    levels[neigh[0]][neigh[1]] += 1
                # If any of the neighbors must flash, stage them
                if levels[neigh[0]][neigh[1]] > 9 and neigh not in octopusesThatFlashed and neigh not in octopusesToFlash:
                    octopusesToFlashIteration.add(neigh)

        # Flash all the octopus
        for octopus in octopusesToFlash:
            # Flash
            levels[octopus[0]][octopus[1]] = 0
            iterationFlashes += 1
            octopusesThatFlashed.add(octopus)

        # If no octopus flashed, break the loop
        if iterationFlashes == 0:
            break

        # Update the list of octopuses to flash
        octopusesToFlash = octopusesToFlashIteration

        # Add the amoung of flashes to the counter
        stepFlashes += iterationFlashes

    return stepFlashes

# Read the energy levels of the octopuses
energyLevels = []
with open("input.txt", "r") as f:
    for line in f:
        # Read the line as numbers
        thisLine = [ int(nr) for nr in line.strip() ]
        energyLevels.append(thisLine)

# Iterate a given number of steps
totalFlashes = 0
for _ in range(100):
    stepFlashes = 0
    # Perform the entire step, updating the energy levels until there are no flashes
    stepFlashes = updateStep(energyLevels)

    # Add the number of flashes in this step to the counter
    totalFlashes += stepFlashes

print("Total number of flashes: {}".format(totalFlashes))
print("\n----------------\n")

# Read the energy levels of the octopuses again
energyLevels = []
with open("input.txt", "r") as f:
    for line in f:
        # Read the line as numbers
        thisLine = [ int(nr) for nr in line.strip() ]
        energyLevels.append(thisLine)

# Find the step at which all octopuses flash simultaneously
allFlashStep = 0
thisStep = 0
while True:
    thisStep += 1

    # Perform the entire step, updating the energy levels until there are no flashes
    stepFlashes = updateStep(energyLevels)

    if stepFlashes == len(energyLevels) * len(energyLevels[0]):
        allFlashStep = thisStep
        break

print("Step at which all octopuses flash simultaneously: {}".format(allFlashStep))
