import re

from collections import deque

# Function to get the value of a character
def char_to_value( char ):
    # Take the ASCII value of the lowercase version of the character
    # Subtract 96, the value before "a"
    value = ord( char.lower() ) - 96
    return value

# Function to get the available neighbors to visit
def get_neighbors_to_visit( pos, heightmap, visited ):
    # Four possible directions
    directions = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    available_neighbors = []
    # Check all directions
    for direc in directions:
        next_pos = [ pos[0] + direc[0], pos[1] + direc[1] ]
        # If this next position is outside the map, do not consider it
        if next_pos[0] < 0 or next_pos[0] >= len(heightmap) or \
          next_pos[1] < 0 or next_pos[1] >= len(heightmap[0]):
            continue

        # Check that the height of the neighbor is at most 1 more than at the
        # current position
        if heightmap[next_pos[0]][next_pos[1]] - heightmap[pos[0]][pos[1]] <= 1:
            available_neighbors.append( next_pos )

    return available_neighbors


# Read the heightmap
heightmap = []
initial_pos = []
goal = []
with open( "input.txt", "r" ) as f:
    # Read the entire file first
    lines = []
    for line in f:
        lines.append( line.strip() )

    # Initialize the map
    heightmap = [ [ 0 for _ in range(len(lines[0])) ] for _ in range(len(lines)) ]

    # Parse each line
    for i in range( len( lines ) ):
        for j in range( len( lines[0] ) ):
            # If this is the starting position
            if lines[i][j] == 'S':
                initial_pos = [ i, j ]
                # The height at the starting position is equal to the minimum one
                heightmap[i][j] = 1
                continue

            # If this is the goal
            if lines[i][j] == "E":
                goal = [ i, j ]
                # The height at the destination is equal to the maximum one
                heightmap[i][j] = char_to_value( 'z' )
                continue

            # Else, get its numerical value and add it to the map
            heightmap[i][j] = char_to_value( lines[i][j] )

# Function to get the shortest path length from a given starting position
def get_shortest_path_length( starting_position, heightmap, goal_position ):
    # Visited cells
    visited = [ [ 0 for _ in range(len(heightmap[0])) ] for _ in range(len(heightmap)) ]

    # Positions to test
    positions_to_test = deque( [ starting_position ] )

    # Minimum path lengths
    init_length = len( heightmap[0] ) * len( heightmap )
    length_to_arrive = [ [ init_length for _ in range(len(heightmap[0])) ] for _ in range(len(heightmap)) ]
    length_to_arrive[starting_position[0]][starting_position[1]] = 0

    # Visited positions
    visited = [ [ 0 for _ in range(len(heightmap[0])) ] for _ in range(len(heightmap)) ]
    nr_visited = 0

    while len( positions_to_test ) > 0:
        # Move to the next node to study
        current = positions_to_test.popleft()
        # If this node was already visited, continue
        if visited[current[0]][current[1]]:
            continue
        else:
            # Set it as visited
            visited[current[0]][current[1]] = 1
            nr_visited += 1

            # Get its neighbors and iterate over them
            for neigh in get_neighbors_to_visit( current, heightmap, visited ):
                positions_to_test.append( neigh )

                # Calculate the possible local score
                new_length = length_to_arrive[current[0]][current[1]] + 1

                # If the node was visited and  this score is smaller than the one it 
                # had previously, update it
                if new_length < length_to_arrive[neigh[0]][neigh[1]]:
                    length_to_arrive[neigh[0]][neigh[1]] = new_length

    # print("Visited {} positions of {}".format( nr_visited, init_length ))

    return length_to_arrive[goal_position[0]][goal_position[1]]


################################################################################
# First part
################################################################################

length_to_goal = get_shortest_path_length( initial_pos, heightmap, goal )

print( initial_pos )

print("\n\n--------------\nFirst part\n\n")
print("The minimum number of steps to reach the goal is: {}".format( length_to_goal ))



################################################################################
# Second part
################################################################################

# # Find all the possible starting positions
# initial_positions = []
# for i in range( len( heightmap ) ):
#     for j in range( len( heightmap[0] ) ):
#         if heightmap[i][j] == 1:
#             initial_positions.append( [ i, j ] )
#
# # Compute the minimum length to the goal from each starting position
# lengths_to_goal = []
# for initial_position in initial_positions:
#     lengths_to_goal.append( get_shortest_path_length( initial_position, heightmap, goal ) )
#
# print("\n\n--------------\nSecond part\n\n")
# print("The shortest path length from any point at the lowest elevation is: {}".format( min( lengths_to_goal ) ))
