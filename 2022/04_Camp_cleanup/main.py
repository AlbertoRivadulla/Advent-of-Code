import re

# First part

# Check if one interval is fully contained in the other
def is_fully_contained( int_inner, int_outer ):
    return ( int_outer[0] <= int_inner[0] ) and ( int_outer[1] >= int_inner[1] )

# Read the pairs of intervals
interval_pairs = []
with open( "input.txt", "r" ) as f:
    for line in f:
        match = re.findall( r"([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)$", line )
        if match:
            interval1 = [ int(match[0][0]), int(match[0][1]) ]
            interval2 = [ int(match[0][2]), int(match[0][3]) ]
            interval_pairs.append( [ interval1, interval2 ] )

# Number of redundant pairs
nr_redundant = 0
for pair in interval_pairs:
    if is_fully_contained( pair[0], pair[1] ) or is_fully_contained( pair[1], pair[0] ):
        nr_redundant += 1

print("\n\n--------------\nFirst part\n\n")
print("The number of pairs in which one fully contains the other is: {}".format( nr_redundant ))


# Second part

# Check if two intervals overlap
def check_overlap( int1, int2 ):
    return ( int1[1] - int2[0] ) * ( int1[0] - int2[1] ) <= 0

nr_overlap = 0
for pair in interval_pairs:
    if check_overlap( pair[0], pair[1] ):
        nr_overlap += 1

print("\n\n--------------\nSecond part\n\n")
print("The number of pairs that have some overlap is: {}".format( nr_overlap ))
