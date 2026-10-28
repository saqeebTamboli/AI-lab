def cost(state):
    conflicts = 0
    N = len(state)

    for i in range(N):
        for j in range(i + 1, N):
            if (state[i] == state[j] or
                    abs(state[i] - state[j]) == abs(i - j)):
                conflicts += 1

    return conflicts


def get_neighbors(state):
    neighbors = []
    N = len(state)

    for i in range(N):
        for j in range(i + 1, N):
            new_state = state.copy()
            new_state[i], new_state[j] = new_state[j], new_state[i]
            neighbors.append((new_state, i, j))

    return neighbors


def hill_climbing(state):
    current = state.copy()

    while True:
        print("\nCurrent state:", tuple(current))
        print("Current cost:", cost(current))

        if cost(current) == 0:
            print("Goal state reached!")
            return current

        neighbors = get_neighbors(current)

        print("\nNeighbor states and costs:")

        for neighbor, i, j in neighbors:
            print(
                f"Swap (x{i}, x{j}): {tuple(neighbor)}, "
                f"Cost = {cost(neighbor)}"
            )

        best, i, j = min(
            neighbors,
            key=lambda item: cost(item[0])
        )

        if cost(best) >= cost(current):
            print("No better neighbor. Algorithm terminates.")
            return current

        print(f"\nSelected swap: (x{i}, x{j})")
        current = best


N = int(input("Enter the number of queens: "))

initial_state = list(map(
    int,
    input(f"Enter {N} row values (1 to {N}), separated by spaces: ").split()
))

if N < 2 or len(initial_state) != N or any(
    x < 1 or x > N for x in initial_state
):
    print("Invalid input! Enter N row values between 1 and N.")
else:
    initial_state = [x - 1 for x in initial_state]

    solution = hill_climbing(initial_state)

    print("\nFinal state:", tuple(x + 1 for x in solution))
    print("Final cost:", cost(solution))

    print("\nChessboard:")
    for row in range(N):
        for col in range(N):
            if solution[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
                                                                        