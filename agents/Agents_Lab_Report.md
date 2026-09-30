# Agents: Laboratory Exercise
**Constructing a Goal-Based Agent using a Large Language Model**
**Lab Report**

## Task 1 – Understanding the Problem
1. **What is the environment?** 
   The environment is a discrete 2D grid map representing the warehouse, containing obstacles (`#`), free space (`.`), a starting point (`S`), and a goal (`G`). It is fully observable and deterministic.
2. **What is the goal of the agent?** 
   To determine a valid, collision-free sequence of moves that takes the vehicle from its starting position (`S`) to the dispatch area (`G`).
3. **What actions are available to the agent?** 
   Moving Up, Down, Left, or Right by exactly one grid square (provided the target square is not an obstacle or out of bounds).
4. **What information must the agent maintain in order to choose its next action?** 
   The agent must maintain its current state (row and column coordinates). Because it uses a search algorithm, it must also maintain a "frontier" of states to explore and a "visited" set to avoid looping infinitely, along with the sequence of actions that led to each state.
5. **Why is this an example of a goal-based agent rather than a simple reflex agent?** 
   A simple reflex agent only acts based on the current percept (its immediate surroundings), which would cause it to easily get trapped in dead-ends or loops in a maze. A goal-based agent explicitly considers future states and searches for a sequence of actions that achieves a specific objective (reaching `G`).

**Think About It**
- *Suppose the warehouse becomes twice as large. Would the same search strategy still be appropriate?*
  If we use Breadth-First Search (BFS), it would still guarantee the shortest path, but it would become very slow and consume a lot of memory because it explores uniformly in all directions. 
- *What additional difficulties might arise?*
  The exponential growth of the search space (time and space complexity). For a much larger map, we would need to switch to an informed search strategy like A* (using a heuristic like Manhattan distance) to pull the search direction toward the goal efficiently.

---

## Task 2 – Designing the Agent
- **The Environment**: A 2D array/grid parsed from the text map.
- **The Current State**: A tuple `(row, column)` representing the agent's coordinates.
- **The Goal**: The tuple `(goal_row, goal_column)` where `G` is located.
- **The Available Actions**: `Move(Up)`, `Move(Down)`, `Move(Left)`, `Move(Right)` (with transition checks ensuring the agent doesn't hit a `#`).
- **The Decision-making component**: A search algorithm (like BFS) that takes the environment, current state, and goal, and outputs a list of actions.

**Simple Block Diagram (Textual Representation)**:
```
[ Environment (Warehouse Map) ] <------- (Action Sequence) ---------+
       |                                                            |
 (Percept: Map layout, S, G)                                        |
       v                                                            |
[ Goal-Based Agent ]                                                |
  |-- Current State: (x, y)                                         |
  |-- Goal: Reach (x_g, y_g)                                        |
  |-- Decision Component: BFS Search Algorithm ---------------------+
```

---

## Task 3 – Prompt Engineering
**Prompt Used**:
*"Write a well-documented Python program implementing a goal-based agent for the warehouse navigation problem shown above. The program should represent the warehouse as a two-dimensional grid, determine a collision-free path from S to G, avoid all obstacles, print either the path found or a suitable message if no path exists, and explain the search algorithm that has been chosen and why it is appropriate. Use standard Python libraries."*

1. **Did the LLM generate a working program on the first attempt?** 
   Yes, the generated Python program executed flawlessly on the first run and successfully printed the 20-step optimal path.
2. **If not, how can you improve your prompt?** 
   While it worked the first time, if it had failed (e.g. by passing through walls), the prompt could be improved by explicitly defining that `[row][col] == '#'` means the transition is strictly forbidden.
3. **What search algorithm did the LLM choose?** 
   Breadth-First Search (BFS).
4. **Why do you think the LLM selected this algorithm?** 
   In a grid where every move costs exactly 1 unit (unweighted graph), BFS is mathematically guaranteed to find the optimal (shortest) path. It is the most standard, reliable, and easiest-to-implement algorithm for this specific type of unweighted maze-solving problem.
