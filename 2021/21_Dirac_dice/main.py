import re

# Read the starting positions
original_positions = []
with open( "input.txt", "r" ) as f:
    for line in f:
        position = int(line.strip()[-1])
        original_positions.append( position )

################################################################################
# First part
################################################################################

# # Initialize the scores and positions
# positions = original_positions
# scores = [ 0, 0 ]
#
# # Run the game until one player reaches 1000 points
# nr_rolls = 0
# dice_val = 0
# current_player = 0
# while True:
#     # Roll three times for the current player
#     displacement = 0
#     for i in range( 3 ):
#         # The value of the dice increases in one each time and restarts once it 
#         # reaches 100
#         dice_val = ( dice_val ) % 100 + 1
#
#         # Move to the corresponding position
#         displacement += dice_val
#
#         # Count the rolls
#         nr_rolls += 1
#
#     # After three rolls, move the player
#     # print( positions[current_player] + displacement )
#     positions[current_player] = ( positions[current_player] + displacement - 1 ) % 10 + 1
#     # Sum the position to the score of the player
#     scores[current_player] += positions[current_player]
#
#     # print()
#     # print("{} rolls".format( nr_rolls ))
#     # print("Player {}, position {}, score {}".format( current_player, positions[current_player], scores[current_player] ))
#
#     if scores[current_player] >= 1000:
#     # if scores[current_player] >= 30:
#         break
#
#     # Change player
#     current_player = ( current_player + 1 ) % 2
#
#
# print("\n\n--------------\nFirst part\n\n")
# print("The score of the loser multiplied by the number of rolls is: {}".format( nr_rolls * min(scores) ))



################################################################################
# Second part
################################################################################

# Function to get all the possible outcomes of three rolls
def get_results_three_rolls():
    # Get all the results
    results = []
    for roll1 in range( 1, 4 ):
        for roll2 in range( 1, 4 ):
            for roll3 in range( 1, 4 ):
                results.append( roll1 + roll2 + roll3 )

    # Get the unique results and their count
    unique_results = []
    for result in results:
        result_found = False
        for i in range( len( unique_results ) ):
            if result == unique_results[i][0]:
                unique_results[i][1] += 1
                result_found = True
                break
        if not result_found:
            unique_results.append( [ result, 1 ] )

    return unique_results

# List of possible results of three rolls
results_three_rolls = get_results_three_rolls()

# Recursive function to get the amount of times each player wins
def get_times_win( positions, scores, player ):
    # Check if some of the scores are above the maximum
    if scores[ 0 ] >= 21:
        # Player 1 wins
        return [ 1, 0 ]
    if scores[ 1 ] >= 21:
        # Player 0 wins
        return [ 0, 1 ]

    # If no player has won, initialize the number of times a player won
    wins = [ 0, 0 ]

    # Compute all the possible outcomes
    for result in results_three_rolls:
        # Update the position and score of the current player
        new_positions = [ el for el in positions ]
        new_scores = [ el for el in scores ]

        new_positions[ player ] = ( new_positions[player] + result[0] - 1 ) % 10 + 1
        new_scores[ player ]    = new_scores[player] + new_positions[ player ]

        # Call this function recursively for the turn of the next player
        wins_prop = get_times_win( new_positions, new_scores, ( player + 1 ) % 2 )

        # Update the times that each player has won
        for i_player in range( 2 ):
            wins[ i_player ] += wins_prop[ i_player ] * result[ 1 ]

    return wins

wins = get_times_win( original_positions, [0, 0], 0 )
print( wins )


print("\n\n--------------\nSecond part\n\n")
print("The player that wins the most wins in {} universes".format( max( wins ) ))
