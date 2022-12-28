#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Set of required fields
requiredFields = set( ( "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid" ) )

# Read the batch of passports
passportEntries = []
with open("input.txt", "r") as f:
    # Variable to hold all the present fields of the passport
    fieldsPassport = []

    # Read the lines
    for line in f:
        # If the line is empty, restart the fields
        if line == "\n":
            # Add the current entry to the list, as a dictionary
            passportEntries.append({ key:value for (key, value) in fieldsPassport })
            # Restart the passport
            fieldsPassport = []

        # Find the present fields in the current line
        fieldsLine = re.findall( r"(byr|iyr|eyr|hgt|hcl|ecl|pid):([\S]+)", line )
        # Add these fields to the current passport
        for field in fieldsLine:
            fieldsPassport.append(field)

    # Add the last entry to the list, as a dictionary
    passportEntries.append({ key:value for (key, value) in fieldsPassport })

# Check which of the different entries contain all fields
validCounter = 0
validPassportEntries = []
for entry in passportEntries:
    # Check if the current passport has all the required fields
    valid = True
    for field in requiredFields:
        if field not in entry.keys():
            valid = False
            break
    if valid == True:
        # Add one to the counter
        validCounter += 1
        # Add it to the list of valid passport entries
        validPassportEntries.append(entry)

print("Entries that contain all fields: {}".format(validCounter))
print("\n----------\n")

# Check which entries are valid according to other rules
validCounter = 0
for entry in validPassportEntries:

    valid = True

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    byr = entry["byr"]
    if len(byr) != 4 or int(byr) < 1920 or int(byr) > 2002:
        # Invalid
        continue

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    iyr = entry["iyr"]
    if len(iyr) != 4 or int(iyr) < 2010 or int(iyr) > 2020:
        # Invalid
        continue

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr = entry["eyr"]
    if len(eyr) != 4 or int(eyr) < 2020 or int(eyr) > 2030:
        # Invalid
        continue

    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    hgt = entry["hgt"]
    if hgt[-2:] == "in" or hgt[-2:] == "cm":
        try:
            # Try to convert the entry to a number
            height = float(hgt[:-2])
            # Check if it is within bounds
            if hgt[-2:] == "cm" and ( height < 150 or height > 193 ):
                # Invalid
                continue
            if hgt[-2:] == "in" and ( height < 59 or height > 76 ):
                # Invalid
                continue
        except:
            # Invalid
            continue
    else:
        # Invalid
        continue

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = entry["hcl"]
    if hcl[0] != "#":
        # Invalid
        continue
    else:
        characters = re.findall(r"[a-f0-9]", hcl[1:])
        if len(characters) != 6:
            # Invalid
            continue

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl = entry["ecl"]
    if ecl not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        # Invalid
        continue

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = entry["pid"]
    digits = re.findall(r"[0-9]", pid)
    if len(digits) != 9:
        # Invalid
        continue

    # cid (Country ID) - ignored, missing or not.

    # If all the conditions were fulfilled, add one to the counter of valid passports
    validCounter += 1


print("Valid entries: {}".format(validCounter))
