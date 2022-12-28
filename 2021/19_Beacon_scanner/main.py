import re
import numpy as np

def get_position_scanner( data1, data2, pos_scanner_1, transformations, nr_overlapping_desired = 12 ):

    # # Iterate over the points from the second scanner
    # for i2 in range( len( data2 ) ):
    #     # Iterate over the points from the first scanner
    #     for i1 in range( len( data1 ) ):
    #         # print("{} {}".format( i1, i2 ))
    #         # Iterate over the transformations
    #         for itrans in range( len( transformations ) ):
    #             # Assume both points are the same. 
    #             # Then, the position of the 2nd scanner is:
    #             # pos_scanner_2 = data1[i1] - np.matmul( transformations[itrans], data2[i2] )
    #             # pos_scanner_2 = data1[i1] - data2[i2][itrans]
    #             pos_scanner_2 = data1[i1] - data2[itrans][i2]
    #
    #             # If the two scanners are too far away, do not compare them
    #             if np.any( np.abs( pos_scanner_1 - pos_scanner_2 ) > 2000 ):
    #                 continue
    #
    #             # Find how many points match if this position of the scanner were true
    #             nr_match = 0
    #             for i2_2 in range( len( data2 ) ):
    #                 # Transform the position of the point
    #                 # point_trans = np.matmul( transformations[itrans], data2[i2_2] ) + pos_scanner_2
    #                 # point_trans = data2[i2_2][itrans] + pos_scanner_2
    #                 point_trans = data2[itrans][i2_2] + pos_scanner_2
    #
    #                 # If the point is farther than 1000 in any direction from the
    #                 # other scanner, don't check this point
    #                 if np.any( np.abs( point_trans - pos_scanner_1 ) > 1000 ):
    #                     continue
    #
    #                 # Compare this with all the points of the first scanner
    #                 for i1_2 in range( len( data1 ) ):
    #                     # If they match, add one to the counter
    #                     if np.array_equal( point_trans, data1[i1_2] ):
    #                         nr_match += 1
    #                         # If enough points have matched, I found the location of the scanner
    #                         if nr_match == nr_overlapping_desired:
    #                             return itrans, pos_scanner_2
    #                         break
    #
    #                 # If there are not enough points remaining, break
    #                 if len( data2 ) - i2_2 - 1 < ( nr_overlapping_desired - nr_match ):
    #                     break
    #
    # return 0, np.array( [ np.nan for _ in range( len( data1[0] ) ) ] )

    # Iterate over the transformations
    for itrans in range( len( transformations ) ):
        # Dictionary with the positions of the scanner, and counter
        pos_2_dic = {}
        # Iterate over the points from the second scanner
        for i2 in range( len( data2[itrans] ) ):
            # Iterate over the points from the first scanner
            for i1 in range( len( data1 ) ):
                # Compute the distance
                this_pos_2 = data1[i1] - data2[itrans][i2]

                # Check if this position is already in the list
                this_hash = hash( str(this_pos_2) )
                if this_hash in pos_2_dic.keys():
                    pos_2_dic[this_hash][1] += 1
                    if pos_2_dic[this_hash][1] >= nr_overlapping_desired:
                        return itrans, this_pos_2
                else:
                    pos_2_dic[this_hash] = [ this_pos_2, 1 ]

    return 0, np.array( [ np.nan for _ in range( len( data1[0] ) ) ] )

# Function to generate all the transformation matrices
def generate_transformation_matrices( dimension ):

    # No transformations for 2 dimensions
    if dimension == 2:
        return [ np.identity( 2, dtype=int ) ]

    transformations = []

    # Matrices for rotations of 90 degrees around each axis
    rot_x = np.array( [ [ 1,0,0 ], [ 0,0,-1 ], [ 0,1,0 ] ], dtype=int )
    rot_y = np.array( [ [ 0,0,1 ], [ 0,1,0 ], [ -1,0,0 ] ], dtype=int )
    rot_z = np.array( [ [ 0,-1,0 ], [ 1,0,0 ], [ 0,0,1 ] ], dtype=int )

    # Construct matrices with up to 3 rotations in each direction
    for x in range( 4 ):
        for y in range( 4 ):
            for z in range( 4 ):
                this_rot = np.identity( 3, dtype=int )
                for _ in range(x):
                    this_rot = np.matmul( rot_x, this_rot )
                for _ in range(y):
                    this_rot = np.matmul( rot_y, this_rot )
                for _ in range(z):
                    this_rot = np.matmul( rot_z, this_rot )

                # Check if this rotation is already in the list
                rot_in_list = False
                for rot in transformations:
                    if np.array_equal( rot, this_rot ):
                        rot_in_list = True
                # If it isn't, add it to the list
                if not rot_in_list:
                    transformations.append( this_rot )

    return transformations

################################################################################
# First part
################################################################################

# Get the readings of the scanners
scanners_data = []
with open( "input.txt", "r" ) as f:
    this_scanner_data = []
    for line in f:
        if "scanner" in line:
            continue
        elif line[0] == '\n':
            # End of the set of data of this scanner
            scanners_data.append( this_scanner_data )
            this_scanner_data = []
        else:
            # Add the point to this_scanner_data
            point = [ int(coord) for coord in line.strip().split(',') ]
            this_scanner_data.append( np.array( point ) )
    # Add the data of the last scanner
    scanners_data.append( this_scanner_data )

# Spatial dimensions
dimensions = len( scanners_data[0][0] )

# Get the transformation matrices
transformations = generate_transformation_matrices( dimensions )

# Compute the original data transformed with each matrix
transformed_data = []
for i in range( len( scanners_data ) ):
    trans_data_this_scanner = []
    for k in range( len( transformations ) ):
        trans_data_this_trans = []
        for j in range( len( scanners_data[i] ) ):
            trans_data_this_trans.append( np.matmul( transformations[k], scanners_data[i][j] ) )
        trans_data_this_trans.sort( key=lambda x: x[0] )
        trans_data_this_scanner.append( trans_data_this_trans )
    transformed_data.append( trans_data_this_scanner )

# Positions of the scanners and beacons
scanners_positions = [ np.zeros( dimensions, dtype=int ) for _ in range( len( scanners_data ) ) ]
transform_indices = [ 0 for _ in range( len( scanners_data ) ) ]
scanners_found = [ 0 for _ in range( len( scanners_data ) ) ]
scanners_found[ 0 ] = 1
beacons_positions = set()

# Add the positions of the scanners of the first beacon to the set
for beacon in scanners_data[ 0 ]:
    beacons_positions.add( tuple(beacon) )

while sum( scanners_found ) < len( scanners_data ):
    # Find the overlapping beacons
    print("\nNext loop\n=============\n")
    for i in range( 1, len( scanners_data ) ):
        for j in range( len( scanners_data ) ):
            # Don't compare an scanner with itself
            # If the position of the scanner j is not known, continue
            # If the scanner has already been found, continue
            if i == j or scanners_found[j] == 0 or scanners_found[i] == 1:
                continue

            # print( "Comparing {} and {}".format( i, j ) )

            # Look for the position and transformation of the scanner 
            trans_index, scanner_pos = get_position_scanner( scanners_data[j],
                                                             transformed_data[i],
                                                             scanners_positions[j],
                                                             transformations,
                                                             12 )
                                                            # 3 )

            # If it was found, break the loop
            # if scanner_pos.any():
            if not np.any( np.isnan( scanner_pos ) ):
                # Mark this scanner as found, and save its position and transformation
                scanners_found[ i ] = 1
                transform_indices[ i ] = trans_index
                # scanners_positions[ i ] = scanners_positions[ j ] + scanner_pos
                scanners_positions[ i ] = scanner_pos

                # Update the position of the beacons
                for k in range( len( scanners_data[ i ] ) ):
                    scanners_data[i][k] = transformed_data[i][trans_index][k] + scanner_pos
                    # scanners_data[i][k] = np.matmul( transformations[trans_index],
                    #                                  scanners_data[i][k] ) \
                    #                       + scanner_pos

                # Add these to the set of different beacons
                for beacon in scanners_data[ i ]:
                    beacons_positions.add( tuple(beacon) )

                print( "\n--------------\n" )
                print( "Found scanner {} from {}, at {}".format( i, j, scanner_pos ) )
                print( "Transformation index: {}".format( trans_index ) )
                print( "Scanners found: {} of {}\n".format( sum(scanners_found), len(scanners_found) ))

                break

            if scanners_found[ i ]:
                break

# print("Positions of the scanners: ")
# print( scanners_positions )

print("\n\n--------------\nFirst part\n\n")
print("The total amount of beacons is: {}".format( len(beacons_positions) ))

################################################################################
# Second part
################################################################################

# Positions of the scanners computed in another run
# scanners_positions = [np.array([0, 0, 0]), np.array([   26, -4784,  2373]), np.array([   30, -4754,  3575]), np.array([  71,  -13, 1212]), np.array([   46, -1144,  3539]), np.array([  -25, -3564, -1159]), np.array([ 1232, -2394,  1256]), np.array([-1257, -3581, -1281]), np.array([ -31,  171, 3652]), np.array([ -107, -6003,  4795]), np.array([  -79, -2402,  2282]), np.array([ 1210, -3430,  1146]), np.array([   65, -4737,  4855]), np.array([  -41,    71, -1237]), np.array([   81, -4790,   -86]), np.array([    0, -2382,  1111]), np.array([   36, -1088,  1126]), np.array([   57, -3497,  2322]), np.array([ -78, 1232,  -64]), np.array([-1260, -4769,   -75]), np.array([    4, -5941,  2429]), np.array([-1188, -2336, -1318]), np.array([-1278, -3527,   -66]), np.array([   33, -5990,  1126]), np.array([ 1217, -3540,   -69]), np.array([ 2342, -2296,  1116]), np.array([ -103, -3591,    38]), np.array([-1206,    48,  3477]), np.array([  -70, -5976,  3633]), np.array([   76, -1096,  2344]), np.array([  14,  154, 2399]), np.array([  -83, -3425,  1085]), np.array([ -87, 2453,    6]), np.array([  -79, -3522, -2431]), np.array([   74,    66, -2337]), np.array([ 2358, -2273,    48])]

def Manhattan_distance( point1, point2 ):
    return np.sum( np.abs( point1 - point2 ) )

# Find the largest Manhattan position between two scanners
largest_distance = 0
for pt1 in scanners_positions:
    for pt2 in scanners_positions:
        largest_distance = max( largest_distance, Manhattan_distance( pt1, pt2 ) )

print(len(scanners_positions))

print("\n\n--------------\nSecond part\n\n")
print("Largest Manhattan distance: {}".format( largest_distance ))

