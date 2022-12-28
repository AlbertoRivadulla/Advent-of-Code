import re

# First part

# Read the original stacks and the movements from the input file
stacks = []
movements = []
with open( "input.txt", "r" ) as f:
    # Read until the number of stacks, saving the previous lines in a list to 
    # parse them later
    lines_boxes = []
    nr_stacks = 0
    for line in f:
        # If the line matches the list of stack numbers
        if line[:6] == " 1   2":
            # Get the number of stacks
            nr_stacks = int(line.strip()[-1])
            break
        else:
            # Save the line to the list of lines
            lines_boxes.append( line )

    # Initialize the stacks
    stacks = [ [] for _ in range(nr_stacks) ]

    # Read the distibution of the boxes
    for i in range( len(lines_boxes) ):
        # Parse the line starting backwards
        this_line = ""
        for j in range( nr_stacks ):
            match = re.findall( r"\[([A-Z])\]",
                                lines_boxes[len(lines_boxes) - i - 1][j*4 : j*4 + 4]
                               )
            # If it contains a box, add it to the corresponding stack
            if match:
                stacks[ j ].append( match[0] )

    # Read the movements
    for line in f:
        match = re.findall(r"move\s([0-9]+)\sfrom\s([0-9]+)\sto\s([0-9]+)$", line)
        if match:
            movement = [ int(match[0][0]), int(match[0][1]) - 1,
                         int(match[0][2]) - 1 ]
            movements.append( movement )

# Move the boxes
for move in movements:
    for _ in range(move[0]):
        stacks[ move[2] ].append( stacks[ move[1] ].pop() )

# Get the boxes on top
boxes_on_top = ""
for stack in stacks:
    boxes_on_top += stack[-1]

print("\n\n--------------\nFirst part\n\n")
print("The boxes on top are: {}".format( boxes_on_top ))



# Second part

# Read the original stacks and the movements from the input file
stacks = []
movements = []
with open( "input.txt", "r" ) as f:
    # Read until the number of stacks, saving the previous lines in a list to 
    # parse them later
    lines_boxes = []
    nr_stacks = 0
    for line in f:
        # If the line matches the list of stack numbers
        if line[:6] == " 1   2":
            # Get the number of stacks
            nr_stacks = int(line.strip()[-1])
            break
        else:
            # Save the line to the list of lines
            lines_boxes.append( line )

    # Initialize the stacks
    stacks = [ [] for _ in range(nr_stacks) ]

    # Read the distibution of the boxes
    for i in range( len(lines_boxes) ):
        # Parse the line starting backwards
        this_line = ""
        for j in range( nr_stacks ):
            match = re.findall( r"\[([A-Z])\]",
                                lines_boxes[len(lines_boxes) - i - 1][j*4 : j*4 + 4]
                               )
            # If it contains a box, add it to the corresponding stack
            if match:
                stacks[ j ].append( match[0] )

    # Read the movements
    for line in f:
        match = re.findall(r"move\s([0-9]+)\sfrom\s([0-9]+)\sto\s([0-9]+)$", line)
        if match:
            movement = [ int(match[0][0]), int(match[0][1]) - 1,
                         int(match[0][2]) - 1 ]
            movements.append( movement )

# Move the boxes
for move in movements:
    # Move the boxes to a buffer
    buffer = []
    for _ in range( move[0] ):
        buffer.append( stacks[ move[1] ].pop() )

    # Move the boxes from the buffer to the destination stack
    for _ in range( move[0] ):
        stacks[ move[2] ].append( buffer.pop() )

# Get the boxes on top
boxes_on_top = ""
for stack in stacks:
    boxes_on_top += stack[-1]

print("\n\n--------------\nSecond part\n\n")
print("The boxes on top are: {}".format( boxes_on_top ))

