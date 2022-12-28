#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Function to update the polymer
def updatePolymer(polymer, rules):
    # Initialize the new polymer
    newPolymer = ""

    # Go through the characters in the original polymer
    for i in range(len(polymer) - 1):
        # Add the current character
        newPolymer += polymer[i]
        # Insert a character based on the current one and the following, according
        # to the rules
        newPolymer += rules[polymer[i]][polymer[i + 1]]

    # Add the last character of the polymer
    newPolymer += polymer[-1]

    return newPolymer

# Read the polymer templace and the insertion rules
initialPolymer = ""
rules = {}
characters = set()
with open("input.txt", "r") as f:
    # Read the polymer template from the first line
    initialPolymer = f.readline().strip()

    for line in f:
        # Read the rule
        rule = re.findall(r"([A-Z])([A-Z])\s->\s([A-Z])", line)
        if len(rule) != 0:
            if len(rules) == 0:
                rules[rule[0][0]] = { rule[0][1] : rule[0][2] }
            else:
                if rule[0][0] not in rules.keys():
                    rules[rule[0][0]] = { rule[0][1] : rule[0][2] }
                else:
                    rules[rule[0][0]][rule[0][1]] = rule[0][2]
            # Save the current character
            characters.add(rule[0][0])

# Update the polymer several times
nrSteps = 10
polymer = initialPolymer
for step in range(nrSteps):
    polymer = updatePolymer(polymer, rules)

# Count the differnt characters
characterCount = { char : 0 for char in characters }
for polymerChar in polymer:
    characterCount[polymerChar] += 1

# Get the counts of the most common and least common characters
mostCommonCount = 0
leastCommonCount = len(polymer)
for char in characterCount.keys():
    if characterCount[char] > mostCommonCount:
        mostCommonCount = characterCount[char]
    if characterCount[char] < leastCommonCount:
        leastCommonCount = characterCount[char]

print("Difference between the most and least common characters after 10 steps: {}".format(mostCommonCount - leastCommonCount))
print("\n----------------\n")

# Function to update the dictionary of adjacencies
def updateAdjacencies(adjacencies, rules):
    newAdjacencies = adjacencies.copy()
    newAdjacencies = { key : val.copy() for key, val in zip(adjacencies.keys(), adjacencies.values()) }
    # Iterate through the list of adjacencies
    for left in adjacencies.keys():
        for right in adjacencies[left].keys():
            thisAdjacencyCount = adjacencies[left][right]
            if thisAdjacencyCount > 0:
                # Check if there is a rule to insert something between these
                if right in rules[left].keys():
                    # Get the element that must be in the middle
                    middle = rules[left][right]
                    # Remove this adjacency
                    newAdjacencies[left][right] -= thisAdjacencyCount
                    # Add the two corresponding adjacencies
                    newAdjacencies[left][middle] += thisAdjacencyCount
                    newAdjacencies[middle][right] += thisAdjacencyCount

    return newAdjacencies

# Initialize the list of adjacenties adjacencies
adjacencies = {}
for left in characters:
    for right in characters:
        if left not in adjacencies.keys():
            adjacencies[left] = { right : 0 }
        else:
            adjacencies[left][right] = 0

# Count the adjacencies in the initial string
for i in range(len(initialPolymer) - 1):
    adjacencies[initialPolymer[i]][initialPolymer[i + 1]] += 1

# Update the list of adjacencies several times
nrSteps = 40
polymer = initialPolymer
for step in range(nrSteps):
    adjacencies = updateAdjacencies(adjacencies, rules)

# Count the different characters
characterCount = { char : 0 for char in characters }
totalCharacters = 0
# Add the first character in the initial string
characterCount[initialPolymer[0]] += 1
for left in adjacencies.keys():
    for right in adjacencies[left].keys():
        characterCount[right] += adjacencies[left][right]
        totalCharacters += adjacencies[left][right]

# Get the counts of the most common and least common characters
mostCommonCount = 0
leastCommonCount = totalCharacters
for char in characterCount.keys():
    if characterCount[char] > mostCommonCount:
        mostCommonCount = characterCount[char]
    if characterCount[char] < leastCommonCount:
        leastCommonCount = characterCount[char]

print("Difference between the most and least common characters after 40 steps: {}".format(mostCommonCount - leastCommonCount))
