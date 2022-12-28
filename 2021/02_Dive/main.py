#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Accumulators for the position of hthe submarine
horizontal = 0
depth = 0
aim = 0

with open("input.txt", "r") as f:
    for line in f:
        movement = [ (direc, int(dist)) for (direc, dist) in
                     re.findall( r"([a-z]+)\s(\d+)", line ) ][0]

        # Move the submarine
        if movement[0] == "forward":
            horizontal += movement[1]
            depth += aim * movement[1]
        elif movement[0] == "down":
            # depth += movement[1]
            aim += movement[1]
        elif movement[0] == "up":
            # depth -= movement[1]
            aim -= movement[1]


print("Horizontal {}, depth {}".format(horizontal, depth))
print("Horizontal * depth = {}".format(horizontal * depth))



