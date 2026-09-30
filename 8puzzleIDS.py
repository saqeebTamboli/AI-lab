                 
# 8 Puzzle using Iterative Deepening Search (IDS)

def get_neighbors(state):
    neighbors = []
    zero = state.index(0)

    row = zero // 3
    col = zero % 3

    moves = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    for dr, dc in moves:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            new_zero = nr * 3 + nc

            new_state = list(state)
            new_state[zero], new_state[new_zero] = \
                new_state[new_zero], new_state[zero]

            neighbors.append(tuple(new_state))

    return neighbors


def depth_limited_search(state, goal, limit, path):
    if state == goal:
        return path

    if limit == 0:
        return None

    for neighbor in get_neighbors(state):

        # Avoid cycles in the current path
        if neighbor not in path:
            result = depth_limited_search(
                neighbor,
                goal,
                limit - 1,
                path + [neighbor]
            )

            if result is not None:
                return result

    return None


def ids(initial, goal, max_depth=30):
    for depth in range(max_depth + 1):

        result = depth_limited_search(
            initial,
            goal,
            depth,
            [initial]
        )

        if result is not None:
            return result

    return None


def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


# 0 represents the blank space
initial = (
    1, 2, 3,
    4, 0, 6,
    7, 5, 8
)

goal = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

solution = ids(initial, goal)

if solution:
    print("IDS Solution:")
    print("Number of moves:", len(solution) - 1)

    for state in solution:
        print_puzzle(state)
else:
    print("No solution found.")
