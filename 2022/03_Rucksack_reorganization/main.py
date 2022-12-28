import re

# First part

# Function to get the value of a character
def get_value( char ):
    # Take the ASCII value of the lowercase version of the character
    # Subtract 96, the value before "a"
    value = ord( char.lower() ) - 96
    if char.isupper():
        # Add 26
        value += 26
    return value

# Function to find the repeated character in the two halves of the string
def find_repeated( string ):
    # Separate the string in two
    first  = string[ : len(string) // 2 ]
    second = string[ len(string) // 2 : ]

    # Find the repeated character
    # There is exactly one per rucksack
    for char1 in first:
        for char2 in second:
            if char1 == char2:
                return char1
    return None

# Read the contents of the rucksacks
rucksacks = []
with open( "input.txt", "r" ) as f:
    for line in f:
        rucksacks.append( line.strip() )

total_priority = 0
for rucksack in rucksacks:
    total_priority += get_value( find_repeated( rucksack ) )

print("\n\n--------------\nFirst part\n\n")
print("The sum of priorities is: {}".format( total_priority ))



# Second part

# Find the item that appears in the three rucksacks, which is the badge of the group
# There are better ways to do this, more easily generalizable to larger groups!!
def find_badge( str1, str2, str3 ):
    for ch1 in str1:
        for ch2 in str2:
            if ch1 == ch2:
                for ch3 in str3:
                    if ch1 == ch3:
                        return ch1
    return None

total_priority_badges = 0
index = 0
while index < len( rucksacks ):
    # Add the priority corresponding to the badge of the current group of three elves
    total_priority_badges += get_value( find_badge( rucksacks[ index ],
                                                    rucksacks[ index + 1 ],
                                                    rucksacks[ index + 2 ]
                                                  ) )
    index += 3

print("\n\n--------------\nSecond part\n\n")
print("The sum of priorities of the badges is: {}".format( total_priority_badges ))
