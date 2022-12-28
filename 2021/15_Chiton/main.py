#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np
import time
import heapq

def findNeighbors(riskMap, pos):
    # # Tentative neighbors
    # tentativeNeighbors = [ ( pos[0] - 1, pos[1] ),
    #                        ( pos[0], pos[1] - 1 ),
    #                        ( pos[0] + 1, pos[1] ),
    #                        ( pos[0], pos[1] + 1 ) ]
    #
    # # Valid neighbors
    # neighbors = []
    # for neigh in tentativeNeighbors:
    #     if neigh[0] >= 0 and neigh[0] < len(riskMap) and neigh[1] >= 0 and neigh[1] < len(riskMap[0]):
    #         # neighbors.append( ( neigh, riskMap[neigh[0]][neigh[1]] ) )
    #         neighbors.append( neigh )

    neighbors = []
    if pos[0] > 0:
        neighbors.append( ( pos[0] - 1, pos[1] ) )
    if pos[0] < len(riskMap) - 1:
        neighbors.append( ( pos[0] + 1, pos[1] ) )
    if pos[1] > 0:
        neighbors.append( ( pos[0], pos[1] - 1 ) )
    if pos[1] < len(riskMap[0]) - 1:
        neighbors.append( ( pos[0], pos[1] + 1 ) )

    return neighbors

def findNeighborsNotVisited(riskMap, pos, visitedPos):
    # # Tentative neighbors
    # tentativeNeighbors = [ ( pos[0] - 1, pos[1] ),
    #                        ( pos[0], pos[1] - 1 ),
    #                        ( pos[0] + 1, pos[1] ),
    #                        ( pos[0], pos[1] + 1 ) ]
    #
    # # Valid neighbors
    # neighbors = []
    # for neigh in tentativeNeighbors:
    #     if neigh[0] >= 0 and neigh[0] < len(riskMap) and neigh[1] >= 0 and neigh[1] < len(riskMap[0]) and neigh not in visitedPos:
    #         # neighbors.append( ( neigh, riskMap[neigh[0]][neigh[1]] ) )
    #         neighbors.append( neigh )

    neighbors = []
    if pos[0] > 0:
        thisNeigh = ( pos[0] - 1, pos[1] )
        if thisNeigh not in visitedPos:
            neighbors.append(thisNeigh)
    if pos[0] < len(riskMap) - 1:
        thisNeigh = ( pos[0] + 1, pos[1] )
        if thisNeigh not in visitedPos:
            neighbors.append(thisNeigh)
    if pos[1] > 0:
        thisNeigh = ( pos[0], pos[1] - 1 )
        if thisNeigh not in visitedPos:
            neighbors.append(thisNeigh)
    if pos[1] < len(riskMap[0]) - 1:
        thisNeigh = ( pos[0], pos[1] + 1 )
        if thisNeigh not in visitedPos:
            neighbors.append(thisNeigh)

    return neighbors

# Read the map with the risk level
riskMap = []
with open("input.txt", "r") as f:
    for line in f:
        thisLine = []
        for char in line.strip():
            thisLine.append(int(char))
        riskMap.append(thisLine)

# Find the risk of the path that starts in the upper left and goes to the lower
# right
goalPos = ( len(riskMap) - 1, len(riskMap[0]) - 1 )

# ==============================================================================
# Solution with the Dijkstra algorithm

def Dijkstra(riskMap):
    # Initialize the distances to each node with an effectively infinite value.
    # This will be the distance of the shortest path to each node
    maxDistance = 9 * ( len(riskMap) + len(riskMap[0]) )
    distances = [ [ maxDistance for _ in range(len(riskMap)) ] for _ in range(len(riskMap[0])) ]
    # Set the distance to the first node to 0
    distances[0][0] = 0

    # Initialize the list of visited positions
    visitedPositions = [ (0, 0) ]

    # Iterate through all the nodes, starting from the position ( 0, 0 )
    for i in range(len(riskMap)):
        # print("{} / {}".format(i, len(riskMap)))
        for j in range(len(riskMap[0])):
            # Get the unvisited neighbors
            neighbors = findNeighborsNotVisited(riskMap, (i, j), visitedPositions)
            # For each neighbor, check if the distance stored is smaller than the one
            # of the current position plus the distance between the two, and update it
            # otherwise
            for neigh in neighbors:
                tentativeNewDistance = distances[i][j] + riskMap[neigh[0]][neigh[1]]
                if distances[neigh[0]][neigh[1]] > tentativeNewDistance:
                    distances[neigh[0]][neigh[1]] = tentativeNewDistance
            # Mark the current node as visited
            visitedPositions.append( ( i, j ) )

    return distances

def Dijkstra2(riskMap):
    '''Based on the implementation in
        https://github.com/benediktwerner/AdventOfCode/blob/master/2021/day15/sol.py
    '''
    # Define the goal position
    goalx = len(riskMap) - 1
    goaly = len(riskMap[1]) - 1

    # List of nodes to visit
    # Initialize it with the first node, which has a distance of zero
    toDo = [ ( 0, (0, 0) ) ]
    # Heapify the list, bringin the smallest element to the first position
    heapq.heapify(toDo)

    # Set of visited nodes
    visited = set()

    while toDo:
        # Get the last node to visit, which is the smallest element in the heap toDo.
        # This removes the element from the heap.
        # This gets the value with the smallest risk value. If a node appears twice
        # (because it was visited through more than one path), this gets the lowest
        # risk found for it. Then it is marked as visited. So if we take the same
        # node again (with a larger risk value now), since it has already been 
        # visited the loop will skip this iteration, and continue.
        risk, (x, y) = heapq.heappop(toDo)
        # If the element is the goal, return its risk
        if x == goalx and y == goaly:
            # return risk, distances
            return risk
        # If the node is visited, continue
        if ( x, y ) in visited:
            continue
        # Mark the node as visited
        visited.add( ( x, y ) )
        # Get the unvisited neighbors
        neighbors = findNeighborsNotVisited(riskMap, ( x, y ), visited)
        # Add each of the neighbors to the toDo heap, with its risk value updated
        for neigh in neighbors:
            heapq.heappush( toDo, ( risk + riskMap[neigh[0]][neigh[1]], neigh ) )

# Initialize the list of visited positions
visitedPositions = [ (0, 0) ]

# Initialize the distances to each node with an effectively infinite value.
# This will be the distance of the shortest path to each node
maxDistance = 9 * ( len(riskMap) + len(riskMap[0]) )
distances = [ [ maxDistance for _ in range(len(riskMap)) ] for _ in range(len(riskMap[0])) ]
# Set the distance to the first node to 0
distances[0][0] = 0

# Compute the best risk for each position with the function implemented above
t0 = time.process_time()
distances = Dijkstra(riskMap)
t1 = time.process_time()

print("Time of execution: {}".format(t1 - t0))
print("Total risk of the path: {}".format(distances[-1][-1]))
print("\n----------------\n")

# Repeat the map 5 times in each direction, adding one to each value and winding it
# back to the range 1-9 if they go over it
repeatedRiskMap = []
for i in range(5):
    for line in riskMap:
        lineRepeated = []
        for j in range(5):
            for element in line:
                thisElement = ( element + i + j ) % 9
                if thisElement == 0:
                    thisElement = 9
                lineRepeated.append(thisElement)
        repeatedRiskMap.append(lineRepeated)

# # Compute the best risk for each position with the first function implemented above
# t0 = time.process_time()
# distances = Dijkstra(repeatedRiskMap)
# t1 = time.process_time()
# print("Time of execution (1st implementation): {}".format(t1 - t0))

# Compute the best risk for each position with the second function implemented above
t0 = time.process_time()
risk = Dijkstra2(repeatedRiskMap)
t1 = time.process_time()
print("Time of execution (2nd implementation): {}".format(t1 - t0))

print("Total risk of the path: {}".format(risk))
