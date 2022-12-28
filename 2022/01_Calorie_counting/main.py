################################################################################
# Part 1
################################################################################

# Calories carried by the elf with most of them
most_calories = 0

with open("input.txt", "r") as f:
    # Number of calories of the current elf
    current_calories = 0
    for line in f:
        # If this is a separator between inventaries of the elves
        if line == "\n":
            # Check if this has more calories than the one with the most before
            most_calories = max( most_calories, current_calories )
            # Restart the counter
            current_calories = 0
        else:
            # Add to the calorie counter
            current_calories += int( line.strip() )

print("The elf with most calories has {} calories\n".format( most_calories ) )


################################################################################
# Part 2
################################################################################

# List with the calories carried by the three that have the most
three_most_calories = [ 0, -1, -2 ]

with open( "input.txt", "r" ) as f:
    # Number of calories of the current elf
    current_calories = 0
    for line in f:
        # If this is a separator between inventaries of the elves
        if line == "\n":
            # Check if it has more calories than the last of the three
            if current_calories > three_most_calories[ 2 ]:
                three_most_calories[ 2 ] = current_calories
                if three_most_calories[ 2 ] > three_most_calories[ 1 ]:
                    temp = three_most_calories[ 1 ]
                    three_most_calories[ 1 ] = three_most_calories[ 2 ]
                    three_most_calories[ 2 ] = temp
                    if three_most_calories[ 1 ] > three_most_calories[ 0 ]:
                        temp = three_most_calories[ 0 ]
                        three_most_calories[ 0 ] = three_most_calories[ 1 ]
                        three_most_calories[ 1 ] = temp
            # Restar the counter
            current_calories = 0

        else:
            # Add to the calorie counter
            current_calories += int( line.strip() )
print(three_most_calories)

print("The amount of calories carried by the three that have the most is: {}\n".format( sum( three_most_calories ) ))
