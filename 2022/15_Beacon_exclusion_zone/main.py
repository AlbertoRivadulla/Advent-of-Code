import re
import numpy as np
import math

# Function to compute the Manhattan distance between two points in 2 dimensions
def Manhattan( point1, point2 ):
    delta = point1 - point2
    return abs( delta[0] ) + abs( delta[1] )

# Read the pairs of positions of a sensor and its closest beacon
sensors_and_beacons = []
with open( "input.txt", "r" ) as f:
    for line in f:
        match = re.findall( r"^.+x=(-*[0-9]+),\sy=(-*[0-9]+).+x=(-*[0-9]+),\sy=(-*[0-9]+)$", line )
        if len( match[0] ) == 4:
            # Position of the sensor
            sensor_pos = np.array( [ int(match[0][0]), int(match[0][1]) ], dtype=int )
            # Position of the beacon
            beacon_pos = np.array( [ int(match[0][2]), int(match[0][3]) ], dtype=int )

            # Manhattan distance between them
            distance = Manhattan( sensor_pos, beacon_pos )

            # Save this in the list
            sensors_and_beacons.append( [ sensor_pos, beacon_pos, distance ] )

################################################################################
# First part
################################################################################

# Row where I want to look
y_look = 10
# y_look = 2000000


# Intervals in the line y = y_look that are inside the diamond of a beacon
intervals = []
for pair in sensors_and_beacons:
    # Left and right limits
    x_left  = pair[0][0] - abs( pair[2] - abs( pair[0][1] - y_look ) )
    x_right = pair[0][0] + abs( pair[2] - abs( pair[0][1] - y_look ) )
    # Create the interval if it is valid
    if x_left < x_right and Manhattan( pair[0], [ x_left, y_look ] ) <= pair[2] and \
            Manhattan( pair[0], [x_right, y_look] ) <= pair[2]:
        intervals.append( [ x_left, x_right ] )

# Merge the intervals, which are already sorted by their starting value
intervals.sort( key=lambda x: x[0] )
# Initialize the list of merged intervals with the first one
merged = [ intervals[0] ]

# Iterate over the intervals
for interval in intervals:
    # If the current interval does not overlap with the previous one, append it
    if interval[0] > merged[-1][1]:
        merged.append( interval )
    # Otherwise there is an overlap, so we merge them updating the x_max value 
    # of the last interval in the merged list
    else:
        merged[-1][1] = max( merged[-1][1], interval[1] )

# Compute the amount of points that are inside some interval
nr_positions = 0
for interval in merged:
    nr_positions += interval[1] - interval[0] + 1

# Remove the sensors and beacons that are at the corresponding line
beacons_in_line = []
for pair in sensors_and_beacons:
    if pair[0][1] == y_look or pair[1][1] == y_look:
        if pair[1][0] not in beacons_in_line:
            nr_positions -= 1
            beacons_in_line.append( pair[1][0] )



print("\n\n--------------\nFirst part\n\n")
print("The number of positions where the beacon cannot be in row y = {} is: {}".format( y_look, nr_positions ))



################################################################################
# Second part
################################################################################

# Function to find the segments of points at a given distance of a sensor
def segments_at_distance( sensor, distance, min_coords, max_coords ):
    segments = []

    # Start at the y position of the sensor, and move up and down
    for delta_y in [ -1, 1 ]:
        # There is one segment to the left and one to the right
        for sign_x in [ -1, 1 ]:
            # Start at the y position of the sensor
            y = sensor[1]

            # Initialize variables
            first_point_found = False
            first_point = [ 0, 0 ]
            last_point  = [ 0, 0 ]

            while True:
                point = [ sensor[0] + sign_x * abs( distance - abs( y - sensor[1] ) ), y ]

                # If the point's distance is larger than the one that we want, break
                if Manhattan( sensor, point ) > distance:
                    break

                # If we go outside the interval, break
                if point[0] < min_coords or point[0] > max_coords or point[1] < min_coords or point[1] > max_coords:
                    y += delta_y
                    continue

                # If the first point had not been found yet, save this one
                if not first_point_found:
                    first_point = point
                    first_point_found = True

                # Move in y
                y += delta_y

                # Update the last point
                last_point = point

            try:
                # Construct the segment from the first and last points
                b = ( last_point[1] - first_point[1] ) / ( last_point[0] - first_point[0] )
                a = first_point[1] - b * first_point[0]
                if not math.isnan( b ):
                    segments.append( [ first_point[0], last_point[0], a, b ] )
            except:
                continue

    return segments


# Maximum and minimum values of the coordinates
min_coords = 0
# max_coords = 20
max_coords = 4000000

# Find all segments of points at distance d+1 from a sensor, and inside the given domain
segments_outside_sensors = []
for pair in sensors_and_beacons:
    segments_outside_sensors.append( segments_at_distance( pair[0], pair[2]+1, min_coords, max_coords ) )

# Find the position of the beacon
position_beacon = []
for segments_1 in segments_outside_sensors:
    # point_found = False
    # Iterate over the other sets of segments
    for segments_2 in segments_outside_sensors:
        if segments_1 == segments_2:
            continue
        # Find the points where they meet
        points = []
        for seg_1 in segments_1:
            for seg_2 in segments_2:
                x = - ( seg_1[2] - seg_2[2] ) / ( seg_1[3] - seg_2[3] )
                y = seg_1[2] + seg_1[3] * x

                # Check that the point is inside the limits of the two segments
                if x >= seg_1[0] and x <= seg_1[1] and x >= seg_2[0] and x <= seg_2[1] \
                        and not math.isnan(x):
                    points.append( [ x, y ] )

        # Iterate over the points
        if len( points ) > 0:
            point_found = True
            for point in points:
                # Check if this point is outside the diamond of all beacons
                for pair in sensors_and_beacons:
                    if Manhattan( point, pair[0] ) <= pair[2]:
                        point_found = False
                        break

                # If I found the point, break
                if point_found:
                    position_beacon = point
                    break


print("\n\n--------------\nSecond part\n\n")
print("Position of the beacon: {}".format( position_beacon ))
print("Frequency: {}".format( int( position_beacon[0] * 4000000 + position_beacon[1] ) ))
