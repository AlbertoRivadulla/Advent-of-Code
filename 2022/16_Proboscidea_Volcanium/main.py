import re
from collections import deque

# Read the valve information
valves = {}
with open( "input.txt", "r" ) as f:
    for line in f:
        match_name = re.findall( r"Valve\s([A-Z]+)\shas", line )
        match_flow = re.findall( r"rate=([0-9]+);", line )
        match_tunnels = re.findall( r"valve[s]*\s(.+)$", line )

        if len( match_name ) > 0 and len( match_flow ) > 0 and len( match_tunnels ) > 0:
            # List of tunnels to which I can go from this valve
            tunnels = [ tunnel.strip() for tunnel in match_tunnels[0].split(',') ]

            # Add this valve to the dictionary
            valves[match_name[0]] = [ int(match_flow[0]), tunnels ]

# Find the working valves
working_valves = [ "AA" ]
for valve in valves.keys():
    if valves[valve][0] != 0:
        working_valves.append( valve )

# Function to compute the length of the shortest paths from one valve to each of
# the rest of them
def len_shortest_paths( valves, valve1 ):
    # Distances of the nodes to visit (the working valves)
    distances = { key : 100000 for key in valves.keys() }

    visited = []
    to_visit_queue = deque( [ valve1 ] )
    distances[ valve1 ] = 0

    # While there are nodes to visit
    while len( to_visit_queue ) > 0:
        # Get the next node to visit
        current = to_visit_queue.popleft()
        # Mark the current node as visited
        visited.append( current )

        # Add all its neighbors to the queue
        for neigh in valves[current][1]:
            if neigh not in visited:
                to_visit_queue.append( neigh )

            # Update the distance to the current node
            if distances[neigh] > distances[current] + 1:
                distances[neigh] = distances[current] + 1
                # Visit the neighbor again
                if neigh not in to_visit_queue:
                    to_visit_queue.append( neigh )

    return distances

# Find the smallest distance between each pair of valves
distances = {}
for valve in valves.keys():
    distances[valve] = len_shortest_paths( valves, valve )

################################################################################
# First part
################################################################################

# Time limit
time_limit = 30
# Initial valve
initial_valve = "AA"

# Initialize the best pressure found
best_pressure = 0
# Queue of states
# Each path has four elements:
#   [ current valve, time elapsed, pressure, visited (opened) valves ]
states = deque( [ [ initial_valve, 0, 0, { key : 0 for key in working_valves } ] ] )
states[0][3][initial_valve] = 1

# Run the loop until I run out of states
while len( states ) > 0:
    # Get the first state
    state = states.popleft()

    # Add states resulting after visiting each new valve that is not visited
    for next_valve in working_valves:
        # If the valve has not been visited yet in this path
        if state[3][next_valve] == 0:
            # New list of visited valves
            next_visited = state[3].copy()
            next_visited[next_valve] = 1

            # New time
            # Current time + distance + 1 (time to open the valve)
            next_time = state[1] + distances[state[0]][next_valve] + 1

            # If there is enough time to do this:
            if next_time < time_limit:
                # New pressure
                next_pressure = state[2] + ( time_limit - next_time ) * valves[next_valve][0]

                # Add the new state to the queue
                states.append( [ next_valve, next_time, next_pressure, next_visited ] )

                # If the pressure is larger than the best one, update it
                best_pressure = max( best_pressure, next_pressure )


print("\n\n--------------\nFirst part\n\n")
print("Best pressure: {}".format( best_pressure ))



################################################################################
# Second part
################################################################################

# Time limit
time_limit = 26
# Initial valve
initial_valve = "AA"

# Queue of states
# Each path has five elements:
#   [ current valve, time elapsed, pressure, visited (opened) valves ]
states = deque( [ [ initial_valve, 0, 0, { key : 0 for key in working_valves } ] ] )
states[0][3][initial_valve] = 1

# Paths available in the given amount of time
paths = []

# Run the loop until I run out of states
while len( states ) > 0:
    # Get the first state
    state = states.popleft()

    # Add states resulting after visiting each new valve that is not visited
    for next_valve in working_valves:
        # If the valve has not been visited yet in this path
        if state[3][next_valve] == 0:
            # New list of visited valves
            next_visited = state[3].copy()
            next_visited[next_valve] = 1

            # New time
            # Current time + distance + 1 (time to open the valve)
            next_time = state[1] + distances[state[0]][next_valve] + 1

            # If there is enough time to do this:
            if next_time < time_limit:
                # New pressure
                next_pressure = state[2] + ( time_limit - next_time ) * valves[next_valve][0]

                # Add the new state to the queue
                states.append( [ next_valve, next_time, next_pressure, next_visited ] )

            # If I reach the time limit with this, add it to the list of paths
            paths.append( [ state[2], [ key for key in state[3].keys() if state[3][key] == 1 and key != initial_valve ] ] )

# Sort the paths in decreasing order of the pressure
paths.sort( key=lambda x: x[0], reverse=True )

# Function to check if two paths share any valve
def valves_shared( path1, path2 ):
    for valve in path1[1]:
        if valve in path2[1]:
            return True
    return False

# Find the two paths with no shared valves that add the largest pressure
best_pressure = 0
for i in range( len( paths ) ):
    for j in range( 0, i - 1 ):
        # If the sum of pressures is smaller than the best, break the loop
        if paths[i][0] + paths[j][0] < best_pressure:
            break

        # Check if the two paths do not share any value
        if len( set(paths[i][1]) & set(paths[j][1]) ) == 0:
            # Update the best pressure if needed
            best_pressure = max( best_pressure, paths[i][0] + paths[j][0] )

print("\n\n--------------\nSecond part\n\n")
print("Best pressure: {}".format( best_pressure ))
