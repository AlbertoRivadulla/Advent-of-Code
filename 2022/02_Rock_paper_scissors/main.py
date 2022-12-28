import re

# First part

# Read the strategy guide
# These are:
#   A, X -> rock, score 1
#   B, Y -> paper, score 2
#   C, Z -> scissors, score 3
my_hands = []
opponent_hands = []

with open( "input.txt", "r" ) as f:
    for line in f:
        match = re.findall( r"([A,B,C])\s([X,Y,Z])$", line )
        if len(match) != 0:
            if match[0][0] == "A":
                opponent_hands.append( 0 )
            elif match[0][0] == "B":
                opponent_hands.append( 1 )
            elif match[0][0] == "C":
                opponent_hands.append( 2 )

            if match[0][1] == "X":
                my_hands.append( 0 )
            if match[0][1] == "Y":
                my_hands.append( 1 )
            if match[0][1] == "Z":
                my_hands.append( 2 )

# Counter for the score
score = 0

for i in range(len(my_hands)):
    # Add the score due to the hand that I chose
    score += my_hands[ i ] + 1

    # Check who wins
    result = my_hands[ i ] - opponent_hands[ i ]
    # Take %3 to make the list in the beginning cyclic
    result %= 3

    # Compute the score
    if result == 0:
        # Draw
        score += 3
    elif result == 1:
        # I won
        # This happens when my hand is immediately after the opponent's hand, in 
        # the list at the beginning.
        score += 6

print("\n\n--------------\nFirst part\n\n")
print("The total score is: {}".format( score ))


# Second part

# The second column in the data tells me how the round needs to end
#   X -> I lose
#   Y -> Draw
#   Z -> I win
desired_results = my_hands

# Counter for the score
score = 0

for i in range( len( desired_results ) ):
    # Add the score due to the result
    score += desired_results[ i ] * 3

    # Find out what hand I need to choose
    my_hand = opponent_hands[ i ] + desired_results[ i ] - 1
    my_hand %= 3

    score += my_hand + 1


print("\n\n--------------\nSecond part\n\n")
print("The total score is: {}".format( score ))
