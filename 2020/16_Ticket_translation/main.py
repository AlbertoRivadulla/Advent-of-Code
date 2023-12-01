import time
import re

# Read the field names and ranges, my ticket and the nearby tickets
field_ranges = {}
my_ticket = []
nearby_tickets = []
with open( "input.txt", "r" ) as f:
    # Read the field names and ranges
    for line in f:
        if line == '\n':
            break
        else:
            line = line.split(':')
            field_name = line[0].strip()
            field_ranges_str = [ el.strip() for el in line[1].split(" or ") ]
            this_field_ranges = [  ]
            for range_str in field_ranges_str:
                this_field_ranges.append( [ int(nr) for nr in range_str.split('-') ] )
            field_ranges[ field_name ] = this_field_ranges

    # Read my ticket
    f.readline()
    my_ticket = [ int(nr) for nr in f.readline().strip().split(',') ]
    f.readline()

    # Read the other tickets
    f.readline()
    for line in f:
        nearby_tickets.append( [ int(nr) for nr in line.strip().split(',') ] )

################################################################################
# First part
################################################################################

# Check if a value is found in a pair of ranges
def value_in_ranges( value, ranges ):
    for rng in ranges:
        if value >= rng[0] and value <= rng[1]:
            return True
    return False

# Function to find the valid tickets
# It returns also the "ticket scanning error rate"
def find_valid_tickets( tickets, field_ranges ):
    error_rate = 0
    valid_tickets = []

    # Check each ticket
    for ticket in tickets:
        # Number of valid fields in the ticket
        valid_fields = 0
        # Check each value of the ticket
        for value in ticket:
            valid = False
            # Compare it with the ranges of the different fields
            for field_name in field_ranges:
                if value_in_ranges( value, field_ranges[ field_name ] ):
                    valid = True
                    break

            # If the ticket is not valid, add this value to the error_rate
            if not valid:
                error_rate += value
            else:
                valid_fields += 1

        # If the ticket is valid, store it in the list
        # if valid:
        if valid_fields == len( ticket ):
            valid_tickets.append( ticket )

    return valid_tickets, error_rate


start_time = time.time()

# Find the invalid tickets
valid_tickets, error_rate = find_valid_tickets( nearby_tickets, field_ranges )


print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Field scanning error rate: {}".format( error_rate ))



################################################################################
# Second part
################################################################################


start_time = time.time()

# Rows with assigned names
rows_found = [ 0 for _ in range( len( my_ticket ) ) ]
# Row number corresponding to each name
field_of_row = { name : 0 for name in field_ranges.keys() }

# Names of the field
field_names       = list( field_ranges.keys() )
field_ranges_list = list( field_ranges.values() )

# Matrix with the names that are valid for each row
valid_names = [ [ 0 for _ in range(len(field_names)) ] for _ in range(len(my_ticket)) ]

# Find the row names that are valid for each column
# Iterate over the rows
for i in range( len( valid_tickets[0] ) ):
    # Compare the values in this row with each field range
    for j in range( len( field_ranges_list ) ):
        valid_field = True
        # Iterate over the tickets
        for ticket in valid_tickets:
            if not value_in_ranges( ticket[i], field_ranges_list[j] ):
                valid_field = False
                break
        if valid_field:
            valid_names[i][j] = 1

# Assign names to the rows until they all have a name assigned
while sum( rows_found ) < len( rows_found ):
    # Find the next row that has only one valid name
    for i in range( len( my_ticket ) ):
        # If the row already has an assigned value, continue
        if rows_found[i]:
            continue
        # Check if it has only one valid name
        if sum( valid_names[i] ) == 1:
            # Find the index of the value
            j = 0
            while valid_names[i][j] == 0:
                j += 1

            # Assign to it this value
            field_of_row[ field_names[j] ] = i

            # Mark it as found
            rows_found[ i ] = 1

            # Remove this value from the rest of the rows that might have it
            for k in range( len( valid_names ) ):
                valid_names[k][j] = 0

# Multiply together the values of the field in my ticket that start by "departure"
product_departures = 1
for name in field_names:
    if name[:9] == "departure":
        product_departures *= my_ticket[ field_of_row[ name ] ]


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Product of the fields that start with departure: {}".format( product_departures ))
