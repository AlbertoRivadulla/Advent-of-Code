import re

class Node:
    def __init__( self, name, parent_node, is_leaf = False, size = 0 ):
        self.size = size
        self.name = name
        self.is_leaf = is_leaf
        self.parent = parent_node

        # List of children nodes
        self.children = []

    # Method to add a children node
    def add_child( self, child ):
        self.children.append( child )

    # Method to update the size of all the parent nodes
    def update_size_parent( self, size ):
        # If it has a parent (otherwise it is the root node)
        if self.parent:
            self.parent.size += size
            self.parent.update_size_parent( size )

    # Method to print the current node and its children
    def get_string( self, indent = 0 ):
        # Print the current node
        string = "{} - {}, size = {}\n".format( ' '*indent, self.name, self.size )
        # Print the children, if the node is not a leaf
        if not self.is_leaf:
            for child in self.children:
                string += child.get_string( indent + 2 )
        return string

    # Method for the first part of the problem
    def sum_directories_smaller_than( self, max_size ):
        sum_sizes = 0

        # Sum the size of the current node
        if self.size < max_size:
            sum_sizes += self.size

        # Sum the sizes of the children nodes, if they are directories
        for child in self.children:
            if not child.is_leaf:
                sum_sizes += child.sum_directories_smaller_than( max_size )

        return sum_sizes

    # Method for the second part of the problem
    def size_smallest_directory_to_delete( self, smallest, required):

        # Check if the current directory is valid
        if ( self.size > required ) and ( self.size < smallest ):
            smallest = self.size

        # Check the children nodes recursively
        for child in self.children:
            if not child.is_leaf:
                smallest = child.size_smallest_directory_to_delete( smallest, required )

        # Look through the tree starting at the top
        return smallest

class Tree:
    def __init__( self ):
        # List of nodes
        self.nodes = []

        # Add the root node
        # This is a node with no parent
        self.nodes.append( Node( "/", None ) )

        # Current position in the tree
        self.current_node = self.nodes[ 0 ]

    # Method to add a child node
    def add_child( self, name, is_leaf, size = 0 ):
        # Add the node to the list, setting the current node as its parent
        self.nodes.append( Node( name, self.current_node, is_leaf, size ) )
        # Add this as a child of the current node
        self.current_node.add_child( self.nodes[-1] )

        # If the size is non-zero, update the size of the parents
        if size != 0:
            self.nodes[ -1 ].update_size_parent( size )

    # Method to move up
    def move_up( self ):
        if self.current_node.parent:
            self.current_node = self.current_node.parent
        else:
            print( "The directory {} has no parent".format( self.current_node.name ) )

    # Method to move to a given child node
    def move_to_child( self, name ):
        for child in self.current_node.children:
            if child.name == name:
                self.current_node = child
                return
        print( "The node {} has no children called {}".format( self.current_node.name, name ) )

    # Method to move to a given directory
    def move( self, name ):
        if name == "/":
            self.current_node = self.nodes[ 0 ]
        elif name == "..":
            self.move_up()
        else:
            self.move_to_child( name )

    # Overload the str method, for printing
    def __str__( self ):
        return self.nodes[0].get_string( 0 )

    # Method for the first part of the problem
    def sum_directories_smaller_than( self, max_size ):
        # Sum the sizes of the directories that are smaller than max_size, 
        # starting at the root
        return self.nodes[ 0 ].sum_directories_smaller_than( max_size )

    # Method for the second part of the problem
    def size_smallest_directory_to_delete( self, total_capacity, total_required ):
        smallest = self.nodes[0].size

        # Compute the space that I need to free
        space_to_free = total_required - ( total_capacity - self.nodes[0].size )
        # Look through the tree starting at the top
        return self.nodes[ 0 ].size_smallest_directory_to_delete( smallest, space_to_free )

# Initialize the tree
tree = Tree()

# Read the directory tree from the file
with open( "input.txt", "r" ) as f:
    adding_children = False
    for line in f:
        # Check if the line is a command
        if line[0] == '$':
            # Not adding children anymore
            adding_children = False
            # Change directory 
            match = re.findall( r"\$\scd\s([a-z0-9\/\.]+)$", line )
            if match:
                # Move to the directory 
                tree.move( match[0] )

            # List directory
            if line[ 2:4 ] == "ls":
                # Set the flag to read the next lines as children
                adding_children = True

        # Parse the line as a node (directory or file), and add it to the tree
        if adding_children:
            # Check if it is a directory
            if line[:3] == "dir":
                tree.add_child( line[4:].strip(), False )
            # Otherwise it should be a file
            else:
                match = re.findall( r"([0-9]+)\s([a-zA-Z0-9\.]+)$", line )
                if match:
                    tree.add_child( match[0][1], True, int(match[0][0]) )


print( tree )



################################################################################
# First part
################################################################################

print("\n\n--------------\nFirst part\n\n")
print( "The sum of the sizes of directories with a size smaller than 100000 is: {}".format( tree.sum_directories_smaller_than( 100000 ) ))


################################################################################
# Second part
################################################################################

# Space required for the update
space_required = 30000000
# Total capacity of the filesystem
total_capacity = 70000000

print("\n\n--------------\nSecond part\n\n")
print( "The size of the smallest directory to delete is: {}".format( tree.size_smallest_directory_to_delete( total_capacity, space_required ) ) )
