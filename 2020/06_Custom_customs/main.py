#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Get the sets of answers from each group
allAnswers = []
with open("input.txt", "r") as f:
    groupAnswers = []
    groupMask = []
    for line in f:
        # If the line is \n, the answers of the current group have ended, so add
        # them to the total list as a set (so each answer is only copied once)
        if line == '\n':
            # allAnswers.append( set(groupAnswers) )
            allAnswers.append( [ groupAnswers[i] for i in range(len(groupAnswers))
                                 if groupMask[i] == 1 ] )
            groupAnswers = []
            groupMask = []
            continue
        # Read the current line of answers
        passengerAnswers = re.findall(r"([a-z])", line)
        if len(groupMask) == 0:
            groupMask = [1] * len(passengerAnswers)
            groupAnswers = passengerAnswers
        else:
            for i in range(len(groupAnswers)):
                if groupAnswers[i] not in passengerAnswers:
                    groupMask[i] = 0

    # Save also the answers of the final group
    allAnswers.append( [ groupAnswers[i] for i in range(len(groupAnswers))
                         if groupMask[i] == 1 ] )

# Find the total amount of answers in the different groups
totalAnswers = 0
for answers in allAnswers:
    totalAnswers += len(answers)

print("Total amount of answers: {}".format(totalAnswers))
print("\n----------\n")
