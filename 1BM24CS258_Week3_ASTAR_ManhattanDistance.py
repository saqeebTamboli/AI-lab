import heapq
import copy

class PuzzleNode:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board       # 2D list representing the puzzle layout
        self.parent = parent     # Pointer to the parent node to reconstruct path
        self.move = move         # The direction of movement that led here
        self.g = g               # Cost from start to current node (depth)
        self.h = h               # Heuristic cost (Manhattan Distance)
        self.f = g + h           # Total evaluated cost

    # Custom comparator for the priority queue to grab the lowest f(n)
    def __lt__(self, other):
        return self.f < other.f

def get_manhattan_distance(current_board, goal_board):
    """
    Heuristic Function h(n): Computes the sum of absolute horizontal 
    and vertical distances of all tiles from their goal positions.
    """
    distance = 0
    goal_positions = {}
    for r in range(len(goal_board)):
        for c in range(len(goal_board[r])):
            goal_positions[goal_board[r][c]] = (r, c)
            
    for r in range(len(current_board)):
        for c in range(len(current_board[r])):
            tile = current_board[r][c]
            if tile != 0:  # Skip the blank space
                goal_r, goal_c = goal_positions[tile]
                distance += abs(r - goal_r) + abs(c - goal_c)
                
    return distance

def find_blank_space(board):
    """Locates the row and column coordinates of the blank space (0)."""
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 0:
                return r, c

def get_neighbors(node, goal_board):
    """Generates all possible valid moves (Up, Down, Left, Right) from the current state."""
    neighbors = []
    r, c = find_blank_space(node.board)
    
    moves = {
        "Up": (r - 1, c),
        "Down": (r + 1, c),
        "Left": (r, c - 1),
        "Right": (r, c + 1)
    }
    
    for move_name, (next_r, next_c) in moves.items():
        if 0 <= next_r < len(node.board) and 0 <= next_c < len(node.board):
            new_board = copy.deepcopy(node.board)
            # Swap blank space with the chosen adjacent tile
            new_board[r][c], new_board[next_r][next_c] = new_board[next_r][next_c], new_board[r][c]
            
            g_cost = node.g + 1
            h_cost = get_manhattan_distance(new_board, goal_board)
            
            neighbors.append(PuzzleNode(new_board, node, move_name, g_cost, h_cost))
            
    return neighbors

def board_to_tuple(board):
    """Converts a 2D list into a hashable tuple structure for tracking duplicates."""
    return tuple(tuple(row) for row in board)

def print_solution_path(node):
    """Traverses backward from the goal state via parents to print the sequence."""
    path = []
    current = node
    while current:
        path.append(current)
        current = current.parent
    path.reverse()
    
    print(f"--- Found Solution in {len(path) - 1} Moves ---")
    for step, state in enumerate(path):
        if step == 0:
            print("Initial State:")
        else:
            print(f"Move {step}: {state.move} (g={state.g}, h={state.h}, f={state.f})")
            
        for row in state.board:
            print(row)
        print()

def a_star_search(start_board, goal_board):
    """Performs A* Search using the Manhattan Distance heuristic."""
    start_h = get_manhattan_distance(start_board, goal_board)
    start_node = PuzzleNode(start_board, g=0, h=start_h)
    
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_list = set()
    
    nodes_expanded = 0
    
    while open_list:
        current_node = heapq.heappop(open_list)
        nodes_expanded += 1
        
        if current_node.board == goal_board:
            print_solution_path(current_node)
            print(f"Total nodes explored during search: {nodes_expanded}")
            return True
            
        board_tuple = board_to_tuple(current_node.board)
        if board_tuple in closed_list:
            continue
        closed_list.add(board_tuple)
        
        for neighbor in get_neighbors(current_node, goal_board):
            if board_to_tuple(neighbor.board) not in closed_list:
                heapq.heappush(open_list, neighbor)
                
    print("No solution found.")
    return False

# --- Executable Entry Point ---
if __name__ == "__main__":
    # Your specified initial state: "123406758"
    initial_puzzle = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]

    # Standard sequential goal state: "123456780"
    target_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    a_star_search(initial_puzzle, target_puzzle)
