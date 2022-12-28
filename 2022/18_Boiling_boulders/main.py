import time
import numpy as np
from collections import deque

# Function to check if two 1x1x1 cubes are adjacent
def check_adjacent( pos1, pos2 ):
    # Difference in their positions
    delta = pos1 - pos2

    # If they are adjacent, the separation in one direction is one and in the other
    # two it is zero. This is check in the next condition:
    if np.sum( np.absolute( delta ) ) == 1:
        # They are adjacent
        return True
    else:
        return False

# Read the position of the cubes
pos_cubes = []
with open( "input.txt", "r" ) as f:
    for line in f:
        pos_cubes.append( np.array( [ int(el) for el in line.strip().split(',') ], dtype=int ) )


################################################################################
# First part
################################################################################

start_time = time.time()

# For each cube, find how many adjacent cubes there are
nr_adjacent_cubes = [ 0 for _ in range( len( pos_cubes ) ) ]
for i in range( len( pos_cubes ) ):
    if i % 100 == 0:
        print( "Cube {} of {}".format( i, len(pos_cubes) ))
    nr_adjacent = 0
    for j in range( len( pos_cubes ) ):
        # Skip if both cubes are the same
        if i == j:
            continue
        # Otherwise, check if they are adjacent
        if check_adjacent( pos_cubes[i], pos_cubes[j] ):
            nr_adjacent += 1

    nr_adjacent_cubes[i] = nr_adjacent

# Count the number of faces not covered
nr_not_covered = 6 * len( pos_cubes )
# Subtract the covered faces
for nr_adjacent in nr_adjacent_cubes:
    nr_not_covered -= nr_adjacent

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Total surface area: {}".format( nr_not_covered ))



################################################################################
# Second part
################################################################################

start_time = time.time()

# Minimum and maximum values of the coordinates
coord_min = np.array( [ np.inf, np.inf, np.inf ] )
coord_max = np.array( [ -np.inf, -np.inf, -np.inf ] )

for pos in pos_cubes:
    for i in range( 3 ):
        coord_min[i] = min( coord_min[i], pos[i] )
        coord_max[i] = max( coord_max[i], pos[i] )

coord_min = coord_min.astype( int )
coord_max = coord_max.astype( int )

# Create a 3-dim grid of points
#   0 -> air
#   1 -> lava
#   2 -> steam
grid = np.zeros( ( coord_max[0] - coord_min[0] + 3,
                   coord_max[1] - coord_min[1] + 3,
                   coord_max[2] - coord_min[2] + 3 ), dtype=int )
grid_size = [ len(grid), len(grid[0]), len(grid[0, 0]) ]
# Mark the lava cubes in the grid
# Leave a gap of a single point at the borders
for pos in pos_cubes:
    grid[ pos[0] - coord_min[0] + 1, pos[1] - coord_min[1] + 1, pos[2] - coord_min[2] + 1 ] = 1

# Add steam at the sides of the grid
# Queue of points with steam to propagate
steam_queue = deque()
# Upper and lower sides
for i in range( len( grid[0] ) ):
    for j in range( len( grid[0, 0] ) ):
        grid[0, i, j]  = 2
        grid[-1, i, j] = 2
        steam_queue.append( [0, i, j] )
        steam_queue.append( [len(grid)-1, i, j] )
# Left and right sides
for i in range( len( grid ) ):
    for j in range( len( grid[0, 0] ) ):
        grid[i, 0, j]  = 2
        grid[i, -1, j] = 2
        steam_queue.append( [i, 0, j] )
        steam_queue.append( [i, len(grid[0])-1, j] )
# Front and back sides
for i in range( len( grid ) ):
    for j in range( len( grid[0] ) ):
        grid[i, j, 0]  = 2
        grid[i, j, -1] = 2
        steam_queue.append( [i, j, 0] )
        steam_queue.append( [i, j, len(grid[0, 0])-1] )

# Function to find the directions in which a steam cell can propagate in the grid
def propagate_steam_cell( point, grid, grid_size ):
    # Points to which it can propagate
    next_points = []
    # Number of lava neighbors
    nr_lava_neighbors = 0

    # Try to move up and down in the three directions
    for delta in [-1, 1]:
        # Neighbors in the three directions
        neighs = [ point.copy() for _ in range(3) ]
        for i in range( len( neighs ) ):
            neighs[i][i] += delta

        # If each point is inside bounds, check if it is empty or lava
        for i in range( len( neighs ) ):
            # If it is outside bounds, continue
            if neighs[i][i] < 0 or neighs[i][i] >= grid_size[i]:
                continue

            # If the point is empty, add it to next_points
            if grid[neighs[i][0], neighs[i][1], neighs[i][2]] == 0:
                next_points.append( neighs[i] )

            # If it is lava, add one to nr_lava_neighbors
            elif grid[neighs[i][0], neighs[i][1], neighs[i][2]] == 1:
                nr_lava_neighbors += 1


    return next_points, nr_lava_neighbors

# Propagate the steam inside
steam_cubes_touching = []
nr_surface_faces = 0
while len( steam_queue ) > 0:
    # Get the next point of the queue
    point = steam_queue.popleft()

    # Get the directions in which it can propagate
    # The function also return the number of lava neighbors of the point
    next_points, nr_lava_neighbors = propagate_steam_cell( point, grid, grid_size )

    # Add to the number of surface faces
    nr_surface_faces += nr_lava_neighbors

    # Add the next points to the queue, and mark them as steam
    for next_pt in next_points:
        grid[ next_pt[0], next_pt[1], next_pt[2] ] = 2
        steam_queue.append( next_pt )


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The total exterior area is: {}".format( nr_surface_faces ))
