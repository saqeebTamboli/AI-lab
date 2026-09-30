
def get_neighbors(state):
    neighbors = []
    zero = state.index(0)

    row = zero // 3
    col = zero % 3

    moves = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)     # Right
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


def dfs(initial, goal):
    stack = [(initial, [initial])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

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

solution = dfs(initial, goal)

if solution:
    print("DFS Solution:")
    print("Number of moves:", len(solution) - 1)

    for state in solution:
        print_puzzle(state)
else:
    print("No solution found.")