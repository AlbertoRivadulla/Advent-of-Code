import time

from functools import cache
from itertools import zip_longest

# Struct for the state
# Elements:
#   tower: tuple[int, ...] ( a tuple of integers of unknown size )
#   piece index: int
#   movement_index: int
State = ( tuple[int, ...], int, int )

# Rocks in binary form
ROCKS = [
         [0b0011110],
         [0b0001000, 0b0011100, 0b0001000],
         [0b0011100, 0b0000100, 0b0000100],  # bottom up!
         # [0b0000100, 0b0000100, 0b0011100],
         [0b0010000, 0b0010000, 0b0010000, 0b0010000],
         [0b0011000, 0b0011000],
        ]

TOWER_CUTOFF_LENGTH = 40

# Read the string of movements
movements = ''
with open( "input.txt", "r" ) as f:
    movements = f.readline().strip()

@cache
def drop_single_step( tower: tuple[int, ...], piece: tuple[int, ...],
                      movement: str ) -> tuple[ tuple[ int, ... ], bool ]:

    # Left movement
    if movement == ">":
        # Check if the piece hits the right wall and if it interesects with the
        # tower after the movement
        if not any( line & 0b0000001 for line in piece ) and \
                not any( (pl >> 1) & tl for ( pl, tl ) in zip( piece, tower ) ):
            # If it doesn't, move the piece to the right
            piece = tuple( (pl >> 1 for pl in piece) )
    # Else: right movement
    else:
        if not any( line & 0b1000000 for line in piece ) and \
                not any( (pl << 1) & tl for ( pl, tl ) in zip( piece, tower ) ):
            # Move the piece to the right
            piece = tuple( (pl << 1 for pl in piece) )

    # Move down
    # Check if the piece intersects the tower in the line below.
    # In zip_longest I add a line at the bottom of the tower (moving it up, and 
    # functioning also as the ground).
    if (
        any( tl & pl for (tl, pl) in zip_longest( [0b1111111] + list(tower),
                                                  piece,
                                                  fillvalue=0 ) )
        # or piece[0]
    ):
        # Return the position of the piece after the step, and a boolean indicating
        # that it cannot drop further
        return ( piece, False )
    else:
        # Return the position of the piece after dropping, and a boolean indicating
        # that it can still drop further
        return ( piece[1:], True )

@cache
def drop_piece( tower: tuple[ int, ... ], piece_index: int, movement_index: int
               ) -> tuple[ State, int ]:

    # Piede in the current state.
    # len(tower) empty lines below (the lines already occupied by the tower), then
    # three empty lines and finally the current rock on top.
    # Recall that rocks are defined with the bottom up
    piece = tuple( [0]*len(tower) + [0,0,0] + ROCKS[piece_index] )
    can_fall = True

    # Drop until the piece cannot drop further down
    while can_fall:
        piece, can_fall = drop_single_step( tower, piece, movements[movement_index] )
        # Next movement
        movement_index = ( movement_index + 1 ) % len( movements )

    # Overlay the piece and the previous tower.
    # Iterate over both and binary-or them
    # zip_longest returns pairs of values taking one from tower and one from piece.
    # If one of these lists runs out of elements, its elements are replaced by the fillvalue
    new_tower = tuple([lt | lp for lt, lp in zip_longest(tower, piece, fillvalue=0)])

    return (
        # State with the truncated tower and advanced piece index
        (
            new_tower[ -TOWER_CUTOFF_LENGTH : ],
            ( piece_index + 1 ) % len(ROCKS),
            movement_index
        ),
        # Incement in height
        len( new_tower ) - len( tower )
    )

@cache
def simulate_pieces( nr_pieces, state: State = ( (), 0, 0 )
                    ) -> tuple[ State, int ]:
    # Start at height 0
    height = 0
    # Drop the required pieces
    for _ in range(nr_pieces):
        # Unpack the argument *state
        state, delta_height = drop_piece(*state)
        height += delta_height

    return (state, height)



################################################################################
# First part
################################################################################

start_time = time.time()
_, height = simulate_pieces( 2022 )

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.10} s ---\n\n".format(time.time() - start_time))
print("Height of the tower: {}".format( height ))



################################################################################
# Second part
################################################################################

start_time = time.time()

# Total number of pieces to drop
nr_rocks_total = 1000000000000
# Number of rocks per step (it must divide exactly nr_rocks_total)
nr_rocks_step = 100000

# Initialize the state and the height
state: State = ( (), 0, 0 )
height = 0
# Run all the steps of the simulation
for step_nr in range( int( nr_rocks_total / nr_rocks_step ) ):
    # print( "{} / {}".format( step_nr, int( nr_rocks_total / nr_rocks_step ) ) )
    state, delta_height = simulate_pieces( nr_rocks_step, state )
    height += delta_height

    # # Part 2
    # timer.mark()
    # total = 1000000000000
    # stepsize = 100_000
    # # I tried and this seems to be the optimal power of 10. The number needs to
    # # neatly divide the total but I was too lazy to test around more. ~7s is
    # # good enogh for me.
    # state = ((), 0, 0)
    # height = 0
    # for _ in tqdm(range(int(total / stepsize))):
    #     state, delta_height = simulate_pieces(stepsize, state)
    #     height += delta_height
    # print(height)


print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.10} s ---\n\n".format(time.time() - start_time))
print("Height of the tower: {}".format( height ))






