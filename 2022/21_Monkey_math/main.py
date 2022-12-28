import time
import re

# Read the data of each monkey
monkeys = {}
monkeys_to_work = []
with open( "input.txt", "r" ) as f:
    for line in f:
        monkey = [ el.strip() for el in line.split(':') ]
        # Check if this monkey has a specific number
        if monkey[1].isnumeric():
            monkeys[ monkey[0] ] = int( monkey[1] )
        # Otherwise this monkey has an operation
        else:
            # Save it as a None value to the list of monkeys
            monkeys[ monkey[0] ] = None
            # Save the operation to the list of monkeys to work
            monkeys_to_work.append( [ monkey[0], monkey[1].split( ' ' ) ] )


################################################################################
# First part
################################################################################

# Function to compute the value of a monkey, if I have enough data.
# Otherwise, it returns None
def compute_value( monkey_to_work, monkeys ) -> tuple[bool, int]:

    # Check if both required values are valid
    left_val = monkeys[ monkey_to_work[1][0] ]
    right_val = monkeys[ monkey_to_work[1][2] ]
    if left_val != None and right_val != None:
        # Compute the value
        result = 0
        if monkey_to_work[1][1] == '+':
            result = left_val + right_val
        elif monkey_to_work[1][1] == '-':
            result = left_val - right_val
        elif monkey_to_work[1][1] == '*':
            result = left_val * right_val
        elif monkey_to_work[1][1] == '/':
            result = left_val / right_val
        # monkeys[ monkey_to_work[0] ] = int( result )

        return True, int( result )

    return False, 0

start_time = time.time()

# Compute the values of all the monkeys
while len( monkeys_to_work ) != 0:
    # Find the next monkey whose value I can compute
    i = 0
    while i < len( monkeys_to_work ):
        # Try to compute the value of the monkey
        success, value = compute_value( monkeys_to_work[i], monkeys )

        # If it was able to compute the result, save it and break the loop
        if success:
            monkeys[ monkeys_to_work[i][0] ] = value

            # Remove the monkey to work from the list
            monkeys_to_work.remove( monkeys_to_work[i] )

            break

        # Move to the next monkey
        i += 1


print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Value of the root monkey: {}".format( monkeys["root"] ))



################################################################################
# Second part
################################################################################

# Function to compute the value of a monkey with the given list of monkeys and operations
# def compute_value( monkey, monkeys, operations ) -> int:
def compute_value( monkey, monkeys, operations ):
    # If the monkey has a numerical value, return it
    if monkeys[ monkey ] != None:
        return monkeys[ monkey ]

    # Otherwise, call this recursively for each of the elements in the operand
    # left_val  = compute_value( operations[monkey][0], monkeys, operations )
    left_val  = int(operations[monkey][0]) if operations[monkey][0].isnumeric() else \
        compute_value( operations[monkey][0], monkeys, operations )
    right_val = int(operations[monkey][2]) if operations[monkey][2].isnumeric() else \
        compute_value( operations[monkey][2], monkeys, operations )

    # Apply the operation between the two
    if operations[monkey][1] == '+':
        return int( left_val + right_val )
    elif operations[monkey][1] == '-':
        return int( left_val - right_val )
    elif operations[monkey][1] == '*':
        return int( left_val * right_val )
    elif operations[monkey][1] == '/':
        return int( left_val / right_val )

    return 0

# Function to compute the value of a monkey for a given value of the monkey humn
# def compute_value_with_humn( monkey, humn_val, monkeys, operations ) -> int:
def compute_value_with_humn( monkey, humn_val, monkeys, operations ):
    # Set the value of the monkey humn
    monkeys[ "humn" ] = humn_val

    # Compute the value of the given monkey
    return compute_value( monkey, monkeys, operations )

# Count the appearnces of the monkey humn in the operations of a given monkey
def count_humn( monkey, monkeys, operations ):
    if monkey == 'humn':
        return 1

    if monkeys[monkey] != None:
        return 0

    left = operations[monkey][0]
    right = operations[monkey][2]

    return count_humn( left, monkeys, operations ) + count_humn( right, monkeys, operations )

# Find the inverse of an operation
def find_inverse_operation( monkey, operations ):
    # Find the operation that contains this monkey
    upper = ""
    for upper in operations.keys():
        if monkey in operations[upper]:
            break

    # Create the inverse operation
    inv_operation = []

    # Find the index of this monkey and the name of the other one
    monkey_ind = 0 if operations[upper][0] == monkey else 2
    other_monkey = operations[upper][0] if monkey_ind == 2 else operations[upper][2]

    # Compute the value of the other monkey, and add it to the inverse operation
    # as a string
    other_val_str = str( compute_value( other_monkey, monkeys, operations ) )

    # Invert the operation
    if operations[upper][1] == '+':
        inv_operation = [ upper, '-', other_val_str ]
    elif operations[upper][1] == '-':
        if monkey_ind == 0:
            inv_operation = [ other_val_str, '+', upper ]
        else:
            inv_operation = [ other_val_str, '-', upper ]
    elif operations[upper][1] == '*':
        inv_operation = [ upper, '/', other_val_str ]
    elif operations[upper][1] == '/':
        if monkey_ind == 0:
            inv_operation = [ other_val_str, '*', upper ]
        else:
            inv_operation = [ other_val_str, '/', upper ]

    return upper, inv_operation

# Find the value of the humn monkey, given a value of a monkey that the root compares
def find_humn_for_value( monkey, value, monkeys, operations ) -> int:
    # Set the value of the monkey humn to None
    monkeys[ "humn" ] = None

    # Invert the operations to compute the value of humn
    inv_operations = {}
    current = "humn"
    while current != monkey:
        # Compute the inverse operation and the next (upper) monkey
        upper, inv_operation = find_inverse_operation( current, operations )
        inv_operations[ current ] = inv_operation
        current = upper

    # In the inverse operations, replace the value of the desired monkey
    for upper in inv_operations.keys():
        if inv_operations[upper][0] == monkey:
            inv_operations[upper][0] = str( value )
        elif inv_operations[upper][2] == monkey:
            inv_operations[upper][2] = str( value )

    # Compute the value of humn with the invserse operations
    return compute_value( "humn", monkeys, inv_operations )


start_time = time.time()

# Read the data of each monkey again
monkeys = {}
operations = {}
with open( "input.txt", "r" ) as f:
    for line in f:
        monkey = [ el.strip() for el in line.split(':') ]
        # Check if this monkey has a specific number
        if monkey[1].isnumeric():
            monkeys[ monkey[0] ] = int( monkey[1] )
        # Otherwise this monkey has an operation
        else:
            # Save it as a None value to the list of monkeys
            monkeys[ monkey[0] ] = None
            # Save the operation to the dic of operations
            operations[ monkey[0] ] = monkey[1].split( ' ' )

# Get the two monkeys whose value have to be the same. These are the two that appear
# in the operation of the monkey "root"
need_to_be_equal = [ operations["root"][0], operations["root"][2] ]

# All numbers appear in only one operation, so only one of the numbers that need
# to be equal depend on humn. To check which, I count the appearances
humn_appearances = [ count_humn( monkey, monkeys, operations ) for monkey in \
                     need_to_be_equal ]
# Index of the monkey that depends on humn
index_depends = 0
while True:
    if humn_appearances[index_depends] == 1:
        break
    index_depends += 1

# Compute the desired value of the monkey
# The value of the argument humn_val is irrelevant
desired_value = compute_value_with_humn( need_to_be_equal[ ( index_depends + 1 ) % 2 ],
                                         0, monkeys, operations )

# Find the value of humn such that the other monkey reaches the desired value
humn_val = find_humn_for_value( need_to_be_equal[ index_depends ], desired_value,
                                monkeys, operations )


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("The correct value of humn is: {}".format( humn_val ))
