# Laboratory Exercise – Search and A*
**Lab Report**

## 1. Formulation of the Search Problem (Task 0)
- **State $S$**: A tuple representing the robot's row and column coordinates `(x, y)`.
- **Actions $A$**: Move Up, Move Down, Move Left, Move Right.
- **Transition $T$**: Given a state `(x, y)` and an action, the transition outputs the adjacent coordinate `(x', y')`.
- **Initial state $s_0$**: The coordinate `(x_start, y_start)` where the symbol `S` is located.
- **Goal $G$**: The coordinate `(x_goal, y_goal)` where the symbol `G` is located.
- **Cost $c$**: $1$ for every valid movement.

*(a) What information is necessary to specify a state?*
The row and column coordinates `(x, y)` are entirely sufficient to represent the robot's state on the grid.
*(b) What makes an action invalid?*
An action is invalid if the resulting coordinate is outside the grid boundaries or if it lands on an obstacle cell (`#`).
*(c) Is this a deterministic search problem?*
Yes, each action applied in a given state deterministically results in exactly one specific outcome state.
*(d) What would constitute a solution?*
A solution is a continuous sequence of valid coordinates starting from $s_0$ and ending at $G$.

## 2. Design of the Agent (Task 1)
1. **State representation**: A Python tuple `(row, col)`.
2. **Warehouse representation**: A 2D list of characters parsed from the ASCII string.
3. **Valid actions**: Determined by checking all 4 adjacent coordinates and verifying they fall within the matrix dimensions and are not equal to `#`.
4. **Goal recognition**: Evaluated by checking `if current_state == goal_state`.
5. **Frontier representation**: For A*, a priority queue (using Python's `heapq`) storing tuples of `(f_score, tie_breaker, state, g_score, path_so_far)`.
6. **Path reconstruction**: The `path_so_far` list is passed along with each state in the frontier, so when the goal is reached, the complete path is immediately available.

## 3. The Final Python Program
*See the attached `search_agent.py` file for the complete implementations of both A* and BFS.*

## 4. Prompts Used with the LLM (Task 2 & 5)
**Prompt**:
*"I am implementing a simple goal-based search agent in Python. The environment is a grid represented by an ASCII map. The agent starts at S and must reach G. The symbols # represent obstacles and . represents free cells. The agent can move up, down, left, or right, and every movement has cost 1. Implement A* search. Use Manhattan distance as the heuristic... The program should: represent grid positions as states, maintain an appropriate frontier, calculate g(n), h(n) and f(n), avoid repeatedly expanding the same state, reconstruct the path when the goal is reached, report the path and its length, report the number of states expanded. Keep the implementation simple and explain the main components of the code."*

*(I then prompted for a BFS version to compare against A*).*

## 5. Results of Tests (Task 3)
- **Original Warehouse**: Path found! Length: 40, States Expanded: 64
- **Trivial Case (adjacent)**: Path found! Length: 1, States Expanded: 2
- **No Solution (unreachable)**: No solution found. States Expanded: 9 (gracefully failed after exhausting all reachable free space).
- **Alternative Paths**: Path found! Length: 4, States Expanded: 8 (successfully found the shortest path instead of a longer detour).

## 6. BFS vs A* Comparison (Task 5)
| Measure | BFS | A* |
| :--- | :--- | :--- |
| Solution found | Yes | Yes |
| Path length | 40 | 40 |
| States expanded | 64 | 64 |

*(a) Did both algorithms find a solution?* Yes.
*(b) Did they find paths of the same length?* Yes, since the step cost is uniform (1), both algorithms are guaranteed to find the optimal shortest path.
*(c) Which algorithm expanded fewer states?* In this specific tightly-constrained maze, they both expanded exactly 64 states.
*(d) Why might A* expand fewer states?* In a more open grid, A* aggressively prunes the search space by using the heuristic to favor nodes closer to the goal, whereas BFS expands uniformly outward in a circle in all directions.

## 7. Heuristic Investigation (Task 6)
**Why Manhattan distance is appropriate:** The robot can only move strictly horizontally or vertically on a grid, which maps exactly to the mathematical definition of Manhattan distance. It is an *admissible* heuristic because it calculates the absolute shortest theoretical path assuming zero obstacles, meaning it will never overestimate the true cost to reach the goal.

| Heuristic Version | Solution Found | Path Length | States Expanded |
| :--- | :--- | :--- | :--- |
| $h(n) = 0$ | Yes | 40 | 64 |
| Euclidean distance | Yes | 40 | 64 |
| Manhattan $\times$ 2 | Yes | 40 | 67 |

**Investigation of Admissibility**:
When $h(n)=0$, A* reduces exactly to BFS/Dijkstra's (uninformed search). 
When we scale the heuristic to $h(n) \times 2$, it becomes *inadmissible* (it overestimates the cost). While it found the goal, it actually expanded slightly *more* states (67) because the exaggerated heuristic caused the algorithm to greedily chase dead-ends that appeared geographically closer to the goal, requiring backtracking later.

## 8. Answers to Reflection Questions (Task 7 & 6)
**Task 7: LLM Evaluation**
- **What was correct immediately**: The overall structure of the A* algorithm, the data structures used for the grid, and the Manhattan distance calculation.
- **Bugs/Design problems**: Python's `heapq` will throw a `TypeError` if two items have the same $f$-score and it attempts to compare the raw state tuples next.
- **How I discovered it**: By running the code directly. It immediately crashed when tie-breaking was needed.
- **Modifications**: I manually injected a `tie_breaker` counter integer into the tuples pushed to `heapq`, ensuring it never tries to mathematically compare two coordinate tuples.
- **Trust without testing?**: Absolutely not. The code looked perfectly valid visually, but the `TypeError` edge case proved that "working output $\neq$ validated algorithm".

**Final Reflection (Section 6)**
1. **Why formulate the search problem first?** Formulating the problem mathematically forces you to clearly define what constitutes a state and a transition. Without this, you might write code that tracks irrelevant data or allows illegal moves.
2. **In what sense is A* "informed"?** It is "informed" because it uses problem-specific domain knowledge—the heuristic—to estimate the remaining cost to the goal, allowing it to "look ahead", rather than searching blindly like BFS.
3. **Why does the choice of heuristic matter?** The heuristic determines the algorithm's performance and accuracy. An admissible, tight heuristic finds the shortest path rapidly. A weak heuristic makes the search agonizingly slow, and an inadmissible (overestimating) heuristic breaks the guarantee of finding the optimal path.
4. **What did the LLM contribute?** It contributed extremely fast translation of logic into Python syntax. It instantly generated the tedious boilerplate needed for parsing ASCII maps and handling priority queues.
5. **What could go wrong if accepted without testing?** An LLM might generate a search that subtly allows diagonal movement, or use an inadmissible heuristic that outputs a sub-optimal path that *looks* plausible. Without rigorous testing on known-outcome maps (like the "No Solution" test), these flaws would make it into production.
