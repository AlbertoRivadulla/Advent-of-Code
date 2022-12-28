#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

windowSize = 25

# Read the list of numbers
numbers = []
with open("input.txt", "r") as f:
    for line in f:
        numbers.append(int(line))

# Find the first number, after the preamble, that is not a sum on a pair of the 
# numbers in the window before it
firstInvalid = 0
for i in range(windowSize, len(numbers)):
    valid = False
    # Check if the current number is a sum of a pair in the window before it
    for j in range(i - windowSize, i):
        for k in range(j+1, i):
            if numbers[i] == numbers[j] + numbers[k]:
                valid = True
                break
        if valid == True:
            break

    # Otherwise, break the loop
    if not valid:
        firstInvalid = numbers[i]
        break


print("First invalid number: {}".format(firstInvalid))
print("\n----------\n")

# Find a contiguous set of at least two numbers that sum to the first invalid
# number above
sumSmallestLargest = 0
for i in range(len(numbers)):
    foundRange = False
    for j in range(i + 1, len(numbers)):
        # Sum all numbers between the positions i and j
        sumContiguous = sum(numbers[i:j])
        # Check if the sum is equal to the first invalid number above
        if sumContiguous == firstInvalid:
            foundRange = True
            # Find the smallest and largest numbers in this range
            small = firstInvalid # Because every element in the range must be less that the sum!
            large = 0
            for nr in numbers[i:j]:
                if nr < small:
                    small = nr
                elif nr > large:
                    large = nr
            sumSmallestLargest = small + large

    if foundRange == True:
        break


print("Sum of the first and last numbers in the contiguos set: {}".format(sumSmallestLargest))
