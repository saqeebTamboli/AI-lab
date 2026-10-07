"""
A* Search Algorithm for 8-Puzzle Problem
Heuristic: Number of Misplaced Tiles

f(n) = g(n) + h(n)
g(n) = Depth of the node (cost from start to current node)
h(n) = Number of Misplaced Tiles (estimated cost from current to goal)
"""

import heapq
from typing import Tuple, List, Dict, Optional


def get_neighbors(state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
    """Get all possible neighboring states by moving the blank tile."""
    neighbors = []
    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            new_zero = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]
            neighbors.append(tuple(new_state))

    return neighbors


def heuristic_misplaced_tiles(state: Tuple[int, ...], goal: Tuple[int, ...]) -> int:
    """Count how many tiles are not in their goal positions."""
    misplaced = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            misplaced += 1
    return misplaced


def a_star_misplaced_tiles(initial: Tuple[int, ...], goal: Tuple[int, ...]) -> Optional[List[Tuple[int, ...]]]:
    """Return the path from initial to goal using A* with misplaced-tiles heuristic."""
    counter = 0
    open_list = [(0, counter, initial, [initial], 0)]
    visited = set()
    g_values: Dict[Tuple[int, ...], int] = {initial: 0}

    while open_list:
        f_n, _, current, path, g_n = heapq.heappop(open_list)

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue

            new_g_n = g_n + 1
            h_n = heuristic_misplaced_tiles(neighbor, goal)
            f_n_neighbor = new_g_n + h_n

            if neighbor not in g_values or new_g_n < g_values[neighbor]:
                g_values[neighbor] = new_g_n
                counter += 1
                heapq.heappush(open_list, (f_n_neighbor, counter, neighbor, path + [neighbor], new_g_n))

    return None


def print_puzzle(state: Tuple[int, ...]) -> None:
    """Print the puzzle grid."""
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


def print_solution(solution: Optional[List[Tuple[int, ...]]], title: str) -> None:
    """Display the final solution path."""
    if solution:
        print(f"\n{'='*50}")
        print(title)
        print(f"{'='*50}")
        print("Number of moves:", len(solution) - 1)
        for idx, state in enumerate(solution):
            print(f"\nStep {idx}:")
            print_puzzle(state)
    else:
        print(f"No solution found for {title}")


if __name__ == "__main__":
    initial_state = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    print("A* SEARCH - 8 PUZZLE PROBLEM")
    print("Heuristic: Number of Misplaced Tiles")
    print("Initial State:")
    print_puzzle(initial_state)
    print("Goal State:")
    print_puzzle(goal_state)

    solution = a_star_misplaced_tiles(initial_state, goal_state)
    print_solution(solution, "A* (Misplaced Tiles)")
