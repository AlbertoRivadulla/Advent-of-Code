import time
import re
import numpy as np
from collections import deque

DIRECTIONS = [
    np.array( [-1, 0], dtype=int ),
    np.array( [ 0, 1], dtype=int ),
    np.array( [ 1, 0], dtype=int ),
    np.array( [ 0,-1], dtype=int ),
    np.array( [ 0, 0], dtype=int ),
]

# Read the initial positions and orientations of the blizzards
blizzard_positions = []
width = 0
height = 0
with open( "input.txt", "r" ) as f:
    # Skip the first line, and use it to compute the width
    width = len( f.readline().strip() ) - 2

    # Read the rest of the lines
    for line in f:
        # If I reached the last line, break
        if line[0] == line[1] == '#':
            break

        # Read the line
        x = 0
        for ch in line.strip()[1:-1]:
            # If there is a blizzard, save it
            if ch == '>':
                blizzard_positions.append( [ [ height, x ], 1 ] )
            elif ch == '<':
                blizzard_positions.append( [ [ height, x ], 3 ] )
            elif ch == 'v':
                blizzard_positions.append( [ [ height, x ], 2 ] )
            elif ch == '^':
                blizzard_positions.append( [ [ height, x ], 0 ] )
            # Add one to the x position
            x += 1

        # Increment the height
        height += 1

# Create the initial map
initial_map = np.ones( [ height, width ], dtype=int )
initial_map *= -1
for pos in blizzard_positions:
    initial_map[ tuple( pos[0] ) ] = pos[1]

################################################################################
# First part
################################################################################

# Function to check if there is going to be a blizzard at a given point and time
def check_if_blizzard( position, time, initial_map ):
    # Go from the position in the four directions
    propagated_pos = [ [ el for el in position ] for _ in range( 4 ) ]
    # Position propagating down (blizzard facing up)
    propagated_pos[0][0] = ( propagated_pos[0][0] + time ) % len( initial_map )
    # Position propagating left (blizzard facing right)
    propagated_pos[1][1] = ( propagated_pos[1][1] - time ) % len( initial_map[0] )
    # Position propagating up (blizzard facing down)
    propagated_pos[2][0] = ( propagated_pos[2][0] - time ) % len( initial_map )
    # Position propagating right (blizzard facing left)
    propagated_pos[3][1] = ( propagated_pos[3][1] + time ) % len( initial_map[0] )

    # Check if there is a blizzard at each propagated position, with the corresponding
    # orientation
    for i in range( len( propagated_pos ) ):
        if initial_map[ tuple(propagated_pos[i]) ] == i:
            return True

    return False

# Function to compute the minimal time to get to a final position
def minimal_time_to_pos( initial_pos, final_pos, initial_map, initial_time = 1 ):
    # Initial time
    time = initial_time
    # Initial position
    initial_position = tuple( initial_pos )
    # Final position
    stop_position = tuple( final_pos )
    # Set of positions to explore in the next step
    positions_to_explore = set( [ initial_position ] )

    while True:
        # Positions for the next step
        next_positions = set()

        # Iterate over the positions to explore in the current step
        for r, c in positions_to_explore:
            # Check all the positions where I can go from this
            for x, y in ((r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                # If the position corresponds to the goal, return the time
                if (x, y) == stop_position:
                    return time

                # If the position is in-bounds and there is no blizzard there,
                # add it to the list of positions for the next step
                if 0 <= x < height and 0 <= y < width \
                        and not check_if_blizzard( [x, y], time, initial_map ):
                    next_positions.add( (x, y) )

        # Positions to explore in the next step
        positions_to_explore = next_positions

        # If I ran out of positions for the next step, start again from the initial
        # one
        if not positions_to_explore:
            positions_to_explore.add( initial_position )

        # Increment the time
        time += 1

start_time = time.time()

# Initial and final positions
initial_pos = [-1, 0]
final_pos = [ len(initial_map), len(initial_map[0]) - 1 ]

# Compute the minimal amount of time to reach the final position
minimal_time = minimal_time_to_pos( initial_pos, final_pos, initial_map )


print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The minimal amount of time to reach the exit is: {}".format( minimal_time ))



################################################################################
# Second part
################################################################################


start_time = time.time()

# Time for the entire trip
total_minimal_time = 0

# Go from the beginning to the exit
total_minimal_time = minimal_time_to_pos( initial_pos, final_pos, initial_map, total_minimal_time )

# Go from the exit to the beginning
total_minimal_time = minimal_time_to_pos( final_pos, initial_pos, initial_map, total_minimal_time )

# Go from the beginning to the exit again
total_minimal_time = minimal_time_to_pos( initial_pos, final_pos, initial_map, total_minimal_time )


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The minimal amount of time for the total trip is: {}".format( total_minimal_time ))
