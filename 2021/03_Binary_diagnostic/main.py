#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import re

def mostCommon(code):
    if code.count("1") > (len(code) - 1) / 2:
        return 1
    else:
        return 0

def binaryToDecimal(string):
    result = 0
    for i in range(len(string)):
        if string[-i - 1] == "1":
            result += 2**i
    return result


# Variable to count the number of lines in the input
countLines = 0
# List to count the appearances of the digit 1 in each position of the lines
countDigits = []

# List of codes
codeList = []

with open("input.txt", "r") as f:
    for line in f:
        # If the length of the list countDigits is zero, initialize it
        if len(countDigits) == 0:
            countDigits = [0] * ( len(line) - 1 )

        # Read the code
        code = line

        # Iterate through all the digits in the line
        # Subtract one to take into account that the last character is a \n
        for i in range(len(code) - 1):
            if code[i] == '1':
                countDigits[i] += 1

        # Increase the counter of lines
        countLines += 1

        # Add the code to the list
        codeList.append(code[:-1])

# From the counts of digits, get the gamma and epsilon numbers
gamma = 0
epsilon = 0
for i in range(len(countDigits)):
    # Check if the most common digit is a 1, starting backwards
    if countDigits[-i - 1] > (countLines / 2):
        # Since it is a one, add to the decimal number gamma
        gamma += 2**i
    # Otherwise, the least common number is a 1, which adds to epsilon
    else:
        epsilon += 2 **i

print("Gamma rate: {}".format(gamma))
print("Epsilon rate: {}".format(epsilon))

print("Gamma * Epsilon = {}".format(gamma * epsilon))

# Compute the oxygen generator rating
def getOxygenRating(codes, level = 0):
    # If there is only one code in the list, return int
    if len(codes) == 1:
        return codes[0]

    # New list of codes
    newCodes = []

    # Get the most common value of the first character
    countOnes = 0
    for code in codes:
        if code[level] == "1":
            countOnes += 1

    # Determine the most common value from the countOnes variable
    mostCommonChar = "0"
    if countOnes >= len(codes) / 2:
        mostCommonChar = "1"


    # Get the new list as the list of values that start with this character
    for code in codes:
        if code[level] == mostCommonChar:
            newCodes.append(code)

    # Repeat the procedure with the remaining codes
    return getOxygenRating(newCodes, level + 1)

oxygenRating = binaryToDecimal( getOxygenRating(codeList) )

# Compute the CO2 scrubber rating
def getCO2Rating(codes, level = 0):
    # If there is only one code in the list, return int
    if len(codes) == 1:
        return codes[0]

    # New list of codes
    newCodes = []

    # Get the most common value of the first character
    countOnes = 0
    for code in codes:
        if code[level] == "1":
            countOnes += 1

    # Determine the least common value from the countOnes variable
    leastCommonChar = "0"
    if countOnes < len(codes) / 2:
        leastCommonChar = "1"

    # Get the new list as the list of values that start with this character
    for code in codes:
        if code[level] == leastCommonChar:
            newCodes.append(code)

    # Repeat the procedure with the remaining codes
    return getCO2Rating(newCodes, level + 1)

CO2Rating = binaryToDecimal( getCO2Rating(codeList) )

print("\n-------------\n")
print("Oxigen generator rating: {}".format(oxygenRating))
print("CO2 scrubber rating: {}".format(CO2Rating))

print(oxygenRating * CO2Rating)




