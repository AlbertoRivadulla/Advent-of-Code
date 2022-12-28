#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

validCounter = 0
with open("input.txt", "r") as f:
    for line in f:
        # Parse the line
        parsedLine = re.findall(r"(\d+)-(\d+)\s(\w):\s(\w+)", line)[0]

        # Get the two indices
        i1 = int(parsedLine[0]) - 1
        i2 = int(parsedLine[1]) - 1
        # Character of reference
        character = parsedLine[2]
        # Password
        password = parsedLine[3]

        # Check that only one of the positions given by the indices in the password
        # is equal to the reference character
        if (password[i1] == character and password[i2] != character) or \
                (password[i1] != character and password[i2] == character):
            validCounter += 1
            # print(password)

print("Valid passwords: {}".format(validCounter))
