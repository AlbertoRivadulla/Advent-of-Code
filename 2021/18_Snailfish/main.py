import re
import math

class Node:
    def __init__( self, parent_node, is_leaf = False, depth = 0, value = None ):
        self.is_leaf = is_leaf
        self.parent = parent_node
        # Depth in the tree
        self.depth = depth
        # Value (only used if the node is a leaf)
        self.value = value
        # If the node is a pair of numbers, this should be 2
        self.pair_count = 0
        # Children
        self.left_child  = None
        self.right_child = None

    # Methods to add children nodes
    def add_children( self, left, right ):
        self.left_child  = left
        self.right_child = right

    # Method to print the current node and its children
    def get_string( self ):
        # Print the children, if the node is not a leaf
        if not self.is_leaf:
            return '[' + self.left_child.get_string() + ',' \
                   + self.right_child.get_string() + ']'
        else:
            # return str( self.value ) + "(" + str( self.depth ) + ")"
            return str( self.value )

    # Explode action
    def find_node_to_explode( self ):
        # If this node is a pair
        if self.pair_count == 2:
            # If it has depth of 4, return it
            if self.depth >= 4:
                return self

        # Check the two nodes below, if this node is not a pair
        if self.pair_count != 2 and not self.is_leaf:
            # Check first the node to the left
            check_left = self.left_child.find_node_to_explode()
            if check_left:
                return check_left
            # Then the node to the right
            check_right = self.right_child.find_node_to_explode()
            if check_right:
                return check_right

        return None

    # Find the next leaf to the left
    def find_left_leaf( self ):
        next_node = self
        # Go up until I can take left
        while True:
            if not next_node.parent:
                # If I reached the root node, there is no neighbor to the left
                return None

            if next_node.parent.left_child == next_node:
                # Continue going up
                next_node = next_node.parent
            else:
                # Go to the left
                next_node = next_node.parent.left_child
                break

        # Go down and right until I reach a leaf
        while True:
            if next_node.is_leaf:
                return next_node
            else:
                next_node = next_node.right_child

    # Find the next leaf to the right
    def find_right_leaf( self ):
        next_node = self
        # Go up until I can take right
        while True:
            if not next_node.parent:
                # If I reached the root node, there is no neighbor to the right
                return None

            if next_node.parent.right_child == next_node:
                # Continue going up
                next_node = next_node.parent
            else:
                # Go to the right
                next_node = next_node.parent.right_child
                break

        # Go down and left until I reach a leaf
        while True:
            if next_node.is_leaf:
                return next_node
            else:
                next_node = next_node.left_child

    # Find a node to split
    def find_node_to_split( self ):
        # If this node is a leaf and its value is larger than 9, return it
        if self.is_leaf and self.value > 9:
            return self

        # If it is not a leaf, check the two nodes below
        if not self.is_leaf:
            # Check first the node to the left
            check_left = self.left_child.find_node_to_split()
            if check_left:
                return check_left
            # Then the node to the right
            check_right = self.right_child.find_node_to_split()
            if check_right:
                return check_right

        return None


    # Split the node into its two children
    def split_to_children( self ):
        # Value of the left child (half rounded down)
        self.left_child.is_leaf = True
        self.left_child.value = math.floor( self.value / 2 )

        # Value of the right child (half rounded up)
        self.right_child.is_leaf = True
        self.right_child.value = math.ceil( self.value / 2 )

        # This node is now a pair
        self.pair_count = 2
        self.is_leaf = False
        self.value = None

        # The parent now has one less leaf child
        self.parent.pair_count -= 1

        return

    # Get the magnitude of the node
    def get_magnitude_nr( self ):
        # If the node is a leaf, return its value
        if self.is_leaf:
            return self.value
        # Otherwise, compute the magnitude from those of its children
        else:
            return 3 * self.left_child.get_magnitude_nr() + 2 * self.right_child.get_magnitude_nr()

class Tree:
    def __init__( self, snailfish_nr ):
        # List of nodes
        self.nodes = []

        # Add the first node, which has no parent
        self.nodes.append( Node( None, False, 0, None ) )

        # Set the first node as the root
        self.root = self.nodes[ 0 ]

        # Current position in the tree
        self.current_node = self.root

        # Read the snailfish number
        self.read_snailfish_number( snailfish_nr )

    # Method to read the snailfish number
    def read_snailfish_number( self, snailfish_nr ):
        depth = 0
        i = 0
        while i < len( snailfish_nr ):
            if snailfish_nr[i] == "[":
                # Increase the depth
                depth += 1
                # Add two nodes to the current one
                self.nodes.append( Node( self.current_node, False, depth ) )
                self.nodes.append( Node( self.current_node, False, depth ) )
                self.current_node.add_children( self.nodes[-2], self.nodes[-1] )
                # Go to the one in the left
                self.current_node = self.current_node.left_child

            elif snailfish_nr[i] == "]":
                # Decrease the depth
                depth -= 1
                # Go one node up
                self.current_node = self.current_node.parent

            elif snailfish_nr[i] == ",":
                # Go to the right node
                self.current_node = self.current_node.parent.right_child

            # If it is a number, add it as a value of the current node
            elif snailfish_nr[i].isdigit():
                # Read the number until it ends
                this_nr = ""
                while snailfish_nr[i].isdigit():
                    this_nr += snailfish_nr[i]
                    i += 1
                i -= 1

                # Add the number as the value of the current node, and mark it as
                # a leaf
                self.current_node.value = int( this_nr )
                self.current_node.is_leaf = True

                # Mark the node as pair
                self.current_node.parent.pair_count += 1

            # Advance in the loop
            i += 1

        return

    # Overload the str method, for printing the tree
    def __str__( self ):
        return self.root.get_string()

    # Explode action
    def explode( self ):
        # Look for the first node that has depth 4 and is not a leaf
        node_to_explode = self.root.find_node_to_explode()

        if node_to_explode:
            # Find the first leaf to the right, and add to it if it exists
            right_leaf = node_to_explode.find_right_leaf()
            # Find the first leaf to the left, and add to it if it exists
            left_leaf = node_to_explode.find_left_leaf()

            # Add to the left and right leaves, as corresponds
            if left_leaf:
                left_leaf.value += node_to_explode.left_child.value
            if right_leaf:
                right_leaf.value += node_to_explode.right_child.value

            # The exploded pair becomes a leaf with the value zero
            node_to_explode.is_leaf = True
            node_to_explode.value = 0
            node_to_explode.pair_count = 0

            # The parent now has one more child leaf
            node_to_explode.parent.pair_count += 1

            # Delete the children from the list of nodes
            self.nodes.remove( node_to_explode.left_child )
            self.nodes.remove( node_to_explode.right_child )
            node_to_explode.left_child = None
            node_to_explode.right_child = None

            return True

        # Return false if no node has been exploded
        return False

    # Split action
    def split( self ):
        # Look for a node to split
        node_to_split = self.root.find_node_to_split()

        if node_to_split:
            # Add two new nodes to the tree
            self.nodes.append( Node( node_to_split, False, node_to_split.depth + 1 ) )
            self.nodes.append( Node( node_to_split, False, node_to_split.depth + 1 ) )
            node_to_split.add_children( self.nodes[-2], self.nodes[-1] )

            # Use the previous nodes to split the desired one
            node_to_split.split_to_children()

            return True

        # Return false if there was not split node
        return False

    # Reduce: apply explode and split actions until they have no effect
    def reduce( self ):
        exploded = True
        split = True
        while exploded or split:
            # Try to explode and then split
            exploded = self.explode()
            if exploded:
                continue
            split    = self.split()

    # Add another number to this one
    def add_snailfish( self, other ):

        # Increase the depth of all the nodes
        for node in self.nodes:
            node.depth += 1
        for node in other.nodes:
            node.depth += 1

        # Create a new node as the root
        self.nodes.append( Node( None, False, 0, None ) )

        # Set this as the root of this and the other number
        other.root.parent = self.nodes[ -1 ]
        self.root.parent = self.nodes[ -1 ]
        self.nodes[ -1 ].add_children( self.root, other.root )
        self.root = self.nodes[ -1 ]

        for node in other.nodes:
            self.nodes.append( node )

        return

    # Compute the magnitude of the number
    def get_magnitude( self ):
        magnitude = self.root.get_magnitude_nr()

        return magnitude


################################################################################
# First part
################################################################################

# Read the numbers
snailfish_nrs = []
with open( "input.txt", "r" ) as f:
    for line in f:
        snailfish_nrs.append( line.strip() )

# Initialize the total sum with the first number
total_sum_tree = Tree( snailfish_nrs[ 0 ] )

# Sum the next numbers
for snailfish_nr in snailfish_nrs[ 1: ]:
    # Read the next number
    next_nr_tree = Tree( snailfish_nr )

    # Add this to the total sum
    total_sum_tree.add_snailfish( next_nr_tree )

    # Reduce the result
    total_sum_tree.reduce()


print("\n\n--------------\nFirst part\n\n")
print("\nThe result is: {}".format( total_sum_tree ))
print("\nThe magnitude of the result is: {}".format( total_sum_tree.get_magnitude() ))


################################################################################
# Second part
################################################################################

# Find the largest magnitude that I can get by adding two numbers
largest_magnitude = 0

for i in range( len( snailfish_nrs ) ):
    for j in range( len( snailfish_nrs ) ):
        # Check that the numbers are different
        if i == j:
            continue
        # Read the two numbers
        nr1 = Tree( snailfish_nrs[ i ] )
        nr2 = Tree( snailfish_nrs[ j ] )

        # Sum the numbers, reduce and get the magnitude of the sum
        nr1.add_snailfish( nr2 )
        nr1.reduce()
        largest_magnitude = max( largest_magnitude, nr1.get_magnitude() )


print("\n\n--------------\nSecond part\n\n")
print("The largest magnitude I can get is: {}".format( largest_magnitude ))
