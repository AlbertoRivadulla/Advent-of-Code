import re
import numpy as np

# Function to draw the map of the cave to the screen
def draw_map( grid ):
    string = "\n"
    for line in grid:
        for el in line:
            if el == 0:
                string += '.'
            elif el == 1:
                string += '#'
            elif el == 2:
                string += 'o'
        string += '\n'
    string += '\n'
    print( string )

# Function to initialize the map of the cave
def initialize_cave( map_instructions, x_min, x_max, y_min, y_max ):
    # Initialize the grid
    #   0 -> air
    #   1 -> rock
    #   2 -> sand
    grid = np.zeros( ( y_max - y_min + 2, x_max - x_min + 3 ), dtype=int )

    # Draw the map of the cave
    for instr in map_instructions:
        for i in range( len(instr) - 1 ):
            # Current and next points
            current_point = instr[i].copy()
            next_point = instr[i + 1].copy()
            # Compute the delta that I have to advance in each step
            delta = next_point - current_point
            delta = delta / np.linalg.norm( delta )
            delta = delta.astype( int )

            # Draw rock walls until the next point is reached
            while not np.array_equal( next_point, current_point ):
                grid[ current_point[1] - y_min, current_point[0] - x_min + 1 ] = 1
                current_point += delta

            # Draw the last point
            grid[ current_point[1] - y_min, current_point[0] - x_min + 1 ] = 1
    return grid

# Read the instructions to draw the map
map_instructions = []
with open( "input.txt", "r" ) as f:
    for line in f:
        these_coords = []
        # Read the instructions in this line
        match = re.findall( r"([0-9]+,[0-9]+)", line )
        if len( match ) > 0:
            for pair in match:
                coords = np.array( [ int(coord) for coord in pair.split(',') ] )
                these_coords.append( coords )
            map_instructions.append( these_coords )

# Get the minimum and maximum values of x and y in the grid
x_min = np.inf
x_max = 0
y_min = 0
y_max = 0

for instr in map_instructions:
    for pair in instr:
        x_min = min( x_min, pair[0] )
        x_max = max( x_max, pair[0] )
        y_min = min( y_min, pair[1] )
        y_max = max( y_max, pair[1] )
x_min = int( x_min )

# Get the map of the cave
grid = initialize_cave( map_instructions, x_min, x_max, y_min, y_max )
draw_map( grid )


################################################################################
# First part
################################################################################

# Function to pour sand to the cave until some falls into the abyss
def pour_sand_until_overflow( grid, origin, x_min, y_min ):
    # Origin in local coordinates
    local_origin = origin.copy()
    local_origin[0] -= x_min - 1
    local_origin[1] -= y_min

    # Drop units of sand until one falls off the bottom
    sand_into_abyss = False
    while not sand_into_abyss:
        # Start always at the local origin
        point = local_origin.copy()
        # Let it go down until there are no more points available
        # while True:
        while not sand_into_abyss:
            # If the sand has gone over the limits, stop the evolution
            # if point[0] > len( grid[0] ) - 2 or point[0] < 1 or point[1] > len( grid ) - 3:
            if point[1] >= len( grid ) - 2:
                sand_into_abyss = True
                break

            # Try to go down
            if grid[ point[1] + 1, point[0] ] == 0:
                point[1] += 1
                continue

            # Try to go down and to the left
            if grid[ point[1] + 1, point[0] - 1 ] == 0:
                point[1] += 1
                point[0] -= 1
                continue

            # Try to go down and to the right
            if grid[ point[1] + 1, point[0] + 1 ] == 0:
                point[1] += 1
                point[0] += 1
                continue

            # If none of the previous movements are allowed, the sand unit reached
            # a stationary point.
            # Draw it to the map
            grid[ point[1], point[0] ] = 2
            break

    return

# Point where the sand falls from
sand_origin = [ 500, 0 ]
# Pour sand to the cave system
pour_sand_until_overflow( grid, sand_origin, x_min, y_min )
draw_map( grid )

# Count the units of sand after pouring sand
sand_count = 0
for line in grid:
    for el in line:
        if el == 2:
            sand_count += 1

print("\n\n--------------\nFirst part\n\n")
print("The number of units of sand is: {}".format( sand_count ))



################################################################################
# Second part
################################################################################

# Function to initialize the map of the cave with a floor at the bottom
def initialize_cave_with_floor( map_instructions, x_min, x_max, y_min, y_max ):
    # Initialize the grid
    #   0 -> air
    #   1 -> rock
    #   2 -> sand
    grid = np.zeros( ( y_max - y_min + 3, x_max - x_min + 3 ), dtype=int )

    # Draw the map of the cave
    for instr in map_instructions:
        for i in range( len(instr) - 1 ):
            # Current and next points
            current_point = instr[i].copy()
            next_point = instr[i + 1].copy()
            # Compute the delta that I have to advance in each step
            delta = next_point - current_point
            delta = delta / np.linalg.norm( delta )
            delta = delta.astype( int )

            # Draw rock walls until the next point is reached
            while not np.array_equal( next_point, current_point ):
                grid[ current_point[1] - y_min, current_point[0] - x_min + 1 ] = 1
                current_point += delta

            # Draw the last point
            grid[ current_point[1] - y_min, current_point[0] - x_min + 1 ] = 1

    # Draw the floor of the cave
    for x in range( x_max - x_min + 3 ):
        grid[ -1, x ] = 1

    return grid

# Function to pour sand to the cave until the mountain reaches the origin
def pour_sand_until_origin_reached( grid, origin, x_min, y_min ):
    # Origin in local coordinates
    local_origin = origin.copy()
    local_origin[0] -= x_min - 1
    local_origin[1] -= y_min

    # Height of the left and right triangles
    height_triangle_left = np.array( [0, 0], dtype=int )
    height_triangle_right = np.array( [0, 0], dtype=int )

    # Drop units of sand until one stays at the origin
    while True:
        # Start always at the local origin
        point = local_origin.copy()
        # Let it go down until there are no more points available
        while True:

            # Try to go down
            if grid[ point[1] + 1, point[0] ] == 0:
                point[1] += 1
                continue

            # Try to go down and to the left
            # Avoid it from going out of the domain
            if point[0] != 0 and grid[ point[1] + 1, point[0] - 1 ] == 0:
                point[1] += 1
                point[0] -= 1

                # If the sand goes out at the left
                if point[0] == 0:
                    # height_triangle_left = point[1] + y_min
                    height_triangle_left = len( grid ) - point[1] - 2

                continue

            # Try to go down and to the right
            # Avoid it from going out of the domain
            if point[0] != len(grid[0]) - 1 and grid[ point[1] + 1, point[0] + 1 ] == 0:
                point[1] += 1
                point[0] += 1

                # If the sand goes out at the right
                if point[0] == len( grid[0] ) - 1:
                    # height_triangle_right = point[1] + y_min
                    height_triangle_right = len( grid ) - point[1] - 2

                continue

            # If none of the previous movements are allowed, the sand unit reached
            # a stationary point.
            # Draw it to the map
            grid[ point[1], point[0] ] = 2

            break

        # draw_map( grid )

        # If the sand cannot leave the origin, break the loop
        if np.array_equal( point, local_origin ):
            break

    return height_triangle_left, height_triangle_right




# Restart the map of the cave
grid = initialize_cave_with_floor( map_instructions, x_min, x_max, y_min, y_max )
# draw_map( grid )

# Point where the sand falls from
sand_origin = [ 500, 0 ]
# Pour sand to the cave system
triangle_heights = pour_sand_until_origin_reached( grid, sand_origin, x_min, y_min )
draw_map( grid )

# Count the units of sand after pouring sand
sand_count = 0
for line in grid:
    for el in line:
        if el == 2:
            sand_count += 1
# Add the sand below the triangles at the left and right of the domain
for height in triangle_heights:
    sand_count += int( height * ( height + 1 ) / 2 )

print("\n\n--------------\nSecond part\n\n")
print("The number of units of sand is: {}".format( sand_count ))
