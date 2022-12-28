import re
import math
from collections import deque

class Monkey:
    def __init__( self ):
        # List of objects
        self.objects = deque()

        # Operation
        # [ operator, number / old ]
        self.operation = [ ' ', ' ' ]

        # Test and outcomes if true and false
        # [ denominator, result true, result false ]
        self.test = [ 0, 0, 0 ]

        # Counter for the times this monkey has inspected an object
        self.inspect_count = 0

        # Product of the divisors of all tests
        self.prod_divisors_tests = 0

    # Overload the str method, for printing the class
    def __str__( self ):
        string = "Monkey\n"
        string += " - Objects: "
        for obj in self.objects:
            string += str( obj ) + ', '
        string += "\n - Operation: old " + self.operation[0] + " " + str(self.operation[1])
        string += "\n - Test: divisible by " + str( self.test[0] )
        string += "\n    - If true: pass to monkey " + str( self.test[1] )
        string += "\n    - If false: pass to monkey " + str( self.test[2] )
        string += "\n - Objects inspected: " + str( self.inspect_count )
        string += "\n"

        return string

    # Run one turn of the game
    def run_turn( self, monkeys, divide_by_three = True ):

        # Inspect all objects in the queue, starting from the beginning
        while len( self.objects ) > 0:
            # Increment the counter of objects inspected
            self.inspect_count += 1

            # Get the first object
            obj = self.objects.popleft()

            # Perform the operation on the object
            if self.operation[0] == '+':
                if self.operation[1] == 'old':
                    obj += obj
                else:
                    obj += self.operation[1]
            if self.operation[0] == '*':
                if self.operation[1] == 'old':
                    obj *= obj
                else:
                    obj *= self.operation[1]

            if divide_by_three:
                # Divide the worry level of the object by 3 and round down
                obj = math.floor( obj / 3 )
            else:
                # Take the modulus of the worry level with the product of the
                # divisors in each of the tests
                obj = obj % self.prod_divisors_tests

            # Perform the test
            if obj % self.test[0] == 0:
                # True outcome
                monkeys[ self.test[1] ].objects.append( obj )

            else:
                # False outcome
                monkeys[ self.test[2] ].objects.append( obj )

        return


# Read the data from the file
monkeys = []
with open( "input.txt", "r" ) as f:
    # Read the entire file
    lines = f.readlines()

    # Parse the lines one by one
    i = 0
    while i < len( lines ):
        # Check if this line starts a new monkey
        match = re.findall( r"Monkey [0-9]+", lines[i] )
        if len( match ) > 0:
            # Add a monkey
            monkeys.append( Monkey() )

            i += 1
            continue

        # Check if this line sets the starting items of the monkey
        match = re.findall( r"Starting\sitems:\s(.+)", lines[i] )
        if len( match ) > 0:
            # Get the items
            for obj in match[0].strip().split(', '):
                monkeys[-1].objects.append( int(obj) )

            i += 1
            continue

        # Check if this line defines the operation of the monkey
        match = re.findall( r"Operation:\snew\ =\ old\ (.)\s(.+)$", lines[i] )
        if len( match ) > 0:
            # Set the operator
            monkeys[-1].operation[0] = match[0][0]

            # Set the second operand
            if match[0][1][0].isdigit():
                monkeys[-1].operation[1] = int( match[0][1] )
            else:
                monkeys[-1].operation[1] = match[0][1]

            i += 1
            continue

        # Check if this line defines the test conditions of the monkey
        match = re.findall( r"Test:\sdivisible\sby\s([0-9]+)$", lines[i] )
        if len( match ) > 0:
            # Set the divider of the condition
            monkeys[-1].test[0] = int( match[0] )
            # Get the two outcomes of the condition
            i += 1
            match_true = re.findall( r"If\strue:\sthrow\sto\smonkey\s([0-9]+)$", lines[i] )
            monkeys[-1].test[1] = int( match_true[0] )
            i += 1
            match_false = re.findall( r"If\sfalse:\sthrow\sto\smonkey\s([0-9]+)$", lines[i] )
            monkeys[-1].test[2] = int( match_false[0] )

            i += 1
            continue

        # Otherwise, simply advance
        i += 1

# Compute the product of the divisors of all tests
prod_divisors = 1
for monkey in monkeys:
    prod_divisors *= monkey.test[0]
for monkey in monkeys:
    monkey.prod_divisors_tests = prod_divisors

for monkey in monkeys:
    print( monkey )


################################################################################
# First part
################################################################################

# # Run the game for a few rounds
# nr_rounds = 20
# for round_nr in range( 1, nr_rounds + 1 ):
#
#     # Run the turn of each monkey
#     for monkey in monkeys:
#         monkey.run_turn( monkeys, True )
#
# print( "\n---------------------\nAfter round {}:\n".format( nr_rounds ) )
# for monkey in monkeys:
#     print( monkey )
#
# # Multiply together the inspection count of the two most active monkeys
# first_most_active = 0
# second_most_active = 0
# for monkey in monkeys:
#     thiscount = monkey.inspect_count
#     if thiscount > first_most_active:
#         second_most_active = first_most_active
#         first_most_active = thiscount
#     elif thiscount > second_most_active:
#         second_most_active = thiscount
# prod_inspection_count = first_most_active * second_most_active
#
# print("\n\n--------------\nFirst part\n\n")
# print("Product of the inspection count of the two most active monkeys: {}".format( prod_inspection_count ))


################################################################################
# Second part
################################################################################

# Run the game for a few rounds
nr_rounds = 10000
# nr_rounds = 1000
for round_nr in range( 1, nr_rounds + 1 ):

    # Run the turn of each monkey
    for monkey in monkeys:
        monkey.run_turn( monkeys, False )

    if round_nr % 100 == 0:
        print( "\n---------------------\nAfter round {}:\n".format( round_nr ) )
        for i in range( len( monkeys ) ):
            print("Monkey {} inspected {} times".format( i, monkeys[i].inspect_count ))


# Multiply together the inspection count of the two most active monkeys
first_most_active = 0
second_most_active = 0
for monkey in monkeys:
    thiscount = monkey.inspect_count
    if thiscount > first_most_active:
        second_most_active = first_most_active
        first_most_active = thiscount
    elif thiscount > second_most_active:
        second_most_active = thiscount
prod_inspection_count = first_most_active * second_most_active

print("\n\n--------------\nSecond part\n\n")
print("Product of the inspection count of the two most active monkeys: {}".format( prod_inspection_count ))
