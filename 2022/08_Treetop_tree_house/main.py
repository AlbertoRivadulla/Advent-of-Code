import re

################################################################################
# First part
################################################################################

# Check if a tree in the grid is visible from outside (at least one direction)
def is_visible( grid, i1, i2 ):
    # Check if the tree is at one edge
    if ( i1 == 0 ) or ( i2 == 0 ) or ( i1 == len(grid) - 1 ) or ( i2 == len(grid[0]) - 1 ):
        return True

    # For the rest of the trees, look it all directions
    directions = ( (0, 1), (0, -1), (1, 0), (-1, 0) )
    for direc in directions:
        i1_comp = i1
        i2_comp = i2
        visible = True
        # Iterate until the edge is reached
        while ( i1_comp != 0 ) and ( i2_comp != 0 ) \
          and ( i1_comp != len(grid) - 1 ) and ( i2_comp != len(grid[0]) - 1 ):
            # Move the indices
            i1_comp += direc[ 0 ]
            i2_comp += direc[ 1 ]

            # If the tree at the comp position is taller than the original one,
            # it is not visible and the loop in this direction must be stopped
            if grid[ i1_comp ][ i2_comp ] >= grid[ i1 ][ i2 ]:
                visible = False
                break
        if visible:
            return True

    return False

# Read the grid of trees
grid = []
with open( "input.txt", "r" ) as f:
    grid = [ [ int(char) for char in line.strip() ] for line in f ]

# Compute the number of trees visible from outside
nr_visible = 0
for i1 in range( len( grid ) ):
    for i2 in range( len( grid[0] )):
        if is_visible( grid, i1, i2 ):
            nr_visible += 1


print("\n\n--------------\nFirst part\n\n")
print("Number of trees visible from outside: {}".format( nr_visible ))



################################################################################
# Second part
################################################################################

def compute_scenic_score( grid, i1, i2 ):
    # Check if the tree is at one edge
    if ( i1 == 0 ) or ( i2 == 0 ) or ( i1 == len(grid) - 1 ) or ( i2 == len(grid[0]) - 1 ):
        # In this case, one of its sides will see no trees, so its score is zero
        return 0

    # For the rest of the trees, look it all directions
    directions = ( (0, 1), (0, -1), (1, 0), (-1, 0) )
    scenic_score = 1
    for direc in directions:
        i1_comp = i1
        i2_comp = i2
        trees_in_direction = 0
        # Iterate until the edge is reached
        while ( i1_comp != 0 ) and ( i2_comp != 0 ) \
          and ( i1_comp != len(grid) - 1 ) and ( i2_comp != len(grid[0]) - 1 ):
            # Move the indices
            i1_comp += direc[ 0 ]
            i2_comp += direc[ 1 ]

            # Add one to the number of trees seen in that direction
            trees_in_direction += 1

            # If the tree at the comp position is taller than the original one,
            # stop looking in that direction
            if grid[ i1_comp ][ i2_comp ] >= grid[ i1 ][ i2 ]:
                break
        # Multiply the scenic score by the number of trees that can be seen in
        # this direction
        scenic_score *= trees_in_direction
    return scenic_score

# Compute the maximum scenic score of a tree in the grid
best_scenic_score = 0
for i1 in range( len( grid ) ):
    for i2 in range( len( grid[0] )):
        best_scenic_score = max( best_scenic_score, compute_scenic_score( grid, i1, i2 ))

print("\n\n--------------\nSecond part\n\n")
print("The best scenic score found is: {}".format( best_scenic_score ))
