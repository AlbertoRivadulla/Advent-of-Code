import time
import re

# Convert a SNAFU number to base 10
def SNAFU_to_decimal( number ):
    decimal = 0
    for i in range( len( number ) ):
        power = 5 ** ( len( number ) - i - 1 )
        if number[i].isdigit() and int(number[i]) < 3:
            decimal += power * int( number[i] )
        else:
            if number[i] == '-':
                decimal += -1 * power
            elif number[i] == '=':
                decimal += -2 * power
            else:
                print("Invalid character")
    return decimal

# Convert a base-10 decimal number to SNAFU
def decimal_to_SNAFU( number ):
    SNAFU = ""

    # Compute the remainders after dividing by 5 repeatedly
    remainders = []
    nr_copy = number
    while nr_copy != 0:
        remainders.append( nr_copy % 5 )
        nr_copy = nr_copy // 5

    # Add one remainder more at the end, in case the next operation produces
    # largest numbers
    remainders.append( 0 )

    # If some of the remainders is 3 or larger, it should modify the next one
    # and it also should be modified itself
    for i in range( len( remainders ) - 1 ):
        if remainders[i] >= 3:
            remainders[i + 1] += 1
            remainders[i] -= 5

    # Construct the SNAFU number from the remainders
    for remainder in remainders:
        if remainder >= 0:
            SNAFU = str( remainder ) + SNAFU
        else:
            if remainder == -1:
                SNAFU = "-" + SNAFU
            elif remainder == -2:
                SNAFU = "=" + SNAFU
            else:
                print("There was some mistake")

    # Return the number. If it has a zero at the beginning, remove it
    return SNAFU[1:] if SNAFU[0] == '0' else SNAFU

# Read the SNAFU numbers
SNAFU_nrs = []
with open( "input.txt", "r" ) as f:
    for line in f:
        SNAFU_nrs.append( line.strip() )

################################################################################
# First part
################################################################################

start_time = time.time()

# Convert all the SNAFU numbers to decimal
decimal_nrs = [ SNAFU_to_decimal(nr) for nr in SNAFU_nrs ]

# Convert to SNAFU the sum of the decimal numbers
sum_SNAFU = decimal_to_SNAFU( sum( decimal_nrs ) )

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The number needed for the console is: {}".format( sum_SNAFU ))


