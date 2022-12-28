import re
import numpy as np

# Function to print the cave configuration
def print_cave( cave ):
    string = ''
    for y in range( len(cave[0]) ):
        this_line = [ '.' for _ in range(7) ]
        for x in range( len(cave) ):
            if cave[x][-y-1] == 1:
                this_line[x] = '#'
        string += ''.join(this_line) + '\n'
    print( string )
    return

rocks_string = '''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''.split( "\n" )

# Read the rock shapes from the string
rocks = []
this_rock_lines = []
for line in rocks_string:
    if line == '':
        # Parse this rock into coordinates
        this_rock_coords = []
        for i in range( len( this_rock_lines ) ):
            for j in range( len( this_rock_lines[0] ) ):
                if this_rock_lines[i][j] == '#':
                    # this_rock_coords.append( [ len(this_rock_lines) - x - 1, y ] )
                    this_rock_coords.append( [ j, len(this_rock_lines) - i - 1 ] )
        rocks.append( this_rock_coords )

        # Empty this rock
        this_rock_lines = []

    else:
        this_rock_lines.append( line )

# Get the size of the largest rock
height_largest = 0
for rock in rocks:
    for point in rock:
        if point[1] > height_largest:
            height_largest = point[1]
height_largest += 1

# Read the string of movements
movements = ''
with open( "input.txt", "r" ) as f:
    movements = f.readline().strip()


################################################################################
# First part
################################################################################

# Find the highest occupied point in the cave
def highest_rock( cave ):
    height = 0
    for y in range( len( cave[0] ) ):
        if sum(cave[:,y]) == 0:
            break
        else:
            height = y
    return height

# Check if the next position of a rock is allowed (no collisions)
def valid_position( cave, rock, pos ):
    # For the points in the rock:
    for point in rock:
        # Check if the point is off-bounds at the left or right
        if point[0] + pos[0] < 0 or point[0] + pos[0] >= len(cave):
            return False

        # Check if there is a rock at that point
        if cave[ point[0]+pos[0], point[1]+pos[1] ] == 1:
            return False

    return True

# Number of rocks
nr_rocks = 2022
# nr_rocks = 3

# Vertical and horizontal offsets for the rocks to appear
x_offset = 2
y_offset = 3

# Initialize the cave
#   0 -> empty
#   1 -> rock / floor
cave = np.array( [ [ 0 for _ in range( (nr_rocks + 1) * height_largest + y_offset + 1 ) ] for _ in range(7) ], dtype=int )
# Draw the floor
for x in range(7):
    cave[x][0] = 1

# Drop the rocks in the cave
movement_index = 0
rock_index = 0

for i in range( nr_rocks ):
    # Pick the rock and move the index to the next one
    this_rock = rocks[ rock_index ]
    rock_index = ( rock_index + 1 ) % len( rocks )

    # Find the point at which it has to start
    pos = [ x_offset, highest_rock( cave ) + y_offset + 1 ]

    # Move the rock until it reaches its final position
    can_move = True
    delta = np.array( [ 0, 0 ], dtype=int )
    while can_move:
        # Move left/right
        this_movement = movements[movement_index]
        movement_index = ( movement_index + 1 ) % len( movements )
        delta[1] = 0
        if this_movement == '<':
            delta[0] = -1
        elif this_movement == '>':
            delta[0] = +1

        if valid_position( cave, this_rock, pos + delta ):
            pos += delta

        # Move down
        delta[0] = 0
        delta[1] = -1
        if valid_position( cave, this_rock, pos + delta ):
            pos += delta
        else:
            # If it cannot move down, stop
            can_move = False

    # Draw the cave at the point
    for point in this_rock:
        cave[ point[0] + pos[0], point[1] + pos[1] ] = 1

    # print_cave( cave )


print("\n\n--------------\nFirst part\n\n")
print("Height of the tower: {}".format( highest_rock( cave ) ))



################################################################################
# Second part
################################################################################


print("\n\n--------------\nSecond part\n\n")
print("Second part not implemented")
