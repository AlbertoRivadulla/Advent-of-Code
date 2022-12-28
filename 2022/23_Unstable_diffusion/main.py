import time
import re
import numpy as np
from copy import deepcopy
from collections import defaultdict

# Read the positions of the elves
initial_elves = []
with open( "input.txt", "r" ) as f:
    i = 0
    for line in f:
        line = line.strip()
        for j in range( len( line ) ):
            if line[ j ] == '#':
                initial_elves.append( np.array( [i, j], dtype=int) )
        i += 1

################################################################################
# First part
################################################################################

# Eight directions around an elf
DIRECTIONS = [
    np.array( [-1,-1], dtype=int ),
    np.array( [-1, 0], dtype=int ),
    np.array( [-1, 1], dtype=int ),
    np.array( [ 0, 1], dtype=int ),
    np.array( [ 1, 1], dtype=int ),
    np.array( [ 1, 0], dtype=int ),
    np.array( [ 1,-1], dtype=int ),
    np.array( [ 0,-1], dtype=int ),
]

# List of instructions to follow
# The first three elements of each item are the directions in which the elf has 
# to look, and the final one is the position that it should move to if the other
# three are empty
INSTRUCTIONS = [
    # If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    [
        np.array( [-1,-1], dtype=int ),
        np.array( [-1, 0], dtype=int ),
        np.array( [-1, 1], dtype=int ),
        np.array( [-1, 0], dtype=int )
    ],
    # If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    [
        np.array( [ 1,-1], dtype=int ),
        np.array( [ 1, 0], dtype=int ),
        np.array( [ 1, 1], dtype=int ),
        np.array( [ 1, 0], dtype=int )
    ],
    # If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    [
        np.array( [-1,-1], dtype=int ),
        np.array( [ 0,-1], dtype=int ),
        np.array( [ 1,-1], dtype=int ),
        np.array( [ 0,-1], dtype=int )
    ],
    # If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
    [
        np.array( [-1, 1], dtype=int ),
        np.array( [ 0, 1], dtype=int ),
        np.array( [ 1, 1], dtype=int ),
        np.array( [ 0, 1], dtype=int )
    ],
]

# Function to create the map of the ground and modify the initial positions of
# the elves to take into account the number of rounds that they will be moving
def initialize_map( n_rounds, initial_elves ):
    elves = deepcopy( initial_elves )

    # Find the minimal and maximal values of the coordinates of the elves
    min_i = np.inf
    max_i = -np.inf
    min_j = np.inf
    max_j = -np.inf
    for elf in elves:
        min_i = min( elf[0], min_i )
        max_i = max( elf[0], max_i )
        min_j = min( elf[1], min_j )
        max_j = max( elf[1], max_j )
    min_i = int( min_i )
    max_i = int( max_i )
    min_j = int( min_j )
    max_j = int( max_j )

    # Move the elves so that they are inside the map after extending it
    for elf in elves:
        elf[0] += n_rounds - min_i
        elf[1] += n_rounds - min_j

    # Create the map, extending the initial ground n_rounds in each side
    ground = np.zeros( ( max_i - min_i + 2*n_rounds + 1,
                         max_j - min_j + 2*n_rounds + 1), dtype=int )

    # Position the elves in the map
    for elf in elves:
        ground[ tuple(elf) ] = 1

    return elves, ground


# Move the elves in the ground one step
def move_elves_one_round( elves, ground, instr_ind ):

    # First half: propose movements
    movements = defaultdict( list )
    for i in range( len( elves ) ):
        # If the eight positions around the elf are empty, the elf does not do 
        # anything
        alone = True
        for direction in DIRECTIONS:
            if ground[ tuple( elves[i] + direction ) ] == 1:
                alone = False
                break
        if alone:
            continue

        # Test the conditions for the four instructions in order.
        # The first one that is fulfilled determines the proposed movement.
        for j in range( 4 ):
            # Check if the 3 positions in the current instruction are empty
            instr_valid = True
            j_instr = ( j + instr_ind ) % 4
            for k in range( 3 ):
                if ground[ tuple( elves[i] + INSTRUCTIONS[j_instr][k] ) ] == 1:
                    instr_valid = False
                    break
            if instr_valid:
                movements[ tuple( elves[i] + INSTRUCTIONS[j_instr][3] ) ].append( i )
                break

    # Second half: apply the movements if they do not coincide (counting the 
    # number of movements applied applied)
    nr_moves = 0
    for location, indices in movements.items():
        # Only move if there is only one elf going to that location
        if len( indices ) == 1:
            # Eliminate the last position of the elf in the map
            ground[ tuple(elves[ indices[0] ]) ] = 0

            # Move the elf
            elves[ indices[0] ] = np.array( location, dtype=int )

            # Place the elf in the map again
            ground[ tuple(elves[ indices[0] ]) ] = 1

            # Count the number of moves
            nr_moves += 1

    return nr_moves == 0


# Function to move the elves in the map a given amount of rounds
def move_elves( n_rounds, initial_elves ):
    # Initialize the map
    elves, ground = initialize_map( n_rounds, initial_elves )

    # Move the elves the number of rounds given
    instr_index = 0
    no_moves = False
    for rnd in range( n_rounds ):
        # print("Round {} of {}".format( rnd, n_rounds ))

        # Move the elves in another function
        no_moves = move_elves_one_round( elves, ground, instr_index )
        # After each round, the first instruction in the list is the next one
        instr_index += 1

        # If there are no valid moves, break
        if no_moves:
            return elves, rnd

    return elves, n_rounds

# Compute the number of empty tiles in the ground covered by the elves in the 
# given state
def compute_empty_tiles( elves ):
    # Find the minimal and maximal values of the coordinates of the elves
    min_i = np.inf
    max_i = -np.inf
    min_j = np.inf
    max_j = -np.inf
    for elf in elves:
        min_i = min( elf[0], min_i )
        max_i = max( elf[0], max_i )
        min_j = min( elf[1], min_j )
        max_j = max( elf[1], max_j )

    # Compute the number of empty tiles
    nr_empty = ( max_i - min_i + 1 ) * ( max_j - min_j + 1 ) - len( elves )

    return nr_empty



start_time = time.time()

# Number of rounds
n_rounds = 10

# Move the elves the amount of rounds given
final_elves, nr_rounds_final = move_elves( n_rounds, initial_elves )

# Compute the number of empty tiles in the ground covered by the elves
empty_tiles = compute_empty_tiles( final_elves )


print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The number of empty tiles in the final state after {} rounds is: {}".format( nr_rounds_final, empty_tiles ))



################################################################################
# Second part
################################################################################


start_time = time.time()

# Number of rounds
n_rounds = 10000

# Move the elves the amount of rounds given
final_elves, nr_rounds_final = move_elves( n_rounds, initial_elves )

# Compute the number of empty tiles in the ground covered by the elves
empty_tiles = compute_empty_tiles( final_elves )


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The number of empty tiles in the final state is: {}".format( empty_tiles ))
print("Number of movements before stabilization: {}".format( nr_rounds_final + 1 ))
