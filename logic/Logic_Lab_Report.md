# Logical Reasoning for Planning
**Laboratory Report**

## 1. Specification of the Planning Problem
- **Initial State $I$**: `{At(Robot, A), At(Package, A)}`
- **Goal $G$**: `{At(Package, C)}`
- **Available Actions**: 
  - `Move(A, B)`, `Move(B, A)`, `Move(B, C)`, `Move(C, B)`
  - `PickUp(Package, L)` for any location L
  - `Drop(Package, L)` for any location L

**Action Details (Example)**:
- `PickUp(Package, A)`:
  - **Preconditions**: `At(Robot, A)`, `At(Package, A)`
  - **Effects**: `Holding(Package)`, `¬At(Package, A)`
- `Drop(Package, C)`:
  - **Preconditions**: `At(Robot, C)`, `Holding(Package)`
  - **Effects**: `At(Package, C)`, `¬Holding(Package)`

## 2. Manually Constructed Plan
1. **Action**: `PickUp(Package, A)`
   - **State $S_1$**: `At(Robot, A), Holding(Package)`
2. **Action**: `Move(A, B)`
   - **State $S_2$**: `At(Robot, B), Holding(Package)`
3. **Action**: `Move(B, C)`
   - **State $S_3$**: `At(Robot, C), Holding(Package)`
4. **Action**: `Drop(Package, C)`
   - **State $S_4$**: `At(Robot, C), At(Package, C)`

*State $S_4$ satisfies the Goal $G$.*

## 3. Prompt Used with the LLM
*"I want to implement a simple planning agent in Python. Represent a state as a set of logical propositions. Each action should contain: a name, positive preconditions, negative preconditions, positive effects, and negative effects. An action is applicable if all of its preconditions are satisfied by the current state. When an action is applied: 1. remove its negative effects from the state; 2. add its positive effects to the state. Use breadth-first search to find a sequence of actions that achieves a specified goal. The program should also detect when no plan exists, print the resulting sequence of actions, and print the states reached after each action. Run the generated program on the warehouse problem."*

## 4. Generated Python Program
*(Please see the attached `logic_planner.py` file inside the `logic/` directory for the full LLM-assisted implementation).*

## 5. Results of Tests
- **Test A: Solvable Problem**
  - **Initial State**: `{At(Robot, A), At(Package, A)}`
  - **Goal**: `{At(Package, C)}`
  - **Result**: Plan found! `['PickUp(Package, A)', 'Move(A, B)', 'Move(B, C)', 'Drop(Package, C)']`
  - **Validity**: The plan is valid and successfully transports the package.
- **Test B: Impossible Problem (No PickUp action available)**
  - **Result**: `No plan found`
  - **Validity**: The planner correctly exhausted all reachable states without hallucinating a way to move the package, reporting failure.
- **Test C: Irrelevant Actions Check**
  - **Goal modified to**: `{At(Robot, C)}`
  - **Result**: Plan found! `['Move(A, B)', 'Move(B, C)']`
  - **Validity**: The planner correctly identified that picking up the package was completely irrelevant to the new goal, and efficiently moved only the robot to C.

## 6. Answers to "Think About It" and In-Text Questions
**Task 0: Initial Applicability**
- *Is PickUp(Package, A) applicable in the initial state?* Yes, because both of its preconditions (`At(Robot, A)` and `At(Package, A)`) are present in the initial state.
- *What about Drop(Package, C)?* No, it is not applicable. Its preconditions (`At(Robot, C)` and `Holding(Package)`) are both missing from the initial state.

**Task 2: Identifying Concepts in Code**
- **Preconditions**: Appears in `def is_applicable(self, state):` where it checks if preconditions are subsets/disjoint from the state.
- **Effects**: Appears in `def apply(self, state):` where it executes set unions and differences to generate a new state.
- **Goal**: Appears in `if goal_set.issubset(current_state):` inside the search loop to terminate planning.
- **BFS**: Appears via `queue = deque()` and `queue.popleft()`, ensuring states are expanded strictly level-by-level.

**Task 4: Logic and Search Flowchart**
```text
Current state
       ↓
Check action preconditions
       ↓
Determine applicable actions
       ↓
Generate successor state
       ↓
Search over alternatives
       ↓
     Goal?
```
*Explanation*: **Logical reasoning** provides the rigid rules of the universe (determining which actions are legally allowed and computing exactly how the world changes when they are applied). **Search** is the algorithmic engine that explores the tree of these logically-valid possibilities to find the specific sequence leading to the desired objective.

**Task 5 & 7: Prolog / Independent Verification**
*Which should you trust more: the LLM's explanation or the independently executed state transitions?*
I trust the independent execution. LLMs generate text based on statistical likelihoods and can hallucinate highly plausible but logically flawed explanations (e.g. inventing a direct path from A to C). An independent code executor or formal Prolog verifier rigidly follows mathematical logic and cannot be fooled by plausible-sounding text.

## 7. Reflection Questions
1. **Why is it useful to specify action preconditions and effects before asking an LLM to write the planner?**
   It grounds the LLM in a rigid logical framework. If you just ask it to "solve the problem," it might write a hard-coded script. Defining preconditions and effects forces it to build a generalized logical reasoning engine.
2. **Give an example of an error that could occur if the planner failed to check an action's preconditions.**
   The robot could execute `Drop(Package, C)` while it is located at `A`, magically teleporting the package to the goal without moving.
3. **Why is a plan that “looks reasonable” not necessarily a valid plan?**
   An LLM might suggest `[PickUp(Package, A), Move(A, C), Drop(Package, C)]`. To a human skimming it, it seems perfectly reasonable, but mathematically it is invalid because `A` and `C` are not directly connected in our specific warehouse model.
4. **What did the LLM contribute to the implementation?**
   The LLM contributed immense engineering productivity by instantly writing the boilerplate code for the `deque` BFS loop, the state management using Python `frozenset`s, and the class structure for the Actions.
5. **What did you have to verify independently?**
   I had to verify that the generated transitions strictly respected the preconditions, and that edge cases (like the impossible problem in Test B) wouldn't send the program into an infinite loop or cause it to hallucinate fake actions.
6. **In this laboratory, where is logical reasoning being used?**
   It is encapsulated inside the `Action` class—specifically within the `is_applicable()` method (evaluating if propositions hold true) and the `apply()` method (deducing the new state).
7. **How is planning related to the search algorithms studied in the previous module?**
   Planning *is* search. However, instead of navigating a pre-defined static map or explicitly drawn graph (like the A* grid), planning performs search over an abstract, dynamic state space generated on-the-fly by applying logical rules to propositions.
