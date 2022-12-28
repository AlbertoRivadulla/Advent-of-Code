#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Size of the window
windowSize = 3

# Read the file and store the results in a list
values = []
with open("input.txt", "r") as file:
    values = [ int(val) for val in file.read().splitlines() ]

# Compare elements in the window
count = 0
# Initialize the window
window = [ values[i] for i in range(windowSize + 1) ]

# Index of the last element inserted
iLast = windowSize
# Index of the beginning of the new window
iWindow = 1

# Iterate through the list of values
for i in range(windowSize, len(values)):
    # Add the new value to the winow
    window[iLast] = values[i]
    iLast = (iLast + 1) % (windowSize + 1)

    # Compute the total of the values in each window
    totalLast = sum( [ window[(iWindow - 1 + j) % (windowSize + 1)] for
                      j in range(windowSize)] )
    totalNew = sum( [ window[(iWindow + j) % (windowSize + 1)] for
                      j in range(windowSize)] )
    # Move the index that points to the beginning of the window
    iWindow = (iWindow + 1) % (windowSize + 1)

    # Compare the two windows
    if totalNew > totalLast:
        count += 1

# Print the solution
print(count)
