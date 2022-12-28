
# Function to convert a string of pixels to a binary number
def pixels_to_binary( string ):
    number = 0
    for i in range( len( string ) ):
        if string[ -1 - i ] == "#":
            number += 2**i
    return number

# Function to print a matrix of pixels as an image
def print_as_image( pixels ):
    string = ""
    for row in pixels:
        for px in row:
            string += px
        string += '\n'
    print( string )

# Function to enhance an image with the given algorithm
def enhance_image( input_image, kernel_size, algorithm ):
    # Compute the offset from a side of the kernel to the center
    offset = ( kernel_size - 1 ) // 2
    # Initialize the new image
    new_image = [ [ ' ' for _ in range(len(input_image[0]) + 2*kernel_size) ] \
                  for _ in range(len(input_image) + 2*kernel_size) ]

    # Compute the disctinct pixels of the new image
    for i in range( len( input_image ) - 2 * offset ):
        for j in range( len( input_image[0] ) - 2 * offset ):
            # Read the string of pixels in the kernel
            str_kernel = ""
            for ik in range( kernel_size ):
                for jk in range( kernel_size ):
                    str_kernel += input_image[ i + ik ][ j + jk ]

            # Read the pixel value from the algorithm
            pixel_value = algorithm[ pixels_to_binary( str_kernel ) ]

            # Set the value of the pixels of the image
            new_image[i + kernel_size + offset][j + kernel_size + offset] = pixel_value

    # Compute the pixels in the border of the new image
    px_borders = new_image[ kernel_size + offset ][ kernel_size + offset ]
    for i in range( len( new_image ) ):
        for j in range( len( new_image[0] ) ):
            # Only write if the pixel has not been filled yet
            if new_image[ i ][ j ] == ' ':
                new_image[i][j] = px_borders

    return new_image

# Read the data
algorithm = ""
input_image = []

with open( "input.txt", "r" ) as f:
    # Read the algorithm
    while True:
        thisline = f.readline().strip()
        if len( thisline ) != 0:
            algorithm += thisline
        else:
            break
    # Read the image
    for line in f:
        input_image.append( line.strip() )


################################################################################
# First part
################################################################################

print("\nInput image:")
for row in input_image:
    print(row)

# Size of the kernel
kernel_size = 3

# Extend the input image 3 pixels in each direction
first_image = [ [ '.' for _ in range(len(input_image[0]) + 2*kernel_size) ] \
                for _ in range(len(input_image) + 2*kernel_size) ]

# Set the pixels of this first image
for i in range( len( input_image ) ):
    for j in range( len( input_image[0] ) ):
        first_image[ i + kernel_size ][ j + kernel_size ] = input_image[ i ][ j ]
# print("\nFirst image:")
# print_as_image( first_image )

# Compute the second image
second_image = enhance_image( first_image, kernel_size, algorithm )
# print("\nSecond image:")
# print_as_image( second_image )

# Compute the third image
third_image = enhance_image( second_image, kernel_size, algorithm )
# print("\nThird image:")
# print_as_image( third_image )

# Count the pixels that are lit
count_pixels_lit = 0
for row in third_image:
    for px in row:
        if px == '#':
            count_pixels_lit += 1

print("\n\n--------------\nFirst part\n\n")
print("The amount of pixels lit in the last image is: {}".format( count_pixels_lit ))

################################################################################
# Second part
################################################################################

# Enhance the image many times
times_to_enhance = 50
old_image = first_image
new_image = []
for iteration in range( times_to_enhance ):
    new_image = enhance_image( old_image, kernel_size, algorithm )
    old_image = new_image

    print( "Enhanced {} times".format( iteration ) )

# Count the pixels that are lit
count_pixels_lit = 0
for row in new_image:
    for px in row:
        if px == '#':
            count_pixels_lit += 1

print("\n\n--------------\nSecond part\n\n")
print("The amount of pixels lit after enhancing {} times is: {}".format( times_to_enhance, count_pixels_lit ))
