import heapq
import copy

class PuzzleNode:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board       # 2D list representing the puzzle layout
        self.parent = parent     # Pointer to the parent node to reconstruct path
        self.move = move         # The direction of movement that led here
        self.g = g               # Cost from start to current node (depth)
        self.h = h               # Heuristic cost (misplaced tiles)
        self.f = g + h           # Total evaluated cost

    # Custom comparator for the priority queue to always grab the lowest f(n)
    def __lt__(self, other):
        return self.f < other.f

def get_misplaced_tiles(current_board, goal_board):
    """
    Heuristic Function h(n): Counts how many numbered tiles 
    are out of their target goal position.
    """
    misplaced = 0
    for i in range(len(current_board)):
        for j in range(len(current_board[0])):
            # Only count actual numbered tiles, ignore the blank space (0)
            if current_board[i][j] != 0 and current_board[i][j] != goal_board[i][j]:
                misplaced += 1
    return misplaced

def find_blank_space(board):
    """Locates the row and column coordinates of the blank space (0)."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 0:
                return r, c

def get_neighbors(node, goal_board):
    """Generates all possible valid moves (Up, Down, Left, Right) from the current state."""
    neighbors = []
    r, c = find_blank_space(node.board)
    
    # Define valid directional shifts for the blank spot
    moves = {
        "Up": (r - 1, c),
        "Down": (r + 1, c),
        "Left": (r, c - 1),
        "Right": (r, c + 1)
    }
    
    for move_name, (next_r, next_c) in moves.items():
        # Ensure the move is within boundaries
        if 0 <= next_r < len(node.board) and 0 <= next_c < len(node.board[0]):
            # Deep copy the board to execute the tile swap
            new_board = copy.deepcopy(node.board)
            # Swap blank space with the chosen adjacent tile
            new_board[r][c], new_board[next_r][next_c] = new_board[next_r][next_c], new_board[r][c]
            
            # Calculate updated path costs
            g_cost = node.g + 1
            h_cost = get_misplaced_tiles(new_board, goal_board)
            
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
    """Performs the A* Search algorithm using the misplaced tiles heuristic."""
    # Initialize the starting node
    start_h = get_misplaced_tiles(start_board, goal_board)
    start_node = PuzzleNode(start_board, g=0, h=start_h)
    
    # Priority queue (Open List) and Tracking Set (Closed List)
    open_list = []
    heapq.heappush(open_list, start_node)
    closed_list = set()
    
    while open_list:
        # Extract the node with the lowest total f(n) cost
        current_node = heapq.heappop(open_list)
        
        # Check if the target layout has been attained
        if current_node.board == goal_board:
            print_solution_path(current_node)
            return True
            
        # Convert state structure to add to history tracking
        board_tuple = board_to_tuple(current_node.board)
        if board_tuple in closed_list:
            continue
        closed_list.add(board_tuple)
        
        # Explore valid neighboring paths
        for neighbor in get_neighbors(current_node, goal_board):
            if board_to_tuple(neighbor.board) not in closed_list:
                heapq.heappush(open_list, neighbor)
                
    print("No solution found.")
    return False

# --- Execution Example ---
if __name__ == "__main__":
    # 0 represents the empty/blank space
    initial_puzzle = [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8]
    ]

    target_puzzle = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    a_star_search(initial_puzzle, target_puzzle)
