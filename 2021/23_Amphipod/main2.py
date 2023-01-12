import heapq

SAMPLE_INPUT = [
    "#############",
    "#...........#",
    "###B#C#B#D###",
    "  #A#D#C#A#",
    "  #########",
]


def solve(lines):
    # Corridor
    state = [[0] for _ in range(11)]
    # Amphipods in the rooms
    for line in lines[2 : len(lines) - 1]:
        for i in range(2, 9, 2):
            '''
                A -> 1
                B -> 2
                C -> 3
                D -> 4
            '''
            state[i].append(ord(line[i + 1]) - ord("A") + 1)

    # Convert this to a tuple of tuples, so it can be used as a key to a dic
    state = tuple(tuple(stack) for stack in state)

    # Dictionary of visited states and queue of states to visit
    visited, queue = {state: 0}, [(0, state)]
    while queue:
        # Get the next state from the queue and the cost for getting to that state
        _, state = heapq.heappop(queue)
        cost = visited[state]

        # Check if all amphipods are located in their corresponding room.
        # If they are, the best configuration has been found.
        if all(all(a == b for b in state[2 * a][1:]) for a in range(1, 5)):
            print("algo")
            return cost

        # Get the next moves
        priority_moves, other_moves = [], []
        for i, src in enumerate(state):
            # Only consider the locations where there is an amphipod (this is, a != 0)
            # in the following loop
            for x, a in enumerate(src):
                if a:
                    break
            else:
                # If there is no amphipod, continue to the next column in the state
                continue

            # If the amphipod is at its corresponding room and there are no other 
            # different amphipods in the current room, continue.
            if i == 2 * a and not any(b and b != a for b in src):
                continue

            # Iterate over the state to find the possible destination
            for j, dst in enumerate(state):

                # If I am at the source room or the corridor to get to the destination
                # is blocked, continue
                if i == j or any(
                    state[k][0] for k in (range(i + 1, j) if i < j else range(j + 1, i))
                ):
                    continue

                # Find the first empty position in the destination column, starting
                # from the bottom.
                for y in range(len(dst) - 1, -1, -1):
                    if not dst[y]:
                        break
                # If there is no available position, continue to the next possible
                # destination
                else:
                    continue

                # If this movement leaves the amphipod at its corresponding room,
                # add it to the list of prioritary movements
                if j == 2 * a:
                    if all(not b or b == a for b in dst):
                        priority_moves.append((a, i, x, j, y))

                # Else, if the destination is a corridor location that is not 
                # directly in front to a room, add it to the list of non-prioritary
                # movements
                elif j not in range(2, 9, 2):
                    if i in range(2, 9, 2) and not dst[0]:
                        other_moves.append((a, i, x, j, y))

                # The other two options would be:
                #   - Amphipod moving to a room other than its destination.
                #   - Amphipod moving to a corridor location right in front of a room.
                # These two are forbidden, so we do not consider them

        # Compute the cost of the movements.
        # If there are prioritary movements, only consider those.
        for a, i, x, j, y in [priority_moves[0]] if priority_moves else other_moves:
            # Compute the new cost.
            # The cost per step is:
            #   A -> 1
            #   B -> 10
            #   C -> 100
            #   D -> 1000
            cost2 = cost + 10 ** (a - 1) * (abs(i - j) + x + y)

            # Convert the state to a list and update it
            state2 = [list(stack) for stack in state]
            state2[i][x] = 0
            state2[j][y] = a
            # Convert the new state back to a tuple
            state2 = tuple(tuple(stack) for stack in state2)

            # If the state has not been visited or it had been visited before with
            # a larger energy cost, mark it as visited and add it to the heap.
            if state2 not in visited or visited[state2] > cost2:
                visited[state2] = cost2
                heapq.heappush(queue, (cost2, state2))


def part1(lines):
    """
    >>> part1(SAMPLE_INPUT)
    12521
    """
    return solve(lines)


def part2(lines):
    """
    >>> part2(SAMPLE_INPUT)
    44169
    """
    return solve(lines[0:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + lines[3:])


parts = (part1, part2)

print("Part 1:")
print( part1( SAMPLE_INPUT ) )
# print("Part 2:")
# print( part2( SAMPLE_INPUT ) )
