import re

################################################################################
# First part
################################################################################

# Move the an element following the other one
def move_element( head, tail ):
    # Compute the differences in position
    hor_diff = head[0] - tail[0]
    ver_diff = head[1] - tail[1]

    # Check if they are touching
    if ( abs( hor_diff ) <= 1 ) and ( abs( ver_diff ) <= 1 ):
        return tail

    # Otherwise, move the tail until they are touching
    tail_new = tail

    # Check if they are separated more than one cell horizontally
    if abs( hor_diff ) > 1:
        # Move in the horizontal direction
        tail_new[0] += hor_diff / abs( hor_diff )
        # Check if they are separated diagonally
        if abs( ver_diff ) >= 1:
            tail_new[1] += ver_diff / abs( ver_diff )
        return tail_new

    # Check if they are separated more than one cell vertically
    if abs( ver_diff ) > 1:
        # Move in the vertical direction
        tail_new[1] += ver_diff / abs( ver_diff )
        # Check if they are separated diagonally
        if abs( hor_diff ) >= 1:
            tail_new[0] += hor_diff / abs( hor_diff )
        return tail_new

    return tail_new

# Movement directions
directions = { "U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0) }

# Read the movements
movements = []
with open( "input.txt", "r" ) as f:
    for line in f:
        match = re.findall( r"([UDLR])\s([0-9]+)", line )
        if match:
            movements.append( [ match[0][0], int( match[0][1] ) ] )


# Count the different points visited by the tail
visited_tail = { ( 0, 0 ) }
pos_head = [ 0, 0 ]
pos_tail = [ 0, 0 ]
for move in movements:
    # Move the head
    for step in range( move[1] ):
        pos_head[ 0 ] += directions[move[0]][0]
        pos_head[ 1 ] += directions[move[0]][1]

        # Move the tail
        pos_tail = move_element( pos_head, pos_tail )

        # Add the position of the tail to the set of visited positions
        visited_tail.add( ( pos_tail[0], pos_tail[1] ) )


print("\n\n--------------\nFirst part\n\n")
print("The amount of different points visited by the tail is: {}".format( len( visited_tail ) ))



################################################################################
# Second part
################################################################################

# Count the different points visited by the tail
visited_tail = { ( 0, 0 ) }
# Now the rope has ten elements
nr_elements = 10
positions = [ [ 0, 0 ] for _ in range( nr_elements ) ]
for move in movements:
    # Move the head
    for step in range( move[1] ):
        positions[0][ 0 ] += directions[move[0]][0]
        positions[0][ 1 ] += directions[move[0]][1]

        # Move the rest of the elements following it
        for i in range( 1, nr_elements ):
            positions[ i ] = move_element( positions[ i-1 ], positions[ i ] )

        # Add the position of the tail to the set of visited positions
        visited_tail.add( ( positions[-1][0], positions[-1][1] ) )


print("\n\n--------------\nSecond part\n\n")
print("The amount of different points visited by the tail is: {}".format( len( visited_tail ) ))
