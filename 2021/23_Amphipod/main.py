import re

class AmphipodHouse:
    def __init__( self, filename ):

        # Names of the amphipods
        self.amphipod_names = ['A', 'B', 'C', 'D']

        # Length of the corridor
        self.corridor_len = 0
        # Corridor
        self.corridor = []

        # Positions of the rooms in the corridor
        self.rooms_positions = [ 2, 4, 6, 8 ]
        # Positions of the amphipods in the rooms
        self.amphipods_in_rooms = [ [] for _ in range( 4 ) ]

        # Energy for moving each amphiphod
        self.amphipod_energy_cost = { 'A': 1,
                                      'B': 10,
                                      'C': 100,
                                      'D': 1000
                                     }
        # Destination rooms of the amphipods
        self.amphipod_destination = { 'A': 0,
                                      'B': 1,
                                      'C': 2,
                                      'D': 3
                                     }

        # Read the initial configuration
        self.read_initial_conf( filename )

        # Minimum energy
        self.minimum_energy = 1000000000000

        # State of the system
        # The last number is the energy of the current state
        self.state = [ self.corridor, self.amphipods_in_rooms, 0 ]

    # Print the configurations
    def __str__( self ):
        return str( self.state )

    # Check if the state is sorted
    def check_sorted( self, state ):
        for i in range( len( self.amphipod_names ) ):
            for j in range( len( state[1][i] ) ):
                if state[1][i][j] != self.amphipod_names[i]:
                    return False
        return True

    # Read the initial configuration from a file
    def read_initial_conf( self, filename ):
        with open( filename, "r" ) as f:
            for line in f:
                # Corridor
                match = re.findall( r"\#([\.]+)\#", line )
                if len( match ) > 0:
                    self.corridor_len = len( match[0].strip() )
                    self.corridor = [ ' ' for _ in range( self.corridor_len )]
                    continue

                # Rooms
                match = re.findall( r"\#+([ABCD])\#([ABCD])\#([ABCD])\#([ABCD])\#+", line )
                if len( match ) > 0:
                    for i in range(len(match[0])):
                        self.amphipods_in_rooms[i].append( match[0][i] )
                    continue

    # Get the lisf of available movements for the current state
    def get_available_movements( self, state ):
        available_movements = []

        # Each movement only moves one amphipod
        # It is a list of 2 lists with 2/3 elements
        #   first list: current position
        #   second list: next position
        # If one of the positions is at the corridor:
        #   list = [ 0, pos_in_corridor ]
        # If one of the positions is at one room:
        #   list = [ 1, room_nr, pos_at_room ]


        return available_movements

    # Evolve the system until all the amphipods are sorted
    def evolve( self ):

        # Queue of movements

        # Add the possible movements to the queue

        while True:
        # while len( next_movements ) > 0:

            # Pop a movement from the queue and apply it

                # If I reached the end configuration and the energy after this is
                # less than the minimum, update the minimum energy

                # If the energy after a movement is larger than the minimum one,
                # stop applying it

                # Else, get the list of possible movements after this one and add 
                # them to the queue

            # If the 

            break

        return



'''
    Amphipods will never stop on the space immediately outside any room. 
    They can move into that space so long as they immediately continue moving. 
    (Specifically, this refers to the four open spaces in the hallway that are directly above an amphipod starting position.)

    Amphipods will never move from the hallway into a room unless that room is their destination room 
    and that room contains no amphipods which do not also have that room as their own destination. 
    If an amphipod's starting room is not its destination room, it can stay in that room until it leaves the room. 
    (For example, an Amber amphipod will not move from the hallway into the right three rooms, 
    and will only move into the leftmost room if that room is empty or if it only contains other Amber amphipods.)

    Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. 
    (That is, once any amphipod starts moving, any other amphipods currently in the hallway are locked in place 
    and will not move again until they can move fully into a room.)
'''



################################################################################
# First part
################################################################################


# Procedure:

    # In each step, get a list of possible movements
        # If there are no available movements, stop

    # Recursively apply each movement, continuing the process

    # Always keep track of the minimum energy
    # For this, the entire process can be written in a class (instead of a global variable for the energy)

    # If after some movement the energy becomes more than the minimum, discard it


# Setup the system
amphipod_house = AmphipodHouse( "input.txt" )

# Evolve the system
amphipod_house.evolve()

print( amphipod_house )

print( amphipod_house.check_sorted( amphipod_house.state ))


print("\n\n--------------\nFirst part\n\n")
print("The minimum energy to sort them is: {}".format( amphipod_house.minimum_energy ))



################################################################################
# Second part
################################################################################


print("\n\n--------------\nSecond part\n\n")
