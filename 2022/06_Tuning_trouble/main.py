import re

################################################################################
# First part
################################################################################

# Function to check if the given characters are all different
def check_different_chars( string ):
    # List of characters already read
    read_chars = []
    for char in string:
        if char in read_chars:
            return False
        else:
            read_chars.append( char )
    # Otherwise return true
    return True

# Read the string
data = ""
with open( "input.txt", "r" ) as f:
    data = f.readline().strip()

# Find the position after the first set of four different characters
pos_four_diff = 4
while pos_four_diff <= len( data ):
    if check_different_chars( data[ pos_four_diff - 4 : pos_four_diff ] ):
        break
    pos_four_diff += 1

print("\n\n--------------\nFirst part\n\n")
print("The position after the first four different characters is: {}".format( pos_four_diff ))


################################################################################
# Second part
################################################################################

# Find the position after the first set of four different characters
pos_fourteen_diff = 14
while pos_fourteen_diff <= len( data ):
    if check_different_chars( data[ pos_fourteen_diff - 14 : pos_fourteen_diff ] ):
        break
    pos_fourteen_diff += 1

print("\n\n--------------\nSecond part\n\n")
print("The position after the first fourteen different characters is: {}".format( pos_fourteen_diff ))
