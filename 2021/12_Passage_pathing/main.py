#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Read all the paths in the file
neighbors = {}
with open("input.txt", "r") as f:
    for line in f:
        # Parse the current line
        left, right = re.findall(r"([a-zA-Z]*)-([a-zA-Z]*)", line)[0]
        # Add each of these to the list of neighbors of the other
        if left not in neighbors.keys():
            neighbors[left] = [right]
        else:
            neighbors[left].append(right)
        if right not in neighbors.keys():
            neighbors[right] = [left]
        else:
            neighbors[right].append(left)

# Find the different paths that go from start to end, and pass at most once through
# each lowercase cave
# I allow passing twice through only one small cave, as in the second part of the exercise.
def findPaths(currentCave, path = [], visitedSmall = [], visitedSmallTwice = False):
    # Copy the path variable
    thisPath = path[:]
    # Add the start cave to the path
    thisPath.append(currentCave)
    # If the current cave is the end, return the path
    if currentCave == "end":
        return [ thisPath ]
    if currentCave == "start" and len(path) > 0:
        return []
    # Copy the set of visited caves for the current path
    theseVisitedSmall = visitedSmall.copy()
    # If the start cave is a small one, mark it as visited
    if currentCave.islower():
        theseVisitedSmall.append(currentCave)
    # Get the neighbors that can be visited from the starting cave
    theseNeighbors = [ neigh for neigh in neighbors[currentCave] if neigh not in visitedSmall ]
    # Start paths from the different neighbors
    paths = []
    # If I have not visited a small cave twice, do it now
    if not visitedSmallTwice:
        # visitedSmallTwice = True
        theseNeighborsSmall = [ neigh for neigh in neighbors[currentCave] if neigh.islower() and neigh in visitedSmall ]
        # Start the path in each of these neighbors the second time
        for smallNeigh in theseNeighborsSmall:
            neighborsSmallPaths = findPaths(smallNeigh, thisPath, theseVisitedSmall, True)
            for path in neighborsSmallPaths:
                paths.append(path)

    # Visit the rest of the neighbors (large ones, and small ones for the first time)
    for neigh in theseNeighbors:
        neighborPaths = findPaths(neigh, thisPath, theseVisitedSmall, visitedSmallTwice)
        for path in neighborPaths:
            paths.append(path)

    return paths

# Compute the paths using the recursive function above
paths = findPaths("start")

print("Number of paths: {}".format(len(paths)))
print("\n----------------\n")
