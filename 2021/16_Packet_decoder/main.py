#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import re
# import numpy as np
# import time

dictHexToBin = { "0" : "0000",
                 "1" : "0001",
                 "2" : "0010",
                 "3" : "0011",
                 "4" : "0100",
                 "5" : "0101",
                 "6" : "0110",
                 "7" : "0111",
                 "8" : "1000",
                 "9" : "1001",
                 "A" : "1010",
                 "B" : "1011",
                 "C" : "1100",
                 "D" : "1101",
                 "E" : "1110",
                 "F" : "1111" }

def hexToBin(hexStr):
    binStr = ""
    for ch in hexStr:
        binStr += dictHexToBin[ch]
    return binStr

def binToDecimal(binStr):
    decimal = 0
    binLength = len(binStr)
    for i in range(binLength):
        decimal += int(binStr[i]) * 2 ** (binLength - i - 1)
    return decimal

def readLiteralPacket(string, indexStart = 0):
    # Current index in the string
    i = 6 + indexStart
    # Accumulator for the bits of the literal value
    literalAccumulator = ""
    # Bool that will change when the parsing of the literal is finished
    finished = False
    # Read groups of 5 bits
    while not finished:
        # Read the next 5 bits
        thisGroup = string[i:i+5]
        i += 5
        # If the first bit is a 1, we have not finished yet
        if thisGroup[0] == "1":
            literalAccumulator += thisGroup[1:]

        # If the first bit is a 0, this is the last part of the literal
        if thisGroup[0] == "0":
            literalAccumulator += thisGroup[1:]
            # The packet is ended
            finished = True

    # Convert the literal to decimal
    literal = binToDecimal(literalAccumulator)
    # print("Literal value {}".format(literal))

    return i - indexStart, literal

def readOperatorPacket(string, typeID, indexStart = 0):
    # Current index in the string
    i = 6 + indexStart

    if i >= len(string):
        return len(string) - 1, 0, 0

    # The 7th bit is the length type ID
    lengthTypeID = string[i]
    i += 1

    # Initialize the accumulator for all versions
    versionAcc = 0
    # Initialize the list of values of the different subpackets
    values = []
    # Initialize the result variable
    result = 0

    # If the lengthTypeID is 0, the next 15 bits are the total length in bits of 
    # the sub-packets contained in this
    if lengthTypeID == "0":
        # Read the next 15 bits
        totalLengthSubpackets = binToDecimal( string[i : i + 15] )
        i += 15
        _, thisVersionAcc, values = readFullPacket(string[ i : i + totalLengthSubpackets ])
        versionAcc += thisVersionAcc
        # Add to the current index
        i += totalLengthSubpackets

    # If the lengthTypeID is 1, the next 11 bits are the number of sub-packets
    # contained in this
    if lengthTypeID == "1":
        # Read the next 11 bits
        nrSubpackets = binToDecimal( string[i : i + 11] )
        i += 11
        # Read the different subpackets
        for _ in range(nrSubpackets):
            iEndSub, thisVersionAcc, value = readPacket(string[i : ])
            values.append(value)
            versionAcc += thisVersionAcc
            i += iEndSub

    # Perform the corresponding operation with the values
    if typeID == 0:
        result = sum(values)
    if typeID == 1:
        result = 1
        for val in values:
            result *= val
    if typeID == 2:
        result = min(values)
    if typeID == 3:
        result = max(values)
    if typeID == 5:
        result = int( values[0] > values[1] )
    if typeID == 6:
        result = int( values[0] < values[1] )
    if typeID == 7:
        result = int( values[0] == values[1] )

    return i - indexStart, versionAcc, result

def readPacket(string):
    # The three first bits are the version
    version = binToDecimal(string[ : 3])

    # The next three bits are the type ID
    typeID = binToDecimal(string[3 : 6])
    # The index where the current packet ends
    iEnd = 0

    # Initialize the accumulator for all versions
    versionAcc = 0
    versionAcc += version
    # Initialize the result variable
    result = 0

    # If the typeID is 4, the packet is a literal
    if typeID == 4:
        # Read the literal until it ends
        iEnd, result = readLiteralPacket(string)

    # Otherwise, it is an operator
    else:
        # Read the opeator packet until it ends
        iEnd, thisVersionAcc, result = readOperatorPacket(string, typeID)
        versionAcc += thisVersionAcc

    return iEnd, versionAcc, result

def readFullPacket(string):
    # Index in the string
    index = 0
    # Initialize the accumulator for all versions
    versionAcc = 0
    # Initialize the list of results
    results = []

    # Parse the entire string
    while index < len(string) - 1:
        # The three first bits are the version
        version = binToDecimal(string[index : index + 3])
        versionAcc += version
        # The next three bits are the type ID
        typeID = binToDecimal(string[index + 3 : index + 6])
        # The index where the current packet ends
        iEnd = 0

        # If the typeID is 4, the packet is a literal
        if typeID == 4:
            # Read the literal until it ends
            iEnd, value = readLiteralPacket(string, index)

        # Otherwise, it is an operator
        else:
            # Read the opeator packet until it ends
            iEnd, thisVersionAcc, value = readOperatorPacket(string, typeID, index)
            versionAcc += thisVersionAcc

        results.append(value)
        index += iEnd

    return index, versionAcc, results

# Read the hexadecimal string
hexString = ""
with open("input.txt", "r") as f:
    hexString = f.readline().strip()
# Convert the hexadecimal string to binary
binString = hexToBin(hexString)

# Parse the entire packet string
index, versionAcc, result = readFullPacket(binString)
result = result[0]

print("Sum of all versions: {}".format(versionAcc))
print("\n----------------\n")
print("Result of all operations: {}".format(result))
