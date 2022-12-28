#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
# import numpy as np
# import time

def printMap(positions, target):
    # Get the maximum and minimum values of x and y
    minX = min(target[0])
    maxX = max(target[0])
    minY = min(target[1])
    maxY = max(target[1])
    for pos in positions:
        if pos[0] > maxX:
            maxX = pos[0]
        elif pos[0] < minX:
            minX = pos[0]
        if pos[1] > maxY:
            maxY = pos[1]
        elif pos[1] < minY:
            minY = pos[1]

    # Initialize the map
    mapList = [ [ " " for _ in range(maxX - minX + 1) ] for _ in range(maxY - minY + 1) ]

    # Add the target
    for x in range(target[0][0] - minX, target[0][1] - minX + 1):
        for y in range(- target[1][1] + maxY, -target[1][0] + maxY + 1):
            mapList[y][x] = "T"

    # Add the starting position
    mapList[- positions[0][1] + maxY][positions[0][0] - minX] = "S"

    # Add the rest of the positions
    for pos in positions[1:]:
        mapList[- pos[1] + maxY][pos[0] - minX] = "#"

    for line in mapList:
        lineStr = ""
        for el in line:
            lineStr += el
        print(lineStr)

def iterate(pos, vel):
    # Update the position
    pos[0] += vel[0]
    pos[1] += vel[1]

    # Update the valocity
    vel[1] -= 1
    if vel[0] != 0:
        vel[0] -= 1 * int(vel[0] / abs(vel[0]))
    return

def checkIfHits(initialVelocity, target):
    # Iterate several times and check if the target is hit
    # Initial position and velocity
    pos = [ 0, 0 ]
    vel = initialVelocity.copy()
    # Initialize the maximum height reached
    maxHeight = 0
    # Value in x reached in the last iteration
    lastX = 0
    # Iterate until the target is hit or the probe goes below it without hiting it
    while True:
        # Perform one iteration
        iterate(pos, vel)
        # Check if the height is larger than the maximum
        if pos[1] > maxHeight:
            maxHeight = pos[1]
        # Check if the target is hit
        if pos[0] >= target[0][0] and pos[0] <= target[0][1]:
            if pos[1] >= target[1][0] and pos[1] <= target[1][1]:
                return True, 0, maxHeight
        # Check if the probe is below the target and has not hit it
        if pos[1] < target[1][0]:
            # Check if the x of the target is reached
            if pos[0] > target[0][1]:
                return False, +1, maxHeight
            elif pos[0] < target[0][0]:
                return False, -1, maxHeight
            else:
                return False, 0, maxHeight
        # If the value in x reached is the same as the one reached in the previous
        # iteration
        if pos[0] == lastX:
            # print("Last x {}".format(lastX))
            # if lastX < target[0][0]:
            if lastX < target[0][0]:
                # Then the target is not reached
                return False, -1, maxHeight
            elif lastX > target[0][1]:
                # The target is not reached, but the probe went beyond it
                return False, +1, maxHeight
        # Save the value in x reached
        lastX = pos[0]

# Read the target positions
# The first line will be the dimensions in x, and the second one in y
target = [ [ 0, 0 ], [ 0, 0 ] ]
with open("input.txt", "r") as f:
    aux = re.findall(r"x=(-*[\d]+)..(-*[\d]+),\sy=(-*[\d]+)..(-*[\d]+)", f.readline())[0]
    target[0][0] = int(aux[0])
    target[0][1] = int(aux[1])
    target[1][0] = int(aux[2])
    target[1][1] = int(aux[3])

# Shoot the probe from the position (0, 0)
position = [ 0, 0 ]

# positions = [ position.copy() ]
# velocity = [ 7, 0 ]
# for i in range(20):
#     iterate(position, velocity)
#     # Store the new position
#     positions.append(position.copy())
# printMap(positions, target)

# Find initial velocities with which the target is hit
initialVelocity = [ 1, 0 ]
velocitiesThatHit = []
maxHeights = []
while True:
    # Test the current velocity
    hit, reachesTargetX, maxHeight = checkIfHits( initialVelocity, target )
    # If the target is hit, save the velocity
    if hit:
        velocitiesThatHit.append(initialVelocity.copy())
        maxHeights.append(maxHeight)
    # Add 1 to the y component of the velocity
    initialVelocity[1] += 1
    # Do the same if it does not reach the target in x
    if reachesTargetX == -1:
        initialVelocity[1] = 0
        initialVelocity[0] += 1
    # If the initial velocity in x is larger than the maximum x of the target, it
    # will never be hit again
    if initialVelocity[0] > target[0][1]:
        break
    if initialVelocity[1] > 200:
        initialVelocity[1] = 0
        initialVelocity[0] += 1

initialVelocity = [ 1, -1 ]
while True:
    # Test the current velocity
    hit, reachesTargetX, maxHeight = checkIfHits( initialVelocity, target )
    # If the target is hit, save the velocity
    if hit:
        velocitiesThatHit.append(initialVelocity.copy())
        maxHeights.append(maxHeight)
    # Add 1 to the y component of the velocity
    initialVelocity[1] -= 1
    # Do the same if it does not reach the target in x
    if reachesTargetX == -1:
        initialVelocity[1] = -1
        initialVelocity[0] += 1
    # If the initial velocity in x is larger than the maximum x of the target, it
    # will never be hit again
    if initialVelocity[0] > target[0][1]:
        break
    if initialVelocity[1] < -200:
        initialVelocity[1] = -1
        initialVelocity[0] += 1

# print(velocitiesThatHit)
# print(maxHeights)

# # Brute force attempt
# velocitiesThatHit = []
# maxHeights = []
# for vx in range(-200, 200):
#     for vy in range(-300, 300):
#         hit, _, maxHeight = checkIfHits( [ vx, vy ], target )
#         # if hit:
#         if hit and vy >= 0:
#             maxHeights.append(maxHeight)
#             velocitiesThatHit.append( [ vx, vy ] )
#
# print(velocitiesThatHit)
# print(maxHeights)

# Get the maximum height reached
maxHeight = 0
maxVel = []
for i in range(len(maxHeights)):
    if maxHeights[i] > maxHeight:
        maxHeight = maxHeights[i]
        maxVel = velocitiesThatHit[i]

print("Maximum height: {}".format(maxHeight))
print("Velocity that reaches the maximum height: {}".format(maxVel))
print("\n----------------\n")
print("Number of initial velocities that reach the target: {}".format(len(velocitiesThatHit)))

# # Read the initial velocities for the example
# initialVelocitiesExample = []
# with open("initialVelocitiesExample.txt", "r") as f:
#     for line in f:
#         aux = re.findall(r"([\d]+),(-*[\d]+)", line)
#         for vel in aux:
#             if int(vel[1]) >= 0:
#                 initialVelocitiesExample.append( [ int(vel[0]), int(vel[1]) ] )
#
# print(initialVelocitiesExample)
# print(len(initialVelocitiesExample))
