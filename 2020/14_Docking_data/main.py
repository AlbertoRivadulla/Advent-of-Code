#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import itertools as it
import numpy as np

def decimalToBinary(nr, length):
    binaryDigits = [0] * length
    quotient = nr
    remainder = 0
    index = 0

    while quotient != 0:
        # Get the remainder of the division by two
        remainder = quotient % 2
        # Divide the number by two
        quotient = quotient // 2
        # Add the remainder to the list of binary digits
        # binaryDigits.append(remainder)
        binaryDigits[ - 1 - index ] = remainder
        # Move the index
        index += 1

    # # Invert the order of the list
    # binaryDigits.reverse()
    #
    return binaryDigits

def binaryToDecimal(binaryDigits):
    decimalValue = 0

    for i in range(len(binaryDigits)):
        decimalValue += binaryDigits[- 1 - i] * 2 ** i

    return decimalValue

def applyMask(binaryDigits, mask):
    for i in range(len(binaryDigits)):
        if mask[i] == "X":
            continue
        elif mask[i] == "0":
            binaryDigits[i] = 0
        elif mask[i] == "1":
            binaryDigits[i] = 1
    return binaryDigits

# Read the mask and values
memoryAndValues = []
with open("input.txt", "r") as f:
    currentMask = ""
    for line in f:
        # Check if the line contains a mask
        readMask = re.findall(r"mask\s=\s([\w]+)", line)
        if len(readMask) == 1:
            currentMask = readMask[0]
            continue
        # Otherwise, the line is a value for the memory
        memoryLine = [int(nr) for nr in re.findall(r"mem\[([\d]+)\]\s=\s([\d]+)", line)[0] ]
        # Convert the value in memory to binary
        binaryDigits = decimalToBinary(memoryLine[1], len(currentMask))
        # Apply the mask
        binaryDigits = applyMask(binaryDigits, currentMask)
        # Convert the number back to decimal
        memoryLine[1] = binaryToDecimal(binaryDigits)
        # Append this to the memory array
        memoryAndValues.append(memoryLine)

# Get the maximum index in memory
memoryLength = 0
for register in memoryAndValues:
    if register[0] > memoryLength:
        memoryLength = register[0]

# Create an array of memoryLength with the current values in memory
memory = [ 0 ] * (memoryLength + 1)
for register in memoryAndValues:
    memory[ register[0] ] = register[1]

# Compute the sum of the values in memory
sumMemory = sum(memory)

print("Sum of the values in memory: {}".format(sumMemory))
print("\n----------\n")

def applyMaskAddress(binaryDigits, mask):
    for i in range(len(binaryDigits)):
        if mask[i] == "X":
            binaryDigits[i] = "X"
        elif mask[i] == "0":
            # binaryDigits[i] = 0
            continue
        elif mask[i] == "1":
            binaryDigits[i] = 1
    return binaryDigits

def getMemoryAddresses(binaryAddress):
    memoryAddresses = []

    # Find the first floating bit "X"
    indexFirstFloating = len(binaryAddress)
    for i in range(len(binaryAddress)):
        if binaryAddress[i] == "X":
            indexFirstFloating = i
            break

    # If there is no floating bit, return the address
    if indexFirstFloating == len(binaryAddress):
        return [ binaryAddress ]

    # Add the addresses obtained by replacing this bit first by 1 and then by 0
    replacedBinaryAddress = binaryAddress[:]
    replacedBinaryAddress[indexFirstFloating] = 1
    subMemoryAddresses = getMemoryAddresses(replacedBinaryAddress)
    for address in subMemoryAddresses:
        memoryAddresses.append(address)

    replacedBinaryAddress = binaryAddress[:]
    replacedBinaryAddress[indexFirstFloating] = 0
    subMemoryAddresses = getMemoryAddresses(replacedBinaryAddress)
    for address in subMemoryAddresses:
        memoryAddresses.append(address)

    return memoryAddresses

# Read the mask and values
memoryAndValues = []
with open("input.txt", "r") as f:
    currentMask = ""
    for line in f:
        # Check if the line contains a mask
        readMask = re.findall(r"mask\s=\s([\w]+)", line)
        if len(readMask) == 1:
            currentMask = readMask[0]
            continue
        # Otherwise, the line is a value for the memory
        memoryLine = [int(nr) for nr in re.findall(r"mem\[([\d]+)\]\s=\s([\d]+)", line)[0] ]
        # Convert the address to binary
        binaryAddress = decimalToBinary(memoryLine[0], len(currentMask))
        # Apply the mask to the address
        binaryAddress = applyMaskAddress(binaryAddress, currentMask)

        # Get the different binary addresses that this produces
        binaryAddresses = getMemoryAddresses(binaryAddress)

        # Write the value to all these addresses
        for address in binaryAddresses:
            memoryAndValues.append( [ binaryToDecimal(address), memoryLine[1] ] )

# # Get the maximum index in memory
# memoryLength = 0
# for register in memoryAndValues:
#     if register[0] > memoryLength:
#         memoryLength = register[0]
#
# # Create an array of memoryLength with the current values in memory
# memory = [ 0 ] * (memoryLength + 1)
# for register in memoryAndValues:
#     memory[ register[0] ] = register[1]

# Compute the sum of the values in memory
visitedAddresses = []
sumMemory = 0
for i in range(len(memoryAndValues)):
    if memoryAndValues[-1-i][0] not in visitedAddresses:
        visitedAddresses.append(memoryAndValues[-1-i][0])
        sumMemory += memoryAndValues[-1-i][1]

print("Sum of the values in memory: {}".format(sumMemory))
