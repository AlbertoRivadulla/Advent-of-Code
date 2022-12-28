import re
import numpy as np

class CubeRegion:
    def __init__( self, inter_x, inter_y, inter_z ):
        # Position of the zero in the intervals
        self.x0 = -inter_x[0]
        self.y0 = -inter_y[0]
        self.z0 = -inter_z[0]
        # Lengths of the intervals
        self.len_x = inter_x[1] - inter_x[0] + 1
        self.len_y = inter_y[1] - inter_y[0] + 1
        self.len_z = inter_z[1] - inter_z[0] + 1

        # Cells of the cube
        # self.cells = [ [ [ 0 for _ in range(self.len_z) ] for _ in range(self.len_y) ] for _ in range(self.len_z) ]
        self.cells = np.zeros( ( self.len_x, self.len_y, self.len_z ), dtype=int )
        return

    # Count the cells that are on
    def count_cells_on( self ):

        return np.sum( self.cells )

    # Switch cells on or off as given by the step of instructions
    def switch_cells( self, step ):

        # Collision in x
        ix0 = self.x0 + step[1][0]
        ix1 = min( self.x0 + step[1][1] + 1, self.len_x )
        # print( "{} {}".format( ix0, ix1 ) )
        if ix0 < self.len_x and ix0 >= 0:
            # Collision in y
            iy0 = self.y0 + step[2][0]
            iy1 = min( self.y0 + step[2][1] + 1, self.len_y )
            # print( "{} {}".format( iy0, iy1 ) )
            if iy0 < self.len_y and iy0 >= 0:
                # Collision in z
                iz0 = self.z0 + step[3][0]
                iz1 = min( self.z0 + step[3][1] + 1, self.len_z )
                # print( "{} {}".format( iz0, iz1 ) )
                if iz0 < self.len_z and iz0 >= 0:
                    for ix in range( ix0, ix1 ):
                        for iy in range( iy0, iy1 ):
                            for iz in range( iz0, iz1 ):
                                self.cells[ ix, iy, iz ] = step[ 0 ]

# Read the steps
steps = []
with open( "input.txt", "r" ) as f:
    for line in f:
        # match = re.findall( r"([a-z]+)\sx=([0-9]+)..([0-9]+),y=([0-9]+)..([0-9]+),z=([0-9]+)..([0-9]+)$", line )
        match = re.findall( r"([a-z]+)\sx=(-*[0-9]+)..(-*[0-9]+),y=(-*[0-9]+)..(-*[0-9]+),z=(-*[0-9]+)..(-*[0-9]+)$", line )
        if len( match ) > 0:
            if len( match[0] ) > 0:
                # Read the first element to see if it is on or off
                result = 0
                if match[0][0] == "on":
                    result = 1
                steps.append( [ result, [ int(match[0][1]), int(match[0][2]) ],
                                        [ int(match[0][3]), int(match[0][4]) ],
                                        [ int(match[0][5]), int(match[0][6]) ] ] )

################################################################################
# First part
################################################################################

# Define the initialization region
init_region = CubeRegion( [-50, 50], [-50,50], [-50,50] )

# Turn cells on or off as given by the steps
for step in steps:
    init_region.switch_cells( step )

    # print("on: {}".format( init_region.count_cells_on() ))


print("\n\n--------------\nFirst part\n\n")
print("Cells in the initialization region that are on: {}".format( init_region.count_cells_on() ))



################################################################################
# Second part
################################################################################

class Cuboid:
    def __init__( self, value, inter_x, inter_y, inter_z ):
        # Positions of the two corners
        self.r0 = [ inter_x[0], inter_y[0], inter_z[0] ]
        self.r1 = [ inter_x[1], inter_y[1], inter_z[1] ]

        # Value
        self.value = value

    def __repr__(self):
        return f"Cuboid: {self.r0[0], self.r0[1], self.r0[2]}, {self.r1[0], self.r1[1], self.r1[2]};"

    # Get the total value of the cube
    def get_total_value( self ):
        # Number of cells in the cube
        n_cells = ( self.r1[0] - self.r0[0] ) * \
                  ( self.r1[1] - self.r0[1] ) * \
                  ( self.r1[2] - self.r0[2] )

        return self.value * n_cells

    # Check if two cuboids collide
    def check_collision( self, other ):

        return self.r0[0] <= other.r1[0] and self.r1[0] >= other.r0[0] and \
               self.r0[1] <= other.r1[1] and self.r1[1] >= other.r0[1] and \
               self.r0[2] <= other.r1[2] and self.r1[2] >= other.r0[2]

    # Check if the cuboid is valid
    def is_valid( self ):
        return ( self.r0[0] < self.r1[0] ) and ( self.r0[1] < self.r1[1] ) and ( self.r0[2] < self.r1[2] )

    # Get the overlap with another cuboid
    def get_overlap_cuboid( self, other ):
        # Overlap cuboid
        overlap_value = -other.value

        overlap_int_x = [ max( self.r0[0], other.r0[0] ), min( self.r1[0], other.r1[0] ) ]
        overlap_int_y = [ max( self.r0[1], other.r0[1] ), min( self.r1[1], other.r1[1] ) ]
        overlap_int_z = [ max( self.r0[2], other.r0[2] ), min( self.r1[2], other.r1[2] ) ]

        overlap = Cuboid( overlap_value, overlap_int_x, overlap_int_y, overlap_int_z )

        return overlap if overlap.is_valid() else None

# Initialize the list of cubes with the first one
cuboids = []
for step in steps[:1]:
    inter_x = [ step[1][0], step[1][1] + 1 ]
    inter_y = [ step[2][0], step[2][1] + 1 ]
    inter_z = [ step[3][0], step[3][1] + 1 ]
    cuboids.append( Cuboid( step[0], inter_x, inter_y, inter_z ) )

# Apply the different steps
for i in range( 1, len(steps) ):
    # Cuboid for the current step
    inter_x = [ steps[i][1][0], steps[i][1][1] + 1 ]
    inter_y = [ steps[i][2][0], steps[i][2][1] + 1 ]
    inter_z = [ steps[i][3][0], steps[i][3][1] + 1 ]
    current_cuboid = Cuboid( steps[i][0], inter_x, inter_y, inter_z )

    # Collide the current cuboid with all the previous ones
    new_cuboids = []

    # Collide the current cuboid with all the previous ones
    for other in cuboids:
        overlaps = []
        # Check if they collide
        if current_cuboid.check_collision( other ):
            # Overlap cuboid
            overlap = current_cuboid.get_overlap_cuboid( other )
            if overlap:
                new_cuboids.append( overlap )
                overlaps.append( overlap )

    # Add this cuboid to the list
    new_cuboids.append( current_cuboid )

    # Add the newly found cuboids to the global list
    for cuboid in new_cuboids:
        cuboids.append( cuboid )

# Compute the total amount of cells turned on
cells_on = 0
count = 0
for cuboid in cuboids:
    cells_on += cuboid.get_total_value()

print("\n\n--------------\nSecond part\n\n")
print("The total amount of cells that are on is: {}".format( cells_on ))


################################################################################
# Another version of the 2nd part, following a solution that I found online
################################################################################

# def run_instructions( instructions ):
#     placed = []
#     volume = 0
#
#     for instruction in reversed( instructions ):
#     # for instruction in instructions:
#         # if instruction[0] != 0:
#         if instruction[0] == 1:
#         # if True:
#             # instr_cuboid = Cuboid( instruction[0], instruction[1], instruction[2], instruction[3] )
#             overlap_instructions = []
#             for cuboid in placed:
#                 #
#                 #
#                 overlap = cuboid.get_overlap_cuboid( instruction[1] )
#                 # overlap = instruction[1].get_overlap_cuboid( cuboid )
#                 #
#                 #
#                 if overlap:
#                     overlap.value = 1
#                     overlap_instructions.append( [ 1, overlap ] )
#             volume += instruction[1].get_volume() - run_instructions( overlap_instructions )
#         placed.append( instruction[1] )
#         # print( instruction[1] )
#         # print( instruction[1].get_volume() )
#     assert volume >= 0, "negative volume"
#     return volume
#
# instructions = []
# for step in steps:
#     inter_x = [ step[1][0], step[1][1] + 1 ]
#     inter_y = [ step[2][0], step[2][1] + 1 ]
#     inter_z = [ step[3][0], step[3][1] + 1 ]
#     instructions.append( [ step[0], Cuboid( step[0], inter_x, inter_y, inter_z )] )
# # print( instructions )
# aux = run_instructions( instructions )
# print( "\n\n\naux {}".format( aux ) )
# print( aux - 2758514936282235 )

