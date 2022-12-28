import time
import re
from collections import deque, defaultdict
# To copy dictonarys of lists
from copy import deepcopy

message = '''
This produces the correct result, but it is slow. A faster implementation is
written in "main3.py", which I found in reddit/github. Both solutions work in
the same way.
'''

print(message)

# Requeriments of each robot:
COSTS = {
    'ore':      [ 'ore' ],
    'clay':     [ 'ore' ],
    'obsidian': [ 'ore', 'clay' ],
    'geode':    [ 'ore', 'obsidian' ]
}

# Read the different blueprints
blueprints = []
with open( "input.txt", "r" ) as f:
    for line in f:
        match = re.findall( r"^Blueprint\s([0-9]+).+?ore\srobot\scosts\s([0-9]+).+?clay\srobot\scosts\s([0-9]+).+?obsidian\srobot\scosts\s([0-9]+)\sore\sand\s([0-9]+).+?geode\srobot\scosts\s([0-9]+)\sore\sand\s([0-9]+).+?$", line )
        if len(match) > 0:
            # Store the costs in the blueprint
            costs = {
                'ore':      [ int(match[0][1]) ],
                'clay':     [ int(match[0][2]) ],
                'obsidian': [ int(match[0][3]), int(match[0][4]) ],
                'geode':    [ int(match[0][5]), int(match[0][6]) ]
            }

            # Get the maximum resources needed of each type to construct any robot
            max_costs = { key : 0 for key in costs.keys() }
            for res_max in max_costs.keys():
                for res_cost in COSTS.keys():
                    for i in range( len( COSTS[res_cost] ) ):
                        if COSTS[res_cost][i] == res_max:
                            if costs[res_cost][i] > max_costs[res_max]:
                                max_costs[res_max] = costs[res_cost][i]

            blueprints.append( [ costs, max_costs ] )

################################################################################
# First part
################################################################################

start_time = time.time()

# Function to get the states after applying all available actions in a given state
def get_possible_states( state, blueprint, max_resources_needed ):
    # It is always possible to not do anything, so I initialize the list of states
    # with the current state
    next_states = [ deepcopy( state ) ]

    # Attempt to buy each type of robot
    for res in state[0].keys():
        # Don't create more bots than what makes you able to build any robot in one step.
        # Since it takes one step to build a robot, if I am able to produce all 
        # the needed resources in that same step it does not make sense to have
        # more robots producing this. So I don't consider these states.
        if state[0][res][0] > max_resources_needed[ res ] and res != "geode":
            # enough_resources = False
            continue

        # Check if I have enough resources of each type
        enough_resources = True
        for i in range( len( blueprint[res] ) ):
            # Consider the amount of resources that I had before this step
            if state[0][COSTS[res][i]][1] - state[0][COSTS[res][i]][0] < blueprint[res][i]:
                enough_resources = False
                break

        # If I have enough resources, create a new state with the result of buying it
        if enough_resources:

            new_state = deepcopy( state )

            # Subtract the resources
            for i in range( len( blueprint[res] ) ):
                new_state[0][COSTS[res][i]][1] -= blueprint[res][i]

            # Check that the amount of resources is correct
            assert all( [ el[1] >= 0 for el in new_state[0].values() ] ), "Invalid number of resources"

            # Add the robot
            new_state[0][res][0] += 1

            # Add this to the list of next states
            next_states.append( new_state )

            # If I can create a geode robot, only create that
            if res == "geode":
                return [ new_state ]

    return next_states

# Function to get the best score that can be achieved a blueprint
def get_best_score( blueprint, max_resources_needed, time_limit ):
    # Each state has the elements:
    #   [ dic with nr of robots and resources, current time, fitness ]
    # Initially I have only one ore robot, and no resources
    initial_state = [ {
        'ore':      [ 1, 0 ],
        'clay':     [ 0, 0 ],
        'obsidian': [ 0, 0 ],
        'geode':    [ 0, 0 ]
        }, 0, 0
    ]

    # Queue of states to explore
    states_queue = deque( [ initial_state ] )

    # Best score of an state at the end
    best_score = 0

    # States already seen
    seen_states = set()

    # Best amount of geodes found at a given time
    best_geode_time = defaultdict( int )

    # Iterate until there are no states to explore (all have finished)
    while len(states_queue) != 0:
        # Get one state
        state = states_queue.pop()

        if str(state) in seen_states:
            continue
        seen_states.add( str(state) )

        # Add one to the time of the state
        state[1] += 1

        # If I reached the end of evolution, stop
        if state[1] > time_limit:
            # Compare with the best score
            # The score of the state is simply the number of geodes
            best_score = max( best_score, state[0]['geode'][1] )
            # print( state )
            # print(best_score)

            # Do not propagate this state further
            continue

        else:
            # Each robot gets one unit of its resource
            for res in state[0].keys():
                state[0][res][1] += state[0][res][0]

            # Get the next possible states
            next_states = get_possible_states( state, blueprint, max_resources_needed )

            # Add the next states to the queue
            for next_state in next_states:

                # Don't explore paths with less geode than previously found at the same time step
                if next_state[0]["geode"][1] < best_geode_time[state[1]]:
                    continue
                elif next_state[0]["geode"][1] > best_geode_time[state[1]]:
                    best_geode_time[state[1]] = next_state[0]["geode"][1]

                states_queue.append( next_state )

    return best_score

# Get the score of all the blueprints
scores = [ 0 for _ in range(len(blueprints)) ]
quality_level_total = 0
for i in range( len( blueprints ) ):
    scores[i] = get_best_score( blueprints[i][0], blueprints[i][1], 24 )
    # Add to the total quality level counter
    quality_level_total += ( i + 1 ) * scores[i]

    print("\nScore of blueprint {}: {}".format( i + 1, scores[i] ))

print("\n\n--------------\nFirst part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Total quality level: {}".format( quality_level_total ))



################################################################################
# Second part
################################################################################

start_time = time.time()

# Get the score of all the blueprints
scores = []
scores_product = 1
for i in range( min( len( blueprints ), 3 ) ):
    scores.append(get_best_score( blueprints[i][0], blueprints[i][1], 32 ))
    # Update the product of scores
    scores_product *= scores[-1]

    print("\nScore of blueprint {}: {}".format( i + 1, scores[i] ))

print( scores )

print("\n\n--------------\nSecond part\n--------------")
print("\t--- Execution time: {:.5} s ---\n\n".format(time.time() - start_time))
print("Product of number of geodes: {}".format( scores_product ))
