from collections import deque

class WarehouseAgent:
    def __init__(self, warehouse_map):
        self.warehouse_map = [list(row) for row in warehouse_map.strip().split('\n')]
        self.rows = len(self.warehouse_map)
        self.cols = len(self.warehouse_map[0])
        self.start = None
        self.goal = None
        
        # Locate start and goal
        for r in range(self.rows):
            for c in range(self.cols):
                if self.warehouse_map[r][c] == 'S':
                    self.start = (r, c)
                elif self.warehouse_map[r][c] == 'G':
                    self.goal = (r, c)

    def get_neighbors(self, r, c):
        neighbors = []
        # Directions: Up, Down, Left, Right
        directions = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]
        
        for dr, dc, action in directions:
            nr, nc = r + dr, c + dc
            # Check bounds and obstacles
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.warehouse_map[nr][nc] != '#':
                    neighbors.append((nr, nc, action))
        return neighbors

    def find_path(self):
        """
        Uses Breadth-First Search (BFS) to find the shortest collision-free path.
        BFS is chosen because the step cost between all adjacent grids is identical (1),
        guaranteeing the optimal (shortest) path to the goal.
        """
        if not self.start or not self.goal:
            return None, "Start or Goal not found in the map."

        # Queue stores tuples of (current_position, path_of_actions, path_of_coordinates)
        queue = deque([(self.start, [], [self.start])])
        visited = set([self.start])

        while queue:
            current_pos, actions, path_coords = queue.popleft()

            if current_pos == self.goal:
                return actions, path_coords

            for nr, nc, action in self.get_neighbors(*current_pos):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), actions + [action], path_coords + [(nr, nc)]))

        return None, "No path exists."

    def print_path(self, path_coords):
        # Create a copy of the map to draw the path
        display_map = [row[:] for row in self.warehouse_map]
        for r, c in path_coords:
            if display_map[r][c] not in ('S', 'G'):
                display_map[r][c] = '*'
                
        print("\nWarehouse Map with Path (*):")
        for row in display_map:
            print("".join(row))

if __name__ == "__main__":
    warehouse_layout = """
#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################
"""
    agent = WarehouseAgent(warehouse_layout.strip())
    
    print("Agent started search...")
    actions, coords = agent.find_path()
    
    if actions is None:
        print(coords)  # Prints error message
    else:
        print(f"Path found in {len(actions)} steps!")
        print(f"Sequence of actions: {actions}")
        agent.print_path(coords)
