% Declarative Knowledge Base for Logical Planning
% Action Preconditions and Effects

% move(Box, From, To)
action(move(B, X, Y), 
       [at(B, X), empty(Y)], 
       [at(B, Y), empty(X)], 
       [at(B, X), empty(Y)]).

% state definitions
initial_state([at(box1, locA), empty(locB), empty(locC)]).
goal_state([at(box1, locC)]).
