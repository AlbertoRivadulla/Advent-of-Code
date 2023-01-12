import time
import re
import heapq

# Function to parse the map into a state tuple
def parse_initial_state( lines ):
    # Initialize the state with the empty corridor
    initial_state = [ [0] for _ in range(11) ]

    # Read the positions of the amphipods in the rooms
    #   A -> 1
    #   B -> 2
    #   C -> 3
    #   D -> 4
    for line in lines[ 2 : len(lines) - 1 ]:
        for i in range( 2, 9, 2 ):
            initial_state[i].append( ord(line[i+1]) - ord("A") + 1 )

    # Convert the state to a tuple of tuples, so it can be used as a key to a dic,
    # and return it
    return tuple( tuple( column ) for column in initial_state )

# Function to check if all the amphipods are located in their rooms
def check_all_sorted( state ):
    # a iterates over the values of the amphipods ( ( 1, 2, 3, 4 ), corresponding
    # to ( A, B, C, D ) )
    # 2*a is the index of the room that they should be located in
    return all( all( a == b for b in state[2*a][1:] ) for a in range( 1, 5 ) )

# Function to get the next possible movements from a current state
def get_next_movements( state ):
    # Initialize lists of movements
    priority_moves, other_moves = [], []

    # Iterate over the columns of the current state
    for i1, src_col in enumerate( state ):

        # Only consider the locations where there is an amphipod (this is, a != 0)
        # in the following loop
        for j1, amph in enumerate( src_col ):
            if amph:
                break
        else:
            # If there is no amphipod in this column, continue to the next one
            continue

        # If the amphipod is at its corresponding room and there are no other 
        # different amphipods in the current room, continue.
        if i1 == 2*amph and not any( b and b != amph for b in src_col ):
            continue

        # Iterate over the state to find the possible destination
        for i2, dst_col in enumerate( state ):
            # If I am at the source room or the corridor to get to the destination
            # is blocked, continue
            if i1 == i2 or any( state[i3][0] for i3 in ( range(i1 + 1, i2) if i1 < i2 else \
                                                         range(i2 + 1, i1) ) ):
                continue

            # Find the first empty position in the destination column, starting
            # from the bottom.
            for j2 in range( len( dst_col ) - 1, -1, -1 ):
                if not dst_col[ j2 ]:
                    break
            # If there is no available position, continue to the next possible
            # destination column.
            else:
                continue

            # If this movement leaves the amphipod at its corresponding room,
            # add it to the list of prioritary movements
            if i2 == 2 * amph:
                if all( not b or b == amph for b in dst_col ):
                    priority_moves.append( ( amph, i1, j1, i2, j2 ) )

            # Else, if the destination is a corridor location that is not 
            # directly in front to a room and the destination position is empty, 
            # add it to the list of non-prioritary movements
            elif i2 not in range( 2, 9, 2 ):
                if i1 in range( 2, 9, 2 ) and not dst_col[0]:
                    other_moves.append( ( amph, i1, j1, i2, j2 ) )

            # The other two options would be:
            #   - Amphipod moving to a room other than its destination.
            #   - Amphipod moving to a corridor location right in front of a room.
            # These two are forbidden, so I do not consider them

    return priority_moves, other_moves

# Function to solve the system, finding the minimum energy necessary to sort the
# amphipods in their rooms
def find_minimum_energy( initial_state ):
    # Dictionary of visited state
    #   { state : energy cost }
    # Notice that state is a tuple, so it can be used as a key to the dictionary
    visited = { initial_state : 0 }

    # Queue of states to visit
    # I initialize this with a list, which then will be treated as a heap
    #   ( energy cost, state )
    states_queue = [ ( 0, initial_state ) ]

    # Propagate the states in the queue
    while states_queue:

        # Get the next state from the queue and the cost for getting to that state.
        # This always gets the smallest element (the one with the smallest first 
        # value, the energy cost).
        _, state = heapq.heappop( states_queue )
        cost = visited[ state ]

        # Check if all amphipods are located in their corresponding room.
        # If they are, the best configuration has been found.
        if check_all_sorted( state ):
            # Return the result
            return cost

        # Get the next movements
        priority_moves, other_moves = get_next_movements( state )

        # Compute the cost of the movements and save them for the next iteration.
        # If there are prioritary movements, only consider the first of them (the
        # one that moves the amphipod with the lowest cost).
        for a, i1, j1, i2, j2 in [ priority_moves[0] ] if priority_moves else other_moves:
            # Compute the new cost.
            # The cost per step is:
            #   A -> 1
            #   B -> 10
            #   C -> 100
            #   D -> 1000
            new_cost = cost + 10 ** ( a - 1 ) * ( abs(i1 - i2) + j1 + j2 )

            # Convert the state to a list and update it
            new_state = [ list( col ) for col in state ]
            new_state[ i1 ][ j1 ] = 0
            new_state[ i2 ][ j2 ] = a
            # Convert the list back to a tuple
            new_state = tuple( tuple( col ) for col in new_state )

            # If the state has not been visited or it had been visited before with
            # a larger energy cost, mark it as visited and add it to the heap.
            if new_state not in visited or visited[ new_state ] > new_cost:
                visited[ new_state ] = new_cost
                heapq.heappush( states_queue, ( new_cost, new_state ) )

                # print( states_queue )

                # print( states_queue.sort() )
                # print( states_queue )




################################################################################
# First part
################################################################################

start_time = time.time()


# Read the map from the file
file_lines = []
with open( "input.txt", "r" ) as f:
    for line in f:
        file_lines.append( line )

# Parse it into a state tuple
initial_state = parse_initial_state( file_lines )

# Compute the minimum energy to sort the amphipods
minimum_energy = find_minimum_energy( initial_state )


print("\n\n--------------\nFirst part\n\n")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The minimum energy to sort them is: {}".format( minimum_energy ))



################################################################################
# Second part
################################################################################

start_time = time.time()

# New lines of the map
new_lines = \
'''  #D#C#B#A#
  #D#B#A#C#'''.split('\n')
# Last two lines of the map
last_two_lines = [ file_lines.pop() for _ in range( 2 ) ]
last_two_lines.reverse()
# Insert the new lines
for new_line in new_lines:
    file_lines.append( new_line )
# Insert the previous last lines again
for line in last_two_lines:
    file_lines.append( line )

# Parse it into a state tuple
initial_state = parse_initial_state( file_lines )

# Compute the minimum energy to sort the amphipods
minimum_energy = find_minimum_energy( initial_state )


print("\n\n--------------\nSecond part\n\n")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The minimum energy to sort them is: {}".format( minimum_energy ))
