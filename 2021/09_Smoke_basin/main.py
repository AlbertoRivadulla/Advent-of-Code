#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

def findNeighbors(heightmap, point):
    # Create the tentative list of neighbors
    tentativeNeighbors = [ [ point[0] - 1, point[1] ],
                         [ point[0], point[1] - 1 ],
                         [ point[0], point[1] + 1 ],
                         [ point[0] + 1, point[1] ] ]

    # Return only the valid neighbors
    neighbors = []
    for neigh in tentativeNeighbors:
        if neigh[0] < 0 or neigh[0] >= len(heightmap):
            continue
        if neigh[1] < 0 or neigh[1] >= len(heightmap[0]):
            continue
        neighbors.append(neigh)

    return neighbors

def checkIfLowest(heightmap, point, neighbors):
    # Find the height of the current point
    pointHeight = heightmap[point[0]][point[1]]
    # Find the height of the neighbors
    neighborsHeight = [ heightmap[neigh[0]][neigh[1]] for neigh in neighbors ]

    # Check if the point is lower than its neighbors
    lowest = True
    for neighborHeight in neighborsHeight:
        if neighborHeight <= pointHeight:
            lowest = False
            break

    return lowest

# Read the heightmap
heightmap = []
with open("input.txt", "r") as f:
    for line in f:
        # Read the line as numbers
        heights = [ int(nr) for nr in line.strip() ]
        heightmap.append(heights)

# Find the points that are lower than its 4 adjacent points
lowestPoints = []
riskLevel = 0
for i in range(len(heightmap)):
    for j in range(len(heightmap[0])):
        # Find the neighbors
        neighbors = findNeighbors(heightmap, (i, j))
        # Check if this point is lower than its neighbors
        if checkIfLowest(heightmap, (i, j), neighbors):
            # Add this point to the list of lower points
            lowestPoints.append( [ i, j ] )
            # Add this point's contribution to the risk level
            riskLevel += heightmap[i][j] + 1

print("Total risk level: {}".format(riskLevel))
print("\n----------------\n")

def findUnvisitedNeighbors(heightmap, visited, point):
    # Create the tentative list of neighbors
    tentativeNeighbors = [ [ point[0] - 1, point[1] ],
                         [ point[0], point[1] - 1 ],
                         [ point[0], point[1] + 1 ],
                         [ point[0] + 1, point[1] ] ]
    # Return only the valid neighbors
    neighbors = []
    for neigh in tentativeNeighbors:
        if neigh[0] < 0 or neigh[0] >= len(heightmap):
            continue
        if neigh[1] < 0 or neigh[1] >= len(heightmap[0]):
            continue
        if visited[neigh[0]][neigh[1]] == 1:
            continue
        neighbors.append(neigh)
    return neighbors

def countHigherNeighbors(heightmap, visited, point):
    # Find the unvisited neighbors
    tentativeNeighbors = findUnvisitedNeighbors(heightmap, visited, point)
    # Get the height of the current neighbor
    pointHeight = heightmap[point[0]][point[1]]

    # Check that the neighbors are higher than the current point, but not at a 
    # height of 9
    validNeighbors = []
    for neigh in tentativeNeighbors:
        if heightmap[neigh[0]][neigh[1]] == 9:
            continue
        if heightmap[neigh[0]][neigh[1]] < pointHeight:
            continue
        validNeighbors.append(neigh)

    # Counter with the number of neighbors
    nrNeighbors = len(validNeighbors)

    # If there are no more valid neighbors, return the number of them
    if nrNeighbors == 0:
        return 0

    # Mark each neighbor as visited
    for neigh in validNeighbors:
        visited[neigh[0]][neigh[1]] = 1

    # Add to the counter the neighbors of each neighbor
    for neigh in validNeighbors:
        nrNeighbors += countHigherNeighbors(heightmap, visited, neigh)

    return nrNeighbors

# Find the different basins
basinSizes = []
visited = [ [ 0 for i in range(len(heightmap[0])) ] for j in range(len(heightmap)) ]

# Find the number of points in each basin
for lowPoint in lowestPoints:
    # Count the number of points in the current basin
    basinSizes.append(countHigherNeighbors(heightmap, visited, lowPoint) + 1)

# Find product the three largest basin sizes
basinSizes.sort()
productLargestBasins = 1
for size in basinSizes[-3:]:
    productLargestBasins *= size

print("Product of the sizes of the 3 largest basins: {}".format(productLargestBasins))
