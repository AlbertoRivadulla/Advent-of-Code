#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

def step(fishes):
    # List of new fishes
    newFishes = 0
    # Iterate over all the fishes
    for i in range(len(fishes)):
        # If the timer is zero, produce a new fish
        if fishes[i] == 0:
            newFishes += 1
            fishes[i] = 6
            continue
        # Reduce the timer in one unit
        fishes[i] -= 1

    # Add the new fishes to the list
    for i in range(newFishes):
        fishes.append(8)


# Read the list of fishes the first day
fishes = []
with open("input.txt", "r") as f:
    fishes = [ int(fish) for fish in re.findall(r"([\d]+)", f.readline()) ]

# Evolve 80 days
nDays = 80
for i in range(nDays):
    step(fishes)


print("Number of fish after {} days: {}".format(nDays, len(fishes)))
print("\n----------------\n")

# Number of fish with each age
# Each fish can have an age from 0 to 9
fishByAge = [ 0 ] * 9

# Read the list of fishes the first day
with open("input.txt", "r") as f:
    inputFishes = [ int(fish) for fish in re.findall(r"([\d]+)", f.readline()) ]
    # Add one to the list of fish by age depending on the age of the fish
    for age in inputFishes:
        fishByAge[age] += 1

def stepByAge(fishByAge):

    # Number of births
    nBirths = fishByAge[0]

    # Decrease one the age of each fish
    for i in range(len(fishByAge) - 1):
        fishByAge[i] = fishByAge[i + 1]

    # Add the new fish to the end
    fishByAge[8] = nBirths

    # Set the age of the fish that have just given birth to 6
    fishByAge[6] += nBirths

    return

# Evolve many days
nDays = 256
for i in range(nDays):
    stepByAge(fishByAge)

print("Number of fish after {} days: {}".format(nDays, sum(fishByAge)))
