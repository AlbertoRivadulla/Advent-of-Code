import re

################################################################################
# First part
################################################################################

# Read the instructions
instructions = []
with open( "input.txt", "r" ) as f:
    for line in f:
        # noop instruction
        if line.strip() == "noop":
            instructions.append( [ 1, 0 ] )
        else:
            split = line.strip().split(' ')
            instructions.append( [ 2, int( split[1] ) ] )

# Compute the sum of the signal strengths at cycles 20, 60, 100, 140, 180, 220
sum_signal_strengths = 0
cycle = 0
register = 1
instruction_index = 0
addx_cycle_counter = 0
while True:
    # Advance one cycle
    cycle += 1

    # Sum the strength at the desired cycle numbers
    if ( cycle - 20 ) % 40 == 0:
        sum_signal_strengths += cycle * register

    # If the instruction is addx, add one to the addx_cycle_counter
    if instructions[ instruction_index ][ 0 ] == 2:
        # Stay at this instruction for two cycles
        addx_cycle_counter += 1

        # When the two cycles have passed, move to the next instruction
        if addx_cycle_counter == 2:
            register += instructions[ instruction_index ][ 1 ]
            addx_cycle_counter = 0
            instruction_index += 1
    else:
        # Move to the next instruction, and do nothing to the register
        instruction_index += 1

    # If I got to the end of the instruction list, break
    if instruction_index == len( instructions ):
        break

print("\n\n--------------\nFirst part\n\n")
print("The sum of the signal strengths is: {}".format( sum_signal_strengths ))


################################################################################
# Second part
################################################################################

# Pixels of the screen
pixels = [ '.' ] * ( 40 * 6 )

# Draw the pixels to the screen
cycle = 0
register = 1
instruction_index = 0
addx_cycle_counter = 0
while True:
    # Horizontal position of the pixel
    pixel_hor = cycle % 40

    # Check the horizontal position of the sprite, and draw the pixel if they
    # match.
    # The sprite is 3 pixels wide.
    # The cycle counter is equal to the position of the pixel being drawn, and
    # the register is the center of the horizontal position of the sprite.
    if abs( pixel_hor - register ) <= 1:
        pixels[ cycle ] = '#'

    # Advance one cycle
    cycle += 1

    # If the instruction is addx, add one to the addx_cycle_counter
    if instructions[ instruction_index ][ 0 ] == 2:
        # Stay at this instruction for two cycles
        addx_cycle_counter += 1

        # When the two cycles have passed, move to the next instruction
        if addx_cycle_counter == 2:
            register += instructions[ instruction_index ][ 1 ]
            addx_cycle_counter = 0
            instruction_index += 1
    else:
        # Move to the next instruction, and do nothing to the register
        instruction_index += 1

    # If I got to the end of the instruction list, break
    if instruction_index == len( instructions ):
        break

# Create the output string to print the pixels
string = ""
for i in range( 6 ):
    for j in range( 40 ):
        string += pixels[ i*40 + j ]
    string += '\n'

print("\n\n--------------\nSecond part\n\n")
print( string )

