#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import itertools as it
import numpy as np

# Read the information from the lines
myTime = 0
lines = []
offsets = []
with open("input.txt", "r") as f:
    # Read my timestamp from the first line
    myTime = int(f.readline())

    # Read the bus numbers from the following lines
    aux = re.findall(r"[^,]+", f.readline())
    # aux = re.findall(r"[^,]+", f.readline())
    thisOffset = 0
    for element in aux:
        if element != "x":
            lines.append(int(element))
            offsets.append(thisOffset)
        thisOffset += 1

# Find the line that goes out closest to my timestamp
closestLine = 0
closestTime = max(lines)
for line in lines:
    # Compute the amount of times the current line went out before my timestamp
    # Notice the integer division
    timesOut = myTime // line
    timesOutRemainder = myTime % line

    # If the remainder of the division is bigger than zero, then add one to timesOut
    if timesOutRemainder > 0:
        timesOut += 1

    # Multiply timesOut by the line number to get the next time at which it will 
    # go out
    nextOut = timesOut * line

    # Check if this is the closest one
    if nextOut - myTime < closestTime:
        closestTime = nextOut - myTime
        closestLine = line

print("Closest line: {}".format(closestLine))
print("Time before the closest line departs: {}".format(closestTime))
print("Product of them: {}".format(closestLine * closestTime))
print("\n----------\n")

earliestTime = 0
increment = 1

for i in range(len(lines)):
    while True:
        if (earliestTime + offsets[i]) % lines[i] == 0:
            break
        earliestTime += increment
    increment *= lines[i]

print("Earliest timestamp where the buses go out in order: {}".format(earliestTime))
