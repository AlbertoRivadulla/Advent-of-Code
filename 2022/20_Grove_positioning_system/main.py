import time
import re

class Node:
    def __init__( self, left_node, value ):
        self.value = value
        # Set the left and right nodes of this one
        #   neighbors[0] -> left node
        #   neighbors[1] -> right node
        self.neighbors = [ left_node, None ]
        # Set this as the right node of its left node
        if left_node:
            left_node.neighbors[1] = self

class LinkedList:
    def __init__( self ):
        # List of nodes
        self.nodes = []

        # List of nodes in the original order
        self.original_nodes = []

        # List of nodes
        self.nodes = []

        # Number of nodes
        self.nr_nodes = 0

    # Method to create the original list of nodes
    def initialize( self, original_nrs ):
        # Create the first node
        self.original_nodes.append( Node( None, original_nrs[0] ) )
        self.nodes.append( self.original_nodes[0] )
        # Don't add the first node
        # self.nr_nodes += 1

        # Add the rest of the numbers
        for i in range( 1, len( original_nrs ) ):
            new_node = Node( self.original_nodes[i-1], original_nrs[i] )
            self.original_nodes.append( new_node )
            self.nodes.append( new_node )
            self.nr_nodes += 1

        # Make the list circular
        self.original_nodes[0].neighbors[0] = self.original_nodes[-1]
        self.original_nodes[-1].neighbors[1] = self.original_nodes[0]

    # Print method
    def __str__( self ):
        string = "[ "
        current_node = self.nodes[0]
        for i in range( len( self.nodes ) ):
            string += str( current_node.value ) + ", "
            current_node = current_node.neighbors[1]
        string += "]"
        return string

    # Method to sort the nodes
    def sort_numbers( self ):
        # Iterate through the nodes in the original order
        for current in self.original_nodes:
            # If the value of the current node is zero, continue
            if current.value == 0:
                continue

            # Join the previous and next neighbors
            current.neighbors[0].neighbors[1] = current.neighbors[1]
            current.neighbors[1].neighbors[0] = current.neighbors[0]

            # Start moving at the current node
            next_node = current

            # Number of steps to move in the list, omitting cyclic moves
            nr_steps = current.value % self.nr_nodes
            # if neigh_index == 0:
            if current.value < 0:
                nr_steps = self.nr_nodes + nr_steps + 1

            # Move always to the right
            for _ in range( nr_steps ):
                # next_node = next_node.neighbors[ neigh_index ]
                next_node = next_node.neighbors[ 1 ]

            # Get the index of the neighbor from the sign of the value
            #   positive value -> move right
            #   negative value -> move left
            neigh_index = 1 if current.value > 0 else 0

            # Insert the current node at the desired position
            next_node.neighbors[ neigh_index ].neighbors[ ( neigh_index + 1) % 2 ] = current
            current.neighbors[ ( neigh_index + 1 ) % 2 ] = next_node
            current.neighbors[ neigh_index ] = next_node.neighbors[ neigh_index ]
            next_node.neighbors[ neigh_index ] = current

        return

    # Compute the groove coordinates
    # This is given by the sum of the 1000th, 2000th and 3000th number after the
    # zero
    def get_groove_coordinates( self ):
        coords = 0

        # Find the value zero
        current = self.original_nodes[0]
        for node in self.original_nodes:
            if node.value == 0:
                current = node
                break

        # Sum the 1000th, 2000th and 3000th values after this
        for _ in range( 3 ):
            # Move to the next number
            for _ in range( 1000 ):
                current = current.neighbors[1]
            # Add this value to the coordinates
            coords += current.value

        return coords

    # Multiply all values by a number
    def multiply_values( self, factor ):
        current = self.original_nodes[0]
        for _ in range( len( self.original_nodes ) ):
            current.value *= factor
            current = current.neighbors[1]


# Read the numbers from the file
original_nrs = []
with open( "input.txt", "r" ) as f:
    for line in f:
        original_nrs.append( int( line.strip() ) )

################################################################################
# First part
################################################################################

start_time = time.time()

# Initialize the list of numbers
linked_list = LinkedList()
linked_list.initialize( original_nrs )

# Sort the list
linked_list.sort_numbers()

# Compute the groove coordinates
groove_coords = linked_list.get_groove_coordinates()

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Groove coordinates: {}".format( groove_coords ))



################################################################################
# Second part
################################################################################


start_time = time.time()

# Initialize the list again
linked_list = LinkedList()
linked_list.initialize( original_nrs )

# Multiply all values by the decryption key
decryption_key = 811589153
linked_list.multiply_values( decryption_key )

# Sort the list ten times
for _ in range( 10 ):
    linked_list.sort_numbers()

# Compute the groove coordinates
groove_coords = linked_list.get_groove_coordinates()

print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Groove coordinates: {}".format( groove_coords ))
