import time
import re

# Read the starting numbers
starting_nrs = []
with open( "input.txt", "r" ) as f:
    numbers = f.readline().strip().split(',')
    starting_nrs = [ int( nr ) for nr in numbers ]

################################################################################
# First part
################################################################################

start_time = time.time()

# Dictionary of the spoken numbers and the last turn they have been spoken
spoken_nrs = {}

# Speak the starting numbers
for i in range( len( starting_nrs ) - 1 ):
    spoken_nrs[ starting_nrs[i] ] = i + 1
# Save the last of the starting numbers as the last spoken number, for the next
# turn
last_nr = starting_nrs[ -1 ]

# Continue playing until reaching 2020 turns
for turn in range( len(starting_nrs) + 1, 2021 ):
# for turn in range( len(starting_nrs) + 1, 11 ):
    # print( "\nTurn {}".format( turn ) )

    # Copy the last number
    last_nr_copy = last_nr

    # Check if this was the first time the last number was spoken
    if last_nr not in spoken_nrs:
        # If it was the first time, speak 0
        last_nr = 0
    else:
        # Speak the difference between the previous turn and the turn where it
        # was previously spoken
        last_nr = turn - 1 - spoken_nrs[ last_nr ]

    # Save the last spoken number
    spoken_nrs[ last_nr_copy ] = turn - 1

    # print( last_nr )

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The last number spoken after 2020 turns is {}".format( last_nr ))



################################################################################
# Second part
################################################################################


start_time = time.time()

# Dictionary of the spoken numbers and the last turn they have been spoken
spoken_nrs = {}

# Speak the starting numbers
for i in range( len( starting_nrs ) - 1 ):
    spoken_nrs[ starting_nrs[i] ] = i + 1
# Save the last of the starting numbers as the last spoken number, for the next
# turn
last_nr = starting_nrs[ -1 ]

# Continue playing until reaching 2020 turns
for turn in range( len(starting_nrs) + 1, 30000001 ):
# for turn in range( len(starting_nrs) + 1, 11 ):

    if turn % 1000000 == 0:
        print( "Turn {}".format( turn ) )

    # Copy the last number
    last_nr_copy = last_nr

    # Check if this was the first time the last number was spoken
    if last_nr not in spoken_nrs:
        # If it was the first time, speak 0
        last_nr = 0
    else:
        # Speak the difference between the previous turn and the turn where it
        # was previously spoken
        last_nr = turn - 1 - spoken_nrs[ last_nr ]

    # Save the last spoken number
    spoken_nrs[ last_nr_copy ] = turn - 1

    # print( last_nr )

print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The last number spoken after 30000000 turns is {}".format( last_nr ))
