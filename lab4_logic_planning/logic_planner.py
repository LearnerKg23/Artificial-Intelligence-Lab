from collections import deque

class Action:
    def __init__(self, name, pre_pos, pre_neg, eff_pos, eff_neg):
        self.name = name
        self.pre_pos = set(pre_pos)
        self.pre_neg = set(pre_neg)
        self.eff_pos = set(eff_pos)
        self.eff_neg = set(eff_neg)

    def is_applicable(self, state):
        # All positive preconditions must be in the state
        if not self.pre_pos.issubset(state):
            return False
        # None of the negative preconditions can be in the state
        if not self.pre_neg.isdisjoint(state):
            return False
        return True

    def apply(self, state):
        # 1. Remove negative effects
        new_state = set(state) - self.eff_neg
        # 2. Add positive effects
        new_state = new_state.union(self.eff_pos)
        return frozenset(new_state)

def run_planner(initial_state, goal_state, actions):
    # Queue stores (current_state, plan_so_far)
    queue = deque([(frozenset(initial_state), [])])
    visited = set([frozenset(initial_state)])
    
    goal_set = set(goal_state)

    while queue:
        current_state, plan = queue.popleft()
        
        # Goal Check: All propositions in the goal state must be true
        if goal_set.issubset(current_state):
            return plan, current_state
            
        for action in actions:
            if action.is_applicable(current_state):
                next_state = action.apply(current_state)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, plan + [action.name]))
                    
    return None, None

def create_actions(include_pickup=True):
    actions = []
    locations = ['A', 'B', 'C']
    
    # Movement actions (A<->B, B<->C)
    connections = [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B')]
    for start, end in connections:
        actions.append(Action(
            name=f"Move({start}, {end})",
            pre_pos=[f"At(Robot, {start})"],
            pre_neg=[],
            eff_pos=[f"At(Robot, {end})"],
            eff_neg=[f"At(Robot, {start})"]
        ))
        
    for loc in locations:
        if include_pickup:
            # PickUp action
            actions.append(Action(
                name=f"PickUp(Package, {loc})",
                pre_pos=[f"At(Robot, {loc})", f"At(Package, {loc})"],
                pre_neg=[f"Holding(Package)"],
                eff_pos=[f"Holding(Package)"],
                eff_neg=[f"At(Package, {loc})"]
            ))
        
        # Drop action
        actions.append(Action(
            name=f"Drop(Package, {loc})",
            pre_pos=[f"At(Robot, {loc})", f"Holding(Package)"],
            pre_neg=[],
            eff_pos=[f"At(Package, {loc})"],
            eff_neg=[f"Holding(Package)"]
        ))
    
    return actions

if __name__ == "__main__":
    initial = ["At(Robot, A)", "At(Package, A)"]
    goal = ["At(Package, C)"]
    
    print("--- Test A: Solvable Problem ---")
    actions = create_actions(include_pickup=True)
    plan, final_state = run_planner(initial, goal, actions)
    if plan:
        print("Plan found:", plan)
        print("Final State:", set(final_state))
    else:
        print("No plan found")
        
    print("\n--- Test B: Impossible Problem (No PickUp action) ---")
    actions_impossible = create_actions(include_pickup=False)
    plan_imp, _ = run_planner(initial, goal, actions_impossible)
    if plan_imp:
        print("Plan found:", plan_imp)
    else:
        print("No plan found")
        
    print("\n--- Test C: Irrelevant Actions Check ---")
    # To test if the planner mistakenly thinks robot reaching C equals package reaching C
    goal_robot = ["At(Robot, C)"]
    plan_rob, _ = run_planner(initial, goal_robot, actions)
    print("Goal = Robot at C -> Plan:", plan_rob)
    print("Notice the package was left behind because the goal didn't require the package.")
