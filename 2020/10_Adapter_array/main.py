#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Read the output joltage of each adapter
adapters = []
with open("input.txt", "r") as f:
    for line in f:
        adapters.append(int(line))

# Get the joltage of the device, as 3 times the maximum of the joltage of all adapters
maxJoltage = 0
for joltage in adapters:
    if joltage > maxJoltage:
        maxJoltage = joltage
deviceJoltage = maxJoltage + 3

# Compute the amount of differences in 1 and 3 jolts when joining all the adapters
# in order
nrDiff1Jolt = 0
nrDiff3Jolt = 0
currentJoltage = 0
# Sort the adapters
adapters.sort()
for i in range(len(adapters)):
    # Find the difference between the joltage after adding the current adapter
    # and before
    if adapters[i] - currentJoltage == 1:
        nrDiff1Jolt += 1
    elif adapters[i] - currentJoltage == 3:
        nrDiff3Jolt += 1

    # Update the current joltage
    currentJoltage = adapters[i]

# Add the difference to the device joltage
if deviceJoltage - currentJoltage == 1:
    nrDiff1Jolt += 1
elif deviceJoltage - currentJoltage == 3:
    nrDiff3Jolt += 1

print("Differences of 1 jolt: {}".format(nrDiff1Jolt))
print("Differences of 3 jolt: {}".format(nrDiff3Jolt))
print("Product of differences: {}".format(nrDiff3Jolt * nrDiff1Jolt))
print("\n----------\n")

# Count the number of arrangements to obtain the required joltage

# Sort the adapters in reverse order, and add the end of the chain
adapters.sort(reverse = True)
adapters.append(0)

# Brute force implementation
def countNextCombinations(targetJoltage, adapters):
    combinations = 0

    if len(adapters) == 0:
        return 1

    # Check which of the following adapters can be connected now
    compatibleAdaptersIndices = []
    for i in range(0, min(3, len(adapters))):
        joltageDiff = targetJoltage - adapters[i]
        if joltageDiff >= 1 and joltageDiff <= 3:
            compatibleAdaptersIndices.append(i)

    # Add the combinations with the compatible adapters
    for i in compatibleAdaptersIndices:
        newCombinations = countNextCombinations(adapters[i], adapters[i + 1:])
        combinations += newCombinations

    return combinations

# # Apply the brute force implementation to the entire set of adapters
# nrCombinations = countNextCombinations(deviceJoltage, adapters)
# print("Number of different combinations: {}".format(nrCombinations))

def countNextPaths(start, adapters):
    paths = 0
    for adapter in adapters:
        joltageDiff = start - adapter
        if joltageDiff >= 1 and joltageDiff <= 3:
            paths += 1
    return paths

def countPreviousPaths(end, adapters):
    paths = 0
    for adapter in adapters:
        joltageDiff = adapter - end
        if joltageDiff >= 1 and joltageDiff <= 3:
            paths += 1
    return paths

# Compute the number of different ways that go from a number to its neighbors
nextPaths = [1] * len(adapters)
previousPaths = [1] * len(adapters)
for i in range(len(adapters)):
    nextPaths[i] = countNextPaths(adapters[i], adapters[i + 1 : min(i + 4, len(adapters))])
    previousPaths[i] = countPreviousPaths(adapters[i], adapters[max(0, i - 4) : i])

# Apply the brute force implementation to restricted sets of adapters, between two
# points out of which there is only one path
leftOne = 0
rightOne = 0
nrCombinations = 1
while rightOne < len(adapters):
    if nextPaths[rightOne] > 1:
        leftOne = rightOne
        # Get to the point where this path and the ones that open after it are closed
        openPaths = nextPaths[rightOne]
        closedPaths = 0

        while True:
            rightOne += 1
            closedPaths += previousPaths[rightOne]
            # Check if all paths have been closed
            if closedPaths == openPaths:
                break
            openPaths += nextPaths[rightOne]

        # Compute the number of combinations between these two points
        combinations = countNextCombinations(adapters[leftOne], adapters[leftOne + 1 : rightOne + 1])
        # Multiply the total number of combinations by this
        nrCombinations *= combinations

        # Update the indices
        leftOne = rightOne - 1

    leftOne += 1
    rightOne += 1

print("Number of different combinations: {}".format(nrCombinations))
