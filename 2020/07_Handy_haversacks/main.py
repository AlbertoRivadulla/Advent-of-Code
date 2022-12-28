#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
# ([a-z]+\s[a-z]+)\s[a-z]+\scontain\s(\d+)\s([a-z]+\s[a-z]+)\s[a-z]+

# Get all the sets of rules from the file
rules = {}
with open("input.txt", "r") as f:
    for line in f:
        outerBag = re.findall(r"([a-z]+\s[a-z]+)\sbags\scontain", line)[0]
        innerBags = re.findall(r"([\d]+)\s([a-z]+\s[a-z]+)", line)

        # Add the rules to the current outer bag
        rules[outerBag] = [ [ int(nr), color ] for (nr, color) in innerBags ]

# Get the possible outer bags in which by bag can be contained
def findOuterBags(innerBag, rules):
    outerBags = set()

    # Iterate through all the outer bags in the list of rules
    for outerBag in rules.keys():
        # Check if the inner bag is contained in it
        if innerBag in [ rule[1] for rule in rules[outerBag] ]:
            outerBags.add(outerBag)

    # Check if each of the outer bags can itself be contained in another
    for outerBag in outerBags:
        outerOuterBags = findOuterBags(outerBag, rules)
        # Add these to the set of outer bags
        outerBags = outerBags.union(outerOuterBags)

    return outerBags

myBag = "shiny gold"
outerBags = findOuterBags(myBag, rules)

print("Amount of different bags that can contain mine: {}".format(len(outerBags)))
print("\n----------\n")

# Count the number of bags inside mine
def countBagsInside(outerBag, rules):
    nrBagsInside = 0

    # Iterate through all the bags that are inside this one
    for (nr, innerBag) in rules[outerBag]:
        # Add the current inner bag
        nrBagsInside += nr
        # Add the bags inside the current inner bag
        nrBagsInsideOfInnerBag = countBagsInside(innerBag, rules)
        nrBagsInside += nr * nrBagsInsideOfInnerBag

    return nrBagsInside

nrBagsInside = countBagsInside(myBag, rules)

print("Amount of bags inside mine: {}".format(nrBagsInside))
