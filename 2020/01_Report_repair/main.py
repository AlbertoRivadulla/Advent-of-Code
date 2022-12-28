#!/usr/bin/env python3
# -*- coding: utf-8 -*-

lines = []
with open("input.txt", "r") as f:
    for line in f:
        lines.append(int(line))

# Iterate over the lines to find the two entries that sum to 2020
firstEntry = 0
secondEntry = 0
thirdEntry = 0
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        for k in range(j + 1, len(lines)):
            if ( lines[i] + lines[j] + lines[k] == 2020 ):
                firstEntry = lines[i]
                secondEntry = lines[j]
                thirdEntry = lines[k]
                print("Match found!")

# print("Entries: {}, {}".format(firstEntry, secondEntry))
print("Product: {}".format(firstEntry * secondEntry * thirdEntry))
