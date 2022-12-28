#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

# Strings for the different numbers
numberStrings = [ "abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf",
                  "abcdefg", "abcdfg"]

# Read the signals and outputs from the file
signalsAndOutputs = []
with open("input.txt", "r") as f:
    for line in f:
        # Get the signals and the outputs
        signals, outputs = re.findall(r"(.+)\s\|\s(.+)", line)[0]
        # Split the signals and the ouptuts
        signals = re.findall(r"([a-z]+)\s*", signals)
        outputs = re.findall(r"([a-z]+)\s*", outputs)
        # Save these
        signalsAndOutputs.append( [ signals, outputs ] )

# Count the instances of 1, 4, 7 or 8 in the output values
count1478 = 0
for signOut in signalsAndOutputs:
    for output in signOut[1]:
        # Check the length of output
        if len(output) == 2: # A 1
            count1478 += 1
        if len(output) == 4: # A 4
            count1478 += 1
        if len(output) == 3: # A 7
            count1478 += 1
        if len(output) == 7: # A 8
            count1478 += 1

print("Amount of 1, 4, 7 or 8 in the output values: {}".format(count1478))
print("\n----------------\n")

# Function to check if two strings contain the same characters
def checkCharactersEqual(str1, str2):
    # Check if all the characters in the first string are contained in the second one
    valid1 = True
    for char in str1:
        if char not in str2:
            valid1 = False
    # Check if all the characters in the second string are contained in the first one
    valid2 = True
    for char in str2:
        if char not in str1:
            valid2 = False
    # Check if both conditions are met
    return valid1 and valid2

# Function to modify a string with a list to map the characters
def mapString(string, mappingIn, mappingOut):
    # Copy the input string
    output = string
    # Create the table for the translation
    transTable = output.maketrans(mappingIn, mappingOut)
    output = output.translate(transTable)
    return output

# Iterate through all the entries, and sum the output values
sumOutput = 0
for signOut in signalsAndOutputs:
    # List of rules
    mappingsOut = "acfbdeg"
    theseMappingsIn = ""
    # Find the 1, 7, 4 and 8 in the signals
    one = ""
    seven = ""
    four = ""
    eight = ""
    for signal in signOut[0]:
        if len(signal) == 2:
            one = signal
        elif len(signal) == 4:
            four = signal
        elif len(signal) == 3:
            seven = signal
        elif len(signal) == 7:
            eight = signal

    # Find the characters B
    charB = one

    # Find the character A, and add this to the list of rules
    charA = seven
    for char in one:
        charA = charA.replace(char, "")

    # Find the characters C
    charC = four
    for char in one:
        charC = charC.replace(char, "")

    # Find the characters D
    charD = eight.replace(charA, "")
    for char in four:
        charD = charD.replace(char, "")

    # Create the mappings and find the correct one
    valid = False
    for i in range(2):
        for j in range(2):
            for k in range(2):
                # Create the mappings
                theseMappingsIn = charA + \
                                  charB[i] + charB[(i+1)%2] + \
                                  charC[j] + charC[(j+1)%2] + \
                                  charD[k] + charD[(k+1)%2]
                # Map the input strings with the mappings
                mappedInput = [ mapString(inp, theseMappingsIn, mappingsOut) for inp in signOut[0] ]

                # Check if the mappings are correct
                maskValid = [0] * len(numberStrings)
                for mappedNumber in mappedInput:
                    for i2 in range(0, len(numberStrings)):
                        if checkCharactersEqual(numberStrings[i2], mappedNumber):
                            if maskValid[i2] == 1:
                                maskValid[i2] = -100
                                break
                            else:
                                maskValid[i2] = 1
                if sum(maskValid) == 10:
                    valid = True
                    break
            if valid:
                break
        if valid:
            break

    # Interpret the output codes
    goodOutputs = [ mapString(out, theseMappingsIn, mappingsOut) for out in signOut[1] ]
    # Convert these to numbers
    goodOutputsNrs = []
    for output in goodOutputs:
        for i in range(len(numberStrings)):
            if checkCharactersEqual(output, numberStrings[i]):
                goodOutputsNrs.append(i)

    # Sum these to the output values
    thisSumOutput = 0
    for i in range(len(goodOutputsNrs)):
        thisSumOutput += goodOutputsNrs[i] * 10 ** (len(goodOutputsNrs) - i - 1)

    sumOutput += thisSumOutput

print("Sum of the output values: {}".format(sumOutput))
