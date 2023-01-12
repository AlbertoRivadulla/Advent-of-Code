import time
import re

'''
    A good explanation on the problem and the solution can be found at
        https://www.ericburden.work/blog/2022/01/05/advent-of-code-2021-day-24/
    Notice that the input studied there is different than mine!
'''

# Read the instructions in chunks
instr_chunks = []
with open( "input.txt", "r" ) as f:
    this_chunk = []
    for line in f:
        # Split the line
        instruction = line.strip().split( ' ' )

        # If it is an 'inp' instruction, save the previous chunk and start a 
        # new one
        if len( instruction ) == 2:
            if len( this_chunk ) != 0:
                instr_chunks.append( this_chunk )
                this_chunk = []

        # Add the instruction to the current chunk
        this_chunk.append( instruction )

    # Save the last chunk
    instr_chunks.append( this_chunk )


################################################################################
# First part
################################################################################

# Auxiliary function to check if a string corresponds to an integer (with sign)
def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

# Function to find the largest pair of numbers ( left, right ) such that
#       left + offset == right
def find_largest_pair_with_offset( offset ):
    for left in range( 9, 0, -1 ):
        for right in range( 9, 0, -1 ):
            if left + offset == right:
                return left, right

# Function to apply apply a chunk of instructions with a given initial state of
# the registers and a value of w
def apply_instr_chunk( instrs, input_registers, w ):

    # Copy the values of the registers
    registers = input_registers.copy()

    # Apply the first instruction to set the value of w
    registers[ 'w' ] = w

    # Apply the rest of the instructions
    for j in range( 1, len( instrs ) ):
        # Get the left and right values
        left_val = registers[ instrs[j][1] ]
        right_val = int(instrs[j][2]) if check_int( instrs[j][2] ) else \
            registers[ instrs[j][2] ]

        # Apply the operation
        result = 0
        if instrs[j][0] == "add":
            result = left_val + right_val
        elif instrs[j][0] == "mul":
            result = left_val * right_val
        elif instrs[j][0] == "div":
            result = left_val // right_val
        elif instrs[j][0] == "mod":
            result = left_val % right_val
        elif instrs[j][0] == "eql":
            result = 1 if left_val == right_val else 0

        # Save the result in the corresponding register
        registers[ instrs[j][1] ] = result

    return registers


start_time = time.time()

# Find the largest MONAD number
# I follow the method explained at
#   https://www.ericburden.work/blog/2022/01/05/advent-of-code-2021-day-24/
largest_MONAD = [ 0 for _ in range( 14 ) ]
# Stack for the left instructions
left_instr_stack = []
for i in range( len( instr_chunks ) ):
    # If the 5th instruction tells to divide z by 1, add the current chunk to 
    # the stack.
    if instr_chunks[i][4][2] == '1':
        left_instr_stack.append( ( i, instr_chunks[i] ) )
    # Otherwise, pop the last element from the stack and cancel its contribution
    # to z with the current one
    else:
        left_i, left_instr_chunk = left_instr_stack.pop()
        # Get the increment in y from the 16th instruction of the left chunk.
        # This is the 'offset' in the reference blog post.
        left_incr = int( left_instr_chunk[15][2] )
        # Get the increment in x from the 6th instruction of the right chunk.
        # This is the 'correction' in the reference blog post.
        right_incr = int( instr_chunks[i][5][2] )
        # Find the largest numbers such that 
        #   left + ( left_incr + right_incr ) == right
        left, right = find_largest_pair_with_offset( left_incr + right_incr )

        # Place these in the corresponding position of the MONAD
        largest_MONAD[ left_i ] = left
        largest_MONAD[ i ]      = right

# Check that the number found is actually a monad
# Initialize all registers to zero
registers = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }
# Apply the instructions in chunks
for i in range( len( instr_chunks ) ):
    registers = apply_instr_chunk( instr_chunks[i], registers, largest_MONAD[i] )
# If the number is valid, the register z should have the value 0 at the end
assert registers['z'] == 0, "The number is not a valid MONAD."

# Convert the largest MONAD to a string
str_largest_MONAD = ''
for nr in largest_MONAD:
    str_largest_MONAD += str( nr )

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The largest MONAD number is: {}".format( str_largest_MONAD ))



################################################################################
# Second part
################################################################################

# Function to find the smallest pair of numbers ( left, right ) such that
#       left + offset == right
def find_smallest_pair_with_offset( offset ):
    for left in range( 1, 10 ):
        for right in range( 1, 10 ):
            if left + offset == right:
                return left, right

start_time = time.time()

# Find the smallest MONAD number
# I follow the method explained at
#   https://www.ericburden.work/blog/2022/01/05/advent-of-code-2021-day-24/
smallest_MONAD = [ 0 for _ in range( 14 ) ]
# Stack for the left instructions
left_instr_stack = []
for i in range( len( instr_chunks ) ):
    # If the 5th instruction tells to divide z by 1, add the current chunk to 
    # the stack.
    if instr_chunks[i][4][2] == '1':
        left_instr_stack.append( ( i, instr_chunks[i] ) )
    # Otherwise, pop the last element from the stack and cancel its contribution
    # to z with the current one
    else:
        left_i, left_instr_chunk = left_instr_stack.pop()
        # Get the increment in y from the 16th instruction of the left chunk.
        # This is the 'offset' in the reference blog post.
        left_incr = int( left_instr_chunk[15][2] )
        # Get the increment in x from the 6th instruction of the right chunk.
        # This is the 'correction' in the reference blog post.
        right_incr = int( instr_chunks[i][5][2] )
        # Find the smallest numbers such that 
        #   left + ( left_incr + right_incr ) == right
        left, right = find_smallest_pair_with_offset( left_incr + right_incr )

        # Place these in the corresponding position of the MONAD
        smallest_MONAD[ left_i ] = left
        smallest_MONAD[ i ]      = right

# Check that the number found is actually a monad
# Initialize all registers to zero
registers = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }
# Apply the instructions in chunks
for i in range( len( instr_chunks ) ):
    registers = apply_instr_chunk( instr_chunks[i], registers, smallest_MONAD[i] )
# If the number is valid, the register z should have the value 0 at the end
assert registers['z'] == 0, "The number is not a valid MONAD."

# Convert the smallest MONAD to a string
str_smallest_MONAD = ''
for nr in smallest_MONAD:
    str_smallest_MONAD += str( nr )


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The smallest MONAD number is: {}".format( str_smallest_MONAD ))



