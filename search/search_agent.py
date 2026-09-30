import heapq
import math
from collections import deque

class SearchAgent:
    def __init__(self, map_str):
        self.grid = [list(row) for row in map_str.strip().split('\n')]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = None
        self.goal = None
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'G':
                    self.goal = (r, c)

    def get_neighbors(self, state):
        r, c = state
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

    def bfs(self):
        if not self.start or not self.goal: return None, 0
        queue = deque([(self.start, [self.start])])
        visited = set([self.start])
        states_expanded = 0
        
        while queue:
            current, path = queue.popleft()
            states_expanded += 1
            
            if current == self.goal:
                return path, states_expanded
                
            for nxt in self.get_neighbors(current):
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))
                    
        return None, states_expanded

    def a_star(self, heuristic_type="manhattan", multiplier=1.0):
        if not self.start or not self.goal: return None, 0
        
        def h(state):
            if heuristic_type == "zero":
                return 0
            elif heuristic_type == "euclidean":
                dist = math.sqrt((state[0]-self.goal[0])**2 + (state[1]-self.goal[1])**2)
                return dist * multiplier
            else: # manhattan
                dist = abs(state[0]-self.goal[0]) + abs(state[1]-self.goal[1])
                return dist * multiplier

        # Priority queue stores (f, tie_breaker, current_state, g, path)
        tie_breaker = 0
        frontier = [(h(self.start), tie_breaker, self.start, 0, [self.start])]
        
        # Best g-score tracker to avoid repeatedly expanding states
        best_g = {self.start: 0}
        states_expanded = 0
        
        while frontier:
            f, _, current, g, path = heapq.heappop(frontier)
            
            # If we popped a state but found a better path earlier, skip it
            if g > best_g.get(current, float('inf')):
                continue
                
            states_expanded += 1
            
            if current == self.goal:
                return path, states_expanded
                
            for nxt in self.get_neighbors(current):
                new_g = g + 1
                if new_g < best_g.get(nxt, float('inf')):
                    best_g[nxt] = new_g
                    new_f = new_g + h(nxt)
                    tie_breaker += 1
                    heapq.heappush(frontier, (new_f, tie_breaker, nxt, new_g, path + [nxt]))
                    
        return None, states_expanded

if __name__ == "__main__":
    maps = {
        "Original": """
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################
""",
        "Trivial": """
#####
#SG##
#####
""",
        "No Solution": """
#######
#S....#
###.###
#...#G#
#######
""",
        "Alternative": """
#####
#S..#
#.#.#
#..G#
#####
"""
    }
    
    print("--- Test Cases with standard A* (Manhattan) ---")
    for name, layout in maps.items():
        agent = SearchAgent(layout)
        path, expanded = agent.a_star()
        if path:
            print(f"{name} Map: Path found! Length: {len(path)-1}, Expanded: {expanded}")
        else:
            print(f"{name} Map: No solution found. Expanded: {expanded}")
            
    print("\n--- BFS vs A* on Original Map ---")
    agent = SearchAgent(maps["Original"])
    bfs_path, bfs_exp = agent.bfs()
    ast_path, ast_exp = agent.a_star()
    print(f"BFS: Length {len(bfs_path)-1}, Expanded {bfs_exp}")
    print(f"A*:  Length {len(ast_path)-1}, Expanded {ast_exp}")
    
    print("\n--- Heuristic Investigations on Original Map ---")
    h_zero_path, h_zero_exp = agent.a_star(heuristic_type="zero")
    print(f"h(n)=0          : Length {len(h_zero_path)-1 if h_zero_path else 'None'}, Expanded {h_zero_exp}")
    
    h_euc_path, h_euc_exp = agent.a_star(heuristic_type="euclidean")
    print(f"Euclidean       : Length {len(h_euc_path)-1 if h_euc_path else 'None'}, Expanded {h_euc_exp}")
    
    h_mult_path, h_mult_exp = agent.a_star(heuristic_type="manhattan", multiplier=2.0)
    print(f"Manhattan * 2   : Length {len(h_mult_path)-1 if h_mult_path else 'None'}, Expanded {h_mult_exp}")
