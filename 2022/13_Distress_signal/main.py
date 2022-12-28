import re


class Node:
    def __init__( self, parent_node, is_leaf = False, value = None ):
        self.parent = parent_node

        # Value (only used if the node is a leaf)
        self.is_leaf = is_leaf
        self.value = value

        # If the value is not a leaf, it will contain a list of elements (also nodes)
        self.children = []

    # # Methods to add children nodes
    # def add_children( self, left, right ):
    #     self.left_child  = left
    #     self.right_child = right

    # Method to print the current node and its children
    def get_string( self ):

        # If the node is not a leaf, print its children surrounded by []
        if not self.is_leaf:
            string = "["
            for child in self.children:
                string += child.get_string() + ','

            return string + "]"

        else:
            if self.value is not None:
                return str( self.value )
            else:
                return ''


    # Method to compare two nodes
    def compare_nodes( self, other ):

        # If both nodes are integers
        if self.is_leaf and other.is_leaf:
            # print("Compare leaves {} {}".format( self.value, other.value ))
            # If the first integer is lower than the second one, the order is correct
            if self.value < other.value:
                return True

            # If they are in the opposite order, it is incorrect
            elif self.value > other.value:
                return False

            # If the values are the same, we don't know if the order is correct
            else:
                return None

        # If both nodes are lists
        elif not self.is_leaf and not other.is_leaf:
            # print("Compare lists")
            # print( self.get_string() )
            # print( other.get_string() )
            # Compare the pairs of values
            index = 0
            while True:

                # If I got to the end of the first list, the order is not correct
                if index >= len( self.children ):
                    if index < len( other.children ):
                        # print("left list ran out")
                        return True
                    else:
                        break

                # If I 
                if index >= len( other.children ):
                    if index < len( self.children ):
                        # print("right list ran out")
                        return False
                    else:
                        break

                # Compare the two elements
                comparison = self.children[index].compare_nodes( other.children[index] )

                # If the comparison returned a non-None value, return its result
                if comparison is not None:
                    return comparison

                # Move on the list
                index += 1

        # If one nodes is integer
        elif self.is_leaf and not other.is_leaf:
            # print("Compare leaf and list")
            # Convert self to a list containing its value as the only leaf
            self.is_leaf = False
            self.children.append( Node( self, True, self.value ) )
            self.value = None

            # Run the comparison again
            return self.compare_nodes( other )

        elif not self.is_leaf and other.is_leaf:
            # print("Compare list and leaf")
            # Convert other to a list containing its value as the only leaf
            other.is_leaf = False
            other.children.append( Node( other, True, other.value ) )
            other.value = None

            # Run the comparison again
            return self.compare_nodes( other )

        return


class Tree:
    def __init__( self, packet ):
        # List of nodes
        self.nodes = []

        # Add the first node, which has no parent
        self.nodes.append( Node( None, False, None ) )

        # Set the first node as the root
        self.root = self.nodes[ 0 ]

        # Current position in the tree
        self.current_node = self.root

        # Flag that is true for the divider packets
        self.is_divider = False

        # Read the packet
        self.read_packet( packet )

    def read_packet( self, string ):
        # Start at the root
        self.current_node = self.root

        # Read the entire string
        i = 0
        while i < len( string ):
            if string[i] == '[':
                # Create a new node and add it as a child of the current one
                # self.nodes.append( Node( self.current_node, False, None ) )
                # Create it as a leaf by default
                self.nodes.append( Node( self.current_node, True, None ) )
                self.current_node.is_leaf = False
                self.current_node.children.append( self.nodes[-1] )

                # Move to this child
                self.current_node = self.current_node.children[-1]

            elif string[i] == ']':
                # Go to the parent of the current node
                self.current_node = self.current_node.parent

                # If the child of the current node is a leaf with value None, remove it
                if self.current_node.children[-1].is_leaf and self.current_node.children[-1].value is None:
                    self.current_node.children.remove( self.current_node.children[-1] )

            elif string[i] == ',':
                # Move to the parent of the current node
                self.current_node = self.current_node.parent
                # Add a new node as a child of the the current one
                # self.nodes.append( Node( self.current_node, False, None ) )
                self.nodes.append( Node( self.current_node, True, None ) )
                self.current_node.is_leaf = False
                self.current_node.children.append( self.nodes[-1] )

                # Move to this child
                self.current_node = self.current_node.children[-1]

            elif string[i].isdigit():
                # Read the number until it ends
                this_nr = ""
                while string[i].isdigit():
                    this_nr += string[i]
                    i += 1
                i -= 1

                # Add the number as the value of the current node, and mark it as
                # a leaf
                self.current_node.value = int( this_nr )
                self.current_node.is_leaf = True

            # Advance in the string 
            i += 1

        return

    # Overload the str method, for printing the tree
    def __str__( self ):
        return self.root.get_string()

    # Method to compare two packets
    def compare_to_packet( self, other ):

        # Copare the two root nodes
        return self.root.compare_nodes( other.root )




################################################################################
# First part
################################################################################

# Read all the packets
packet_pairs = []
with open( "input.txt", "r" ) as f:
    this_pair = []
    for line in f:
        # If the line is empty, the two elements of the current pair have already
        # been read.
        # Add them to the list of pairs
        if line == '\n':
            packet_pairs.append( this_pair )
            this_pair = []
        # Otherwise, read the packet from the line
        else:
            this_pair.append( Tree( line.strip() ) )
    # Add the last pair to the list
    packet_pairs.append( this_pair )


# Compare the packets
sum_indices_valid = 0
for i in range( len( packet_pairs ) ):
    # print()
    # print( "Comparing pair {}".format( i+1 ))
    # print( packet_pairs[i][0] )
    # print( packet_pairs[i][1] )
    # Compare the current pair
    if packet_pairs[i][0].compare_to_packet( packet_pairs[i][1] ):
        # print("Valid pair {}".format( i + 1 ))
        sum_indices_valid += i + 1

print("\n\n--------------\nFirst part\n\n")
print("The sum of indices of the valid pairs is: {}".format( sum_indices_valid ))



################################################################################
# Second part
################################################################################


# Read all the packets again, in a single list
packets = []
with open( "input.txt", "r" ) as f:
    for line in f:
        # Skip blank lines
        if line != "\n":
            packets.append( Tree( line.strip() ) )

# Additional divider packets
divider_packets = [ Tree( "[[2]]" ), Tree( "[[6]]" ) ]
for divider in divider_packets:
    divider.is_divider = True
    packets.append( divider )

# Sort the packets using the insertion sort algorithm
i = 1
while i < len( packets ):
    temp = packets[ i ]
    j = i - 1
    while j >= 0 and not packets[j].compare_to_packet( temp ):
        packets[j+1] = packets[j]
        j -= 1
    packets[j+1] = temp
    i += 1

# Look for the positions of the divider packets
prod_position_dividers = 1
for i in range( len( packets ) ):
    if packets[i].is_divider:
        prod_position_dividers *= ( i + 1 )


print("\n\n--------------\nSecond part\n\n")

print("Sorted packets:")
for packet in packets:
    print( packet )

print("The product of the positions of the dividers is: {}".format( prod_position_dividers ))
