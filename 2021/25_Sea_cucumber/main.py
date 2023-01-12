import time
import re
import numpy as np

# Function to print the map
def print_map( cucumber_map ):
    string = ''
    for line in cucumber_map:
        for el in line:
            if el == 0:
                string += '.'
            elif el == 1:
                string += '>'
            elif el == 2:
                string += 'v'
        string += '\n'

    print( string )

# Read the map with the positions and directions of the cucumbers
# Values in the map:
#   0 -> Empty
#   1 -> Cucumber facing east
#   2 -> Cucumber facing south
cucumbers_east = []
cucumbers_south = []
cucumber_map = []
with open( "input.txt", "r" ) as f:
    width = 0
    height = 0
    nr_east = 0
    nr_south = 0
    # Find the dimensions of the map, and count the number of cucumbers facing
    # east and south
    for line in f:
        # Update dimensions
        height += 1
        width = len( line ) - 1
        # Count cucumbers
        for ch in line:
            if ch == '>':
                nr_east += 1
            elif ch == 'v':
                nr_south += 1

    # Initialize the lists
    cucumbers_east  = [ [ 0, 0 ] for _ in range( nr_east ) ]
    cucumbers_south = [ [ 0, 0 ] for _ in range( nr_south ) ]
    cucumber_map = np.zeros( ( height, width ), dtype=int )

    # Go back to the beginning of the file
    f.seek( 0 )

    # Find all the cucumbers and place them in the map
    idx_east  = 0
    idx_south = 0
    idx_ver   = 0
    for line in f:
        # Run over all the characters
        for idx_hor in range( len( line ) - 1 ):
            # Check if there is a cucumber facing east
            if line[ idx_hor ] == '>':
                cucumber_map[ idx_ver, idx_hor ] = 1
                cucumbers_east[ idx_east ] = [ idx_ver, idx_hor ]
                idx_east += 1

            # Check if there is a cucumber facing south
            elif line[ idx_hor ] == 'v':
                cucumber_map[ idx_ver, idx_hor ] = 2
                cucumbers_south[ idx_south ] = [ idx_ver, idx_hor ]
                idx_south += 1

        idx_ver += 1


################################################################################
# First part
################################################################################

# Function to move the cucumbers one step
def move_one_step( cucumber_map, cucumbers_east, cucumbers_south ):

    # Move the cucumbers facing east
    movements_east = []
    for cuc_i in range( len(cucumbers_east) ):
        # Next tentative location
        next_i = cucumbers_east[cuc_i][0]
        next_j = ( cucumbers_east[cuc_i][1] + 1 ) % len( cucumber_map[0] )
        # Check if the next location is empty
        if cucumber_map[ next_i, next_j ] == 0:
            # If it is empty, add this to the list of movements
            # Save the index, current position and next position
            movements_east.append( [ cuc_i, cucumbers_east[cuc_i], [ next_i, next_j ] ] )
    # Apply the movements
    for move in movements_east:
        cucumbers_east[ move[0] ] = move[ 2 ]
        cucumber_map[ tuple(move[1]) ] = 0
        cucumber_map[ tuple(move[2]) ] = 1

    # Move the cucumbers facing south
    movements_south = []
    for cuc_i in range( len(cucumbers_south) ):
        # Next tentative location
        next_i = ( cucumbers_south[cuc_i][0] + 1 ) % len( cucumber_map )
        next_j = cucumbers_south[cuc_i][1]
        # Check if the next location is empty
        if cucumber_map[ next_i, next_j ] == 0:
            # If it is empty, add this to the list of movements
            # Save the index, current position and next position
            movements_south.append( [ cuc_i, cucumbers_south[cuc_i], [ next_i, next_j ] ] )
    # Apply the movements
    for move in movements_south:
        cucumbers_south[ move[0] ] = move[ 2 ]
        cucumber_map[ tuple(move[1]) ] = 0
        cucumber_map[ tuple(move[2]) ] = 2

    return len( movements_east ) + len( movements_south )

start_time = time.time()


# Move the cucumbers until there are no possible movements
nr_steps = 0
while True:
    # Move one step
    nr_moves = move_one_step( cucumber_map, cucumbers_east, cucumbers_south )
    nr_steps += 1

    # If there are no move movements possible, break the loop
    if nr_moves == 0:
        break

print_map( cucumber_map )


print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The number of steps before the stationary state is: {}".format( nr_steps ))



################################################################################
# Second part
################################################################################


start_time = time.time()


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
