import time
import re
import numpy as np
from copy import deepcopy

# Read the map and instructions
instructions = []
with open( "input.txt", "r" ) as f:
    # First pass: get the dimensions of the map and read the instructions at the
    # end
    n_rows    = 0
    n_columns = 0
    reading_map = True
    for line in f:
        # If I got to the blank line, stop reading the map
        if len( line.strip() ) == 0:
            break

        # If I am reading the map, update the dimensions
        n_rows += 1
        n_columns = max( n_columns, len(line[:-1]) )

    # Read the line of instructions
    instr_string = f.readline().strip()
    i = 0
    while i < len( instr_string ):
        # If the current character is a number, read until there are no more numbers
        if instr_string[i].isdigit():
            this_nr = ''
            while i < len( instr_string ):
                # If I got to a non-number character, stop reading the number 
                # and go back
                if not instr_string[i].isdigit():
                    i -= 1
                    break
                # Otherwise, add the digit to the number
                else:
                    this_nr += instr_string[i]
                    i += 1
            # Store the number in the list of instructions
            instructions.append( int( this_nr ) )
        # If the current character is not a number, add it to the list
        else:
            instructions.append( instr_string[i] )
        # Move in the string
        i += 1

    # Go back to the beginning
    f.seek( 0 )

    # Initialize the map
    #   0 -> outside the map
    #   1 -> floor
    #   2 -> wall
    board = np.zeros( ( n_rows, n_columns ), dtype=int)
    i_line = 0
    for line in f:
        # If I got to the end of the map, break
        if len( line.strip() ) == 0:
            break

        # Parse the line up to the last character ( a '\n' )
        for i in range( len( line ) - 1 ):
            if line[i] == ' ':
                # Outside the map
                continue
            elif line[i] == '.':
                # Floor
                board[i_line, i] = 1
            elif line[i] == '#':
                # Wall
                board[i_line, i] = 2

        # Move to the next line
        i_line += 1

# List of directions (right, down, left, up)
directions = [ np.array( [0, 1], dtype=int ),
               np.array( [1, 0], dtype=int ),
               np.array( [0, -1], dtype=int ),
               np.array( [-1, 0], dtype=int )
              ]


################################################################################
# First part
################################################################################

# Move in a board, from a given initial state and following a set of instructions
def move_in_board( initial_state, board, instructions ):
    # Initial state
    state = deepcopy(initial_state)

    # Iterate over the instructions
    i = 0
    while i < len( instructions ):
        # If the instruction is L or R, change the direction
        if instructions[i] == 'L':
            # Rotate counter-clockwise
            state[1] = ( state[1] - 1 ) % 4
        elif instructions[i] == 'R':
            # Rotate clockwise
            state[1] = ( state[1] + 1 ) % 4
        # Otherwise, the instruction is a number and I have to move the amount
        # of steps indicated
        else:
            prev_state = deepcopy( state )
            for _ in range( instructions[i] ):
                # Move to the next position
                state[0] += directions[state[1]]

                # Check if I went off bounds (either outside the floor/walls or
                # outiside the domain)
                off_bounds = False
                if state[0][0] < 0 or state[0][0] >= len(board) or \
                        state[0][1] < 0 or state[0][1] >= len(board[0]):
                    off_bounds = True
                elif board[ tuple(state[0]) ] == 0:
                    off_bounds = True

                # If I go off bounds, go in the opposite direction until I reach
                # the end of the map
                if off_bounds:
                    state[0] += directions[ ( state[1] + 2 ) % 4 ]
                    while board[ tuple(state[0]) ] != 0:
                        state[0] += directions[ ( state[1] + 2 ) % 4 ]

                        # If I go off bounds, break
                        if state[0][0] < 0 or state[0][0] >= len(board) or \
                                state[0][1] < 0 or state[0][1] >= len(board[0]):
                            break

                    # Once I reached the end, go back one step
                    state[0] += directions[ state[1] ]

                    # If there was a wall, go back to the previous state
                    if board[ tuple(state[0]) ] == 2:
                        state[0] = prev_state[0].copy()
                        state[1] = prev_state[1]

                # If I am now in a wall, go back to the previous state and break
                elif board[ tuple(state[0]) ] == 2:
                    state[0] = prev_state[0].copy()
                    state[1] = prev_state[1]
                    break

                # Copy the current state for the next step
                prev_state[0] = state[0].copy()
                prev_state[1] = state[1]

        # Move to the next instruction
        i += 1

    return state

start_time = time.time()

# Find the initial position
# The last number is the direction, 
initial_state = [ np.array( [ 0, 0 ], dtype=int ), 0 ]
# Move to the right until I find a floor tile
while board[ tuple(initial_state[0]) ] != 1:
    initial_state[0] += directions[0]

print(initial_state)

# Move in the map
final_state = move_in_board( initial_state, board, instructions )

# Compute the password
password = 1000 * (final_state[0][0] + 1) + 4 * (final_state[0][1] + 1) + final_state[1]

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Final state: {}".format( final_state ))
print("Password: {}".format( password ))



################################################################################
# Second part
################################################################################

# Function to find all the edges in the cube
def find_edges( board ):
    # Get the cube edge length
    n_tiles = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                n_tiles += 1
    edge_len = int( np.sqrt( n_tiles / 6 ) )

    # Find all the outer edges of the board
    edges = []
    delta_hor = np.array( [0, 1], dtype=int )
    delta_ver = np.array( [1, 0], dtype=int )
    origin    = np.array( [0, 0], dtype=int )

    # Look for the vertical edges
    # Move horizontally
    for i in range( int(len(board[0]) / edge_len) ):
        # Move vertically
        for j in range( int(len(board) / edge_len) ):
            # The following alternates between the beginning and the end
            for k in range( 2 ):
                pt1 = origin + (i*edge_len + (edge_len-1)*k) * delta_hor + j*edge_len * delta_ver
                pt2 = origin + (i*edge_len + (edge_len-1)*k) * delta_hor + (j*edge_len + edge_len-1) * delta_ver
                # Check if there are points here
                if board[tuple(pt1)] != 0 and board[tuple(pt2)] != 0:
                    # If I am at the left border -> edge facing left
                    if i == 0 and k == 0:
                        edges.append( [ pt2, pt1, 2 ] )
                    # If I am at the right border -> edge facing right
                    elif i == int(len(board[0]) / edge_len - 1) and k == 1:
                        edges.append( [ pt1, pt2, 0 ] )
                    # If there are not points at the left -> edge facing left
                    elif k == 0 and board[tuple( pt1 - delta_hor)] == 0:
                        edges.append( [ pt2, pt1, 2 ] )
                    # If there are not points at the right -> edge facing right
                    elif k == 1 and board[tuple( pt1 + delta_hor)] == 0:
                        edges.append( [ pt1, pt2, 0 ] )

    # Look for the vertical edges
    # Move vertically
    for j in range( int(len(board) / edge_len) ):
        # Move vertically
        for i in range( int(len(board[0]) / edge_len) ):
            # The following alternates between the beginning and the end
            for k in range( 2 ):
                pt1 = origin + i*edge_len * delta_hor + (j*edge_len + (edge_len-1)*k) * delta_ver
                pt2 = origin + (i*edge_len + edge_len-1) * delta_hor + (j*edge_len + (edge_len-1)*k) * delta_ver
                # Check if there are points here
                if board[tuple(pt1)] != 0 and board[tuple(pt2)] != 0:
                    # If I am at the upper border -> edge facing up
                    if j == 0 and k == 0:
                        edges.append( [ pt1, pt2, 3 ] )
                    # If I am at the bottom border -> edge facing down
                    elif j == int(len(board) / edge_len - 1) and k == 1:
                        edges.append( [ pt2, pt1, 1 ] )
                    # If there are not points above -> edge facing up
                    elif k == 0 and board[tuple( pt1 - delta_ver)] == 0:
                        edges.append( [ pt1, pt2, 3 ] )
                    # If there are not points below -> edge facing down
                    elif k == 1 and board[tuple( pt1 + delta_ver)] == 0:
                        edges.append( [ pt2, pt1, 1 ] )

    assert len(edges) == 14, "Incorrect amount of external vertices found"

    return edges

# Function to get the index of the next edge after the current one from the list
def get_next_edge( this_ind, edges, clockwise = True ):
    next_ind = 0

    if clockwise:
        while True:
            # Look for an edge joined linearly
            if np.array_equal( edges[this_ind][1] + directions[(edges[this_ind][2]+1)%4],
                               edges[next_ind][0] ):
                return next_ind

            # Look for an edge joined in an outer corner
            if np.array_equal( edges[this_ind][1], edges[next_ind][0] ):
                return next_ind

            # Look for an edge joined in an inner corner
            if np.array_equal( edges[this_ind][1] + directions[edges[this_ind][2]],
                               edges[next_ind][0] + directions[edges[next_ind][2]] ):
                return next_ind

            # Move to the next edge
            next_ind = ( next_ind + 1 ) % len(edges)

    else:
        while True:
            # Look for an edge joined linearly
            if np.array_equal( edges[this_ind][0] + directions[(edges[this_ind][2]-1)%4],
                               edges[next_ind][1] ):
                return next_ind

            # Look for an edge joined in an outer corner
            if np.array_equal( edges[this_ind][0], edges[next_ind][1] ):
                return next_ind

            # Look for an edge joined in an inner corner
            if np.array_equal( edges[this_ind][0] + directions[edges[this_ind][2]],
                               edges[next_ind][1] + directions[edges[next_ind][2]] ):
                return next_ind

            # Move to the next edge
            next_ind = ( next_ind + 1 ) % len(edges)

# Function to find the equivalences between edges
    # Each equivalence has the data of the two edges (initial and final points), 
    # and the relative rotation (nr of indices in the directions list that I have)
    # to advance
def get_cube_equivalences( board ):
    # Get all the edges of the cube with the other function
    edges = find_edges( board )

    # List to mark when an edge has been matched
    matched = [ 0 for _ in range( len( edges ) ) ]

    # List of equivalences between edges
    equivalences = []

    # Start at the first edge and move along a direction parallel to it (its normal + 1, so clockwise movement)
    while sum(matched) < len( edges ) - 2:
        # Pick the first unmatched edge
        this_ind = 0
        next_ind = 0
        for i in range( len( edges ) ):
            found = False
            if matched[i] == 0:
                this_ind = i
                # Move until I reach a point where two edges are joined in an inner corner
                # For this, the normal of the second corner must be that of the first one rotated
                # counter-clockwise (the previous one in the list of directions)
                next_ind = get_next_edge( this_ind, edges )
                while ( edges[next_ind][2] + 1 ) % 4 != edges[this_ind][2]:
                    this_ind = next_ind
                    next_ind = get_next_edge( this_ind, edges )

                # If the edges are not matched yet, break the loop in order to
                # add the equivalence between them
                if matched[ this_ind ] == 0 and matched[ next_ind ] == 0:
                    found = True
                    break
            if found:
                break

        # Rotation delta between two edges
        delta_rot = 1
        while True:
            equivalences.append( [ edges[this_ind], edges[next_ind], delta_rot ] )
            equivalences.append( [ edges[next_ind], edges[this_ind], -delta_rot ] )
            # Mark them as matched
            matched[ this_ind ] = 1
            matched[ next_ind ] = 1

            # Move once more (propagate) along the two edges to check for more 
            # equivalent edges
            next_this_ind = get_next_edge( this_ind, edges, False ) # Counter-clockwise
            next_next_ind = get_next_edge( next_ind, edges, True )  # Clockwise

            # If at least one of the edges is already matched, break this loop
            if matched[ next_this_ind ] == 1 or matched[ next_this_ind ] == 1:
                break

            # If I turn a corner in one direction but not in the other, match the
            # two edges in the next iteration of the loop
            # Else, break the loop
            if not ( ( ( edges[next_ind][2] + 1 ) % 4 == edges[next_next_ind][2] and \
                    edges[next_this_ind][2] == edges[this_ind][2] ) or \
               ( ( edges[next_this_ind][2] + 1 ) % 4 == edges[this_ind][2] and \
                    edges[next_next_ind][2] == edges[next_ind][2] ) ):
                break

            # Move the indices
            this_ind = next_this_ind
            next_ind = next_next_ind

            # Increment the rotation delta
            delta_rot = ( delta_rot + 1 ) % 4


    # If there are only two unmatched edges, match them
    if len(edges) - sum(matched) == 2:
        # Get the two unmatched edges
        unmatched = []
        for i in range( len( edges ) ):
            if matched[i] == 0:
                unmatched.append( i )

        # Add the equivalences to the list
        delta_rot = edges[unmatched[0]][2] - edges[unmatched[1]][2]
        equivalences.append( [ edges[unmatched[0]], edges[unmatched[1]], delta_rot ] )
        equivalences.append( [ edges[unmatched[1]], edges[unmatched[0]], -delta_rot ] )

    # print("\nEquivalences:")
    # for equiv in equivalences:
    #     print(equiv)

    return equivalences

# Get the state after going off-bounds in a cube
def get_position_cube_off_bounds( prev_state, equivalences ):

    next_state = deepcopy( prev_state )

    # Find the edge that I was in
    # This is going to be the first edge of the corresponding equivalence
    equiv_ind = 0
    while True:
        # Horizontal edge (rotation 1 or 3)
        if equivalences[equiv_ind][0][2] % 2 == 1:
            # The vertex must have the same value of the first component, and 
            # the second one must be between the two of the edges
            max_y = max( equivalences[equiv_ind][0][0][1], equivalences[equiv_ind][0][1][1] )
            min_y = min( equivalences[equiv_ind][0][0][1], equivalences[equiv_ind][0][1][1] )
            if prev_state[0][0] == equivalences[equiv_ind][0][0][0] and \
                    prev_state[0][1] <= max_y and prev_state[0][1] >= min_y:
                break

        # Vertical edge (rotation 1 or 3)
        elif equivalences[equiv_ind][0][2] % 2 == 0:
            # The vertex must have the same value of the second component, and 
            # the first one must be between the two of the edges
            max_x = max( equivalences[equiv_ind][0][0][0], equivalences[equiv_ind][0][1][0] )
            min_x = min( equivalences[equiv_ind][0][0][0], equivalences[equiv_ind][0][1][0] )
            if prev_state[0][1] == equivalences[equiv_ind][0][0][1] and \
                    prev_state[0][0] <= max_x and prev_state[0][0] >= min_x:
                break

        equiv_ind += 1

    # Get the distance from the first vertex of the previous edge to the point,
    # along the direction of the edge
    dir_first = equivalences[equiv_ind][0][1] - equivalences[equiv_ind][0][0]
    dir_first = dir_first / np.linalg.norm( dir_first )
    dir_first = dir_first.astype( int )
    test_pos = equivalences[equiv_ind][0][0].copy()
    distance = 0
    while not np.array_equal( test_pos, prev_state[0] ):
        distance += 1
        test_pos += dir_first

    # The final position if the distance computed before from the second vertex
    # of the final edge, along the direction of the edge
    dir_final = equivalences[equiv_ind][1][0] - equivalences[equiv_ind][1][1]
    dir_final = dir_final / np.linalg.norm( dir_final )
    dir_final = dir_final.astype( int )
    next_state[0] = equivalences[equiv_ind][1][1].copy()
    for _ in range( distance ):
        next_state[0] += dir_final

    # Update the direction index
    next_state[1] = ( next_state[1] + equivalences[equiv_ind][2] ) % 4

    return next_state

# Move in a cube, from a given initial state and following a set of instructions
def move_in_cube( initial_state, board, equivalences, instructions ):
    # Initial state
    state = deepcopy(initial_state)

    # Iterate over the instructions
    i = 0
    while i < len( instructions ):
        # If the instruction is L or R, change the direction
        if instructions[i] == 'L':
            # Rotate counter-clockwise
            state[1] = ( state[1] - 1 ) % 4
        elif instructions[i] == 'R':
            # Rotate clockwise
            state[1] = ( state[1] + 1 ) % 4
        # Otherwise, the instruction is a number and I have to move the amount
        # of steps indicated
        else:
            prev_state = deepcopy( state )
            for _ in range( instructions[i] ):
                # Move to the next position
                state[0] += directions[state[1]]

                # Check if I went off bounds (either outside the floor/walls or
                # outiside the domain)
                off_bounds = False
                if state[0][0] < 0 or state[0][0] >= len(board) or \
                        state[0][1] < 0 or state[0][1] >= len(board[0]):
                    off_bounds = True
                elif board[ tuple(state[0]) ] == 0:
                    off_bounds = True

                # If I go off bounds, go in the opposite direction until I reach
                # the end of the map
                if off_bounds:
                    # state = get_position_in_cube( state, prev_state, equivalences )
                    state = get_position_cube_off_bounds( prev_state, equivalences )

                    # If there was a wall, go back to the previous state
                    if board[ tuple(state[0]) ] == 2:
                        state[0] = prev_state[0].copy()
                        state[1] = prev_state[1]

                # If I am now in a wall, go back to the previous state and break
                elif board[ tuple(state[0]) ] == 2:
                    state[0] = prev_state[0].copy()
                    state[1] = prev_state[1]
                    break

                # Copy the current state for the next step
                prev_state[0] = state[0].copy()
                prev_state[1] = state[1]

        # Move to the next instruction
        i += 1

    return state

start_time = time.time()

# Find the equivalences between edges
equivalences = get_cube_equivalences( board )

# Move in the cube, giving the equivalences between edges
final_state = move_in_cube( initial_state, board, equivalences, instructions )

# Compute the password
password = 1000 * (final_state[0][0] + 1) + 4 * (final_state[0][1] + 1) + final_state[1]

print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Final state: {}".format( final_state ))
print("Password: {}".format( password ))
