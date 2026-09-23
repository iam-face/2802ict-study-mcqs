# 2802ICT Intelligent Systems: Lecture Study Guide

Central revision notes for the lecture slides and the lab solutions in this folder. Pair this file with [Study MCQs.md](Study%20MCQs.md) for question practice.

Textbook: Russell and Norvig, *Artificial Intelligence: A Modern Approach*, 3rd edition.

The lecture numbering below follows the PDF titles. Week 1's tentative schedule listed decision trees earlier and neural networks later. The actual slide order is the one used here.

`Lecture8.pdf` in the Lectures folder is a 3006ICT robotics lecture. It is not part of this guide.

## How to use this file

1. Use the contents list to jump to one lecture.
2. Read **Need to know** first. That is the exam core.
3. Use **Definitions and formulas** when a question asks you to compute or compare.
4. Read **Lab** only where a solution PDF exists. Weeks 1 to 4, 10, and 11 have no lab solution in this folder.
5. Close each section with **Check yourself** before moving on.

## Contents

- [Course map](#course-map)
- [Search algorithms at a glance](#search-algorithms-at-a-glance)
- [Learning tasks at a glance](#learning-tasks-at-a-glance)
- [Lecture 1: Introduction and agents](#lecture-1-introduction-and-agents)
- [Lecture 2: Uninformed search](#lecture-2-uninformed-search)
- [Lecture 3: Informed search](#lecture-3-informed-search)
- [Lecture 4: Local search and CSPs](#lecture-4-local-search-and-csps)
- [Lecture 5: Machine learning basics](#lecture-5-machine-learning-basics)
- [Lecture 6: Linear models](#lecture-6-linear-models)
- [Lecture 7: Feed-forward neural networks](#lecture-7-feed-forward-neural-networks)
- [Lecture 8: Model selection and regularisation](#lecture-8-model-selection-and-regularisation)
- [Lecture 9: Decision trees](#lecture-9-decision-trees)
- [Lecture 10: Bayes nets](#lecture-10-bayes-nets)
- [Lecture 11: MDPs and reinforcement learning](#lecture-11-mdps-and-reinforcement-learning)
- [Formula card](#formula-card)

## Course map

| Lecture | Week on slides | Topic | Reading | Lab in this folder |
| --- | --- | --- | --- | --- |
| 1 | 1 | AI overview, agents, PEAS | AIMA Ch. 1-2 | None |
| 2 | 2 | Uninformed search | AIMA Ch. 3, pp. 64-91 | None |
| 3 | 3 | Informed search (greedy, A*) | AIMA Ch. 3, pp. 92-109 | None |
| 4 | 4 | Hill climbing, then CSPs | AIMA Ch. 4, pp. 120-129 | None |
| 5 | 5 | Supervised, unsupervised, RL overview, evaluation |  | Lab week 5 |
| 6 | 6 | Linear and logistic regression, perceptron, softmax |  | Lab week 6 |
| 7 | 7 | MLPs, back-propagation | AIMA s. 21.1 | Lab week 7, continued in Lab week 8 |
| 8 | 8 | Capacity, regularisation, residual connections |  | Lab week 8 is the XOR network, not this lecture's theory |
| 9 | 9 | Decision tree learning (ID3) |  | Lab week 9 |
| 10 | 10 | Probability and Bayes nets |  | None |
| 11 | 11 | MDPs and Q-learning |  | None |

Assessment context from the week 1 slides: Assignment 1 and Assignment 2 are 30% each. The final exam is 40%, closed book, and you need at least 40/100 on the exam to pass the course. Exam window on the slides: 15-24 October 2026. Late penalty is 5% per day, up to 7 days, unless an extension is granted.

## Search algorithms at a glance

`b` is the branching factor, `d` is the depth of the shallowest goal, `m` is the maximum path length, `C*` is the optimal path cost, and `epsilon` is the smallest step cost.

| Algorithm | Frontier | Complete? | Optimal? | Time | Space |
| --- | --- | --- | --- | --- | --- |
| BFS | FIFO queue | Yes, if `b` is finite | Yes, if every step cost is equal | `O(b^d)` | `O(b^d)` |
| UCS | Priority queue by `g` | Yes, if every step cost is at least `epsilon` | Yes | `O(b^(C*/epsilon))` | `O(b^(C*/epsilon))` |
| DFS | LIFO stack | No, in infinite spaces or with loops | No | `O(b^m)` | `O(bm)` |
| Depth-limited | Stack, depth cap `l` | No, if the shallowest goal is deeper than `l` | No | `O(b^l)` | `O(bl)` |
| Iterative deepening | Repeated depth-limited search, `l = 0, 1, 2, ...` | Yes, if `b` is finite | Yes, if step costs are equal | About `O(b^d)` | `O(bd)` |
| Greedy best-first | Priority queue by `h` | No in general. Yes in a finite space with repeated-state checking | No | `O(b^m)` | `O(b^m)` |
| A* | Priority queue by `f = g + h` | Yes, if `b` is finite and step cost is at least `epsilon` | Yes, with an admissible heuristic for tree search, and a consistent heuristic for graph search | Exponential | Exponential |

The slides call iterative deepening the best general uninformed choice: linear space, and not much more time than the others. Use BFS when solutions are short. Use DFS when solutions are dense. UCS is the only uninformed method that returns a lowest-cost path when step costs differ.

## Learning tasks at a glance

| Task | Labels? | Output | Examples from the slides and labs |
| --- | --- | --- | --- |
| Classification | Yes | Discrete class | Loan default, rain or no rain, digit recognition |
| Regression | Yes | Continuous number | House price, energy use in kWh |
| Clustering | No | Groups | Essay grouping, viewer segments |
| Association rules | No predefined class | Co-occurrence rules | `{onions, potatoes} => {burger}` |
| Semi-supervised | A few labels, many unlabelled | Usually a class | Pseudo-labelling, medical images |
| Reinforcement learning | No input-output pairs | A policy | Delayed reward, credit assignment |

---

## Lecture 1: Introduction and agents

Reading: AIMA Chapters 1-2. No lab solution in this folder.

### Need to know

The course splits AI into two strands. Traditional AI is top-down: representation, reasoning, and search. Machine learning is bottom-up: learn from examples. You are expected to know how a method works and why it is used.

The four dimensions of AI come from crossing two axes:

|  | Human | Rational |
| --- | --- | --- |
| Thinking | Match human thought, including errors and biases. Cognitive science is top-down (models plus psychology). Neuroscience is bottom-up (the physical brain). | Laws of thought: valid reasoning, from Aristotle's syllogisms to first-order logic. |
| Acting | Act so as to pass as human. | Do the right thing: the best expected outcome given the information available. |

Acting humanly is the Turing Test (1950), also called the Imitation Game. The question is whether a computer can pass as human. The slides list four prerequisites: natural language processing, knowledge representation, automated reasoning, and machine learning. A chatbot that deceives a judge can still lack those capabilities.

Milestones named on the slides:

- 1956: the term Artificial Intelligence is adopted at the Dartmouth meeting.
- 1997: Deep Blue beats Kasparov. Presented as a win for search.
- 2016: AlphaGo beats Lee Sedol. Presented as deep reinforcement learning. The Go state space is given as about `10^170`.
- 2021-2026 on the slides: generative models, then reasoning models, then agentic systems that decompose long tasks, use tools, and refine their own work.

Symbolic AI (GOFAI) uses explicit symbols, rules, ontologies, and search.

- Advantage: the derivation is explainable, and it does not need a training set.
- Limit: brittle under noise, and rules are hard to acquire at scale.

Subsymbolic AI (deep learning) learns weights from raw data.

- Advantage: handles vision, language, and other unstructured inputs, and scales with compute.
- Limit: opaque, and it needs large labelled sets and large compute.

An agent is architecture plus program. The architecture is the hardware. The program implements the agent function: the mapping from what the agent perceives to what it does. A state is a complete configuration of the agent and the environment. The state representation decides what the program can track, and therefore bounds what the system can do.

Sensors and actuators:

- Human: eyes, ears, touch, smell; hands, legs, voice.
- Robot: cameras, LiDAR, thermometers, infrared; motors, hydraulics, speakers.

PEAS is Performance, Environment, Actuators, Sensors.

- Automated taxi. Performance: safety, destination, laws, comfort, profit. Environment: roads, pedestrians, weather. Actuators: steering, throttle, brakes, horn, display. Sensors: cameras, radar, GPS, engine sensors, compass.
- Shopping agent. Performance: price, quality, recommendations, speed. Environment: the web, shops, shipping APIs. Actuators: form fills, redirects, checkout. Sensors: HTML, scripts, JSON, page layout.

### Check yourself

- Place cognitive science, neuroscience, the Turing Test, and laws of thought on the four-dimension grid.
- Write PEAS for a new agent without looking at the taxi example.
- State one advantage and one limit of symbolic AI, and the same for deep learning.

---

## Lecture 2: Uninformed search

Reading: AIMA Chapter 3, pages 64-91. No lab solution in this folder. Assignment 1's maze task is this material in code.

### Need to know

Solving a search problem has three steps: formulate it, search for a sequence of actions, then execute that sequence. In this course, finding one solution is enough when a solution exists.

A search problem is the 5-tuple `<S0, A, T, G, C>`:

- `S0`: initial state. If it is given, the relevant state space is the states reachable from it.
- `A(s)`: actions legal in state `s`.
- `T(s, a) = s'`: transition model, also called the successor or result function.
- `G`: goal test. There may be more than one goal state.
- `C(s, a, s')`: step cost. Path cost is the sum of step costs.

A solution is a sequence of actions from the initial state to a goal. An optimal solution has the lowest path cost among solutions.

A node is not a state. A node stores the state, the parent node, the action that produced it, and the path cost from the start. That is how the solution path is recovered.

Worked formulations you should be able to reproduce:

- Romania: start in Arad, goal is Bucharest, actions are drives to a neighbour, cost is distance in km. One solution is Arad, Sibiu, Fagaras, Bucharest.
- Vacuum world: eight states, actions Left, Right, Suck, cost 1 per action, goal is no dirt (states 7 and 8 on the slide).
- Pac-Man: one agent, with an initial state, legal actions, a successor function, a goal test, and a path cost.

The state space graph can be too large to draw. The search tree is the structure the algorithm builds. The tree can still grow exponentially.

General tree search:

1. Frontier starts as the initial state.
2. If the frontier is empty, there is no solution.
3. Remove a node. If it is a goal, return the path.
4. Expand it and add the children to the frontier.

The strategy is only the order in which nodes are removed. Graph search adds an explored set and does not re-add a state that is already in the frontier or the explored set. Two warnings from the slides: the check is on the state, not the node, and discarding a later path to a repeated state can discard a cheaper path. Uniform-cost search needs an extra test so that a better path replaces a worse one still on the frontier.

Properties to define precisely:

- Complete: a solution is found whenever one exists.
- Optimal: a lowest-cost solution is found.
- Time and space are counted in generated nodes, using `b`, `d`, and `m`.

BFS expands the shallowest node (FIFO). It is complete if `b` and `d` are finite. It is optimal when every action has the same cost, because the shallowest goal is then a cheapest goal. Time is `1 + b + b^2 + ... + b^d = (b^(d+1) - 1) / (b - 1) = O(b^d)`. Space is `O(b^d)` because the explored set and the frontier are both stored. Space is the practical problem, not time. BFS minimises the number of steps. It does not minimise path cost when step costs differ.

UCS expands the lowest path cost `g` (priority queue). It matches BFS when all step costs are equal. The goal test is applied when a node is selected for expansion, not when it is first generated. It is complete if every step costs at least `epsilon > 0`, and it is optimal. Time and space are `O(b^(C*/epsilon))`.

DFS expands the deepest node (stack). It is not complete in infinite-depth spaces or spaces with loops. Avoiding repeated states along the current path makes it complete in finite spaces. Time is `O(b^m)`, which is worse than BFS when `m` is much larger than `d`, and can be better when solutions are dense. Space is `O(bm)`, linear in the depth. It is not optimal.

Depth-limited search is DFS that generates no children at depth `l`. It fails when the shallowest solution is deeper than `l`. Iterative deepening runs depth-limited search for `l = 0, 1, 2, ...` until a solution appears. It uses linear space and only a small extra time factor, because most nodes sit at the deepest level and are generated only once at the final limit.

### Check yourself

- List the five components for the vacuum world and for the Romania problem.
- Say which field of a node is used to rebuild the action sequence.
- Explain why BFS can return a path that is not the cheapest path.
- State why UCS tests the goal on expansion, not on generation.

---

## Lecture 3: Informed search

Reading: AIMA Chapter 3, pages 92-109. No lab solution in this folder.

### Need to know

A heuristic is extra problem knowledge: an estimate of the cost from a state to a goal. `g(n)` is the cost already paid to reach `n`. `h(n)` estimates the cost still to pay. `f(n)` estimates the total cost of a path through `n`.

Best-first search is uniform-cost search with `f` in place of `g`. The frontier is a priority queue in increasing `f`.

Greedy best-first search uses `f(n) = h(n)`. It expands the node that looks closest to the goal. Straight-line distance to Bucharest is the running example. It is not complete if loops are allowed, and it is complete in a finite space when repeated states are checked. Time and space are `O(b^m)`. It is not optimal. The slides give Arad-Sibiu-Fagaras-Bucharest at 450 km against the shorter Arad-Sibiu-Rimnicu Vilcea-Pitesti-Bucharest at 418 km.

A* uses `f(n) = g(n) + h(n)`. It avoids expanding paths that are already expensive.

A heuristic is admissible when `h(n) <= h*(n)` for every node, where `h*(n)` is the true cost to a goal. It never overestimates. It is optimistic. Straight-line distance is admissible because a road cannot be shorter than the straight line. If `h` is admissible, A* tree search (no repeated-state checking) is optimal. Admissibility alone does not guarantee optimality once repeated states are checked.

A heuristic is consistent (monotonic) when, for every successor `n'` of `n`,

`h(n) <= cost(n, n') + h(n')`.

Then `f(n') >= f(n)` along any path, so `f` never decreases. Consistency is stronger than admissibility: every consistent heuristic is admissible. If `h` is consistent, A* graph search is optimal, and nodes are expanded in order of increasing `f` (the `f`-contours). Timisoara is the slide example of a node that is pruned.

A* is complete when `b` is finite and every step costs at least `epsilon`. Time and space are exponential because every generated node is kept. It is optimal with an admissible heuristic for tree search and a consistent heuristic for graph search.

The 8-puzzle heuristics, both admissible, come from relaxed problems:

- `h1`: number of misplaced tiles. At the start state on the slide, `h1 = 8`. This is optimal if a tile may move to any square.
- `h2`: sum of Manhattan distances. At that start state, `h2 = 3+1+2+2+2+3+3+2 = 18`. This is optimal if a tile may move to any adjacent square, even through other tiles.

If `h2(n) >= h1(n)` for every `n` and both are admissible, `h2` dominates `h1` and is the better search heuristic, because it is closer to the true cost without going over it. Node counts on the slides:

| Solution depth | IDS | A* with h1 | A* with h2 |
| --- | --- | --- | --- |
| 12 | 3,644,035 | 227 | 73 |
| 24 | about 54,000,000,000 | 39,135 | 1,641 |

The 8-puzzle action on the slide is: a tile can move from A to B if A is adjacent to B and B is blank. Dropping either condition, or both, produces a relaxed problem whose optimal cost is an admissible heuristic. The optimal cost of a relaxed problem is never greater than the optimal cost of the real problem.

Memory-bounded variants, named only: iterative deepening A* (IDA*) cuts off on `f` rather than depth; recursive best-first search (RBFS); simplified memory-bounded A* (SMA*). RBFS and SMA* stay optimal with limited memory and can solve problems on which A* runs out of memory. Detail is left to AIMA section 3.5.3.

### Check yourself

- Compute `f` for a node when you are given `g` and `h`.
- Explain why an overestimate can make A* return a suboptimal path.
- Say which heuristic, admissible or consistent, is required for tree search and which for graph search.
- Derive `h1` and `h2` from the two relaxations of the 8-puzzle rule.

---

## Lecture 4: Local search and CSPs

Reading: AIMA Chapter 4, pages 120-129. No lab solution in this folder. Assignment 1's crossword task is a CSP.

### Part 1: Local search and hill climbing

### Need to know

Earlier search cared about the path. Local search cares only about the final configuration. The path is irrelevant.

Given configurations `S` and an evaluation `Eval(X)`, find a global extremum. For 8-queens, `Eval` is the number of attacking pairs, and the global solution is `h = 0`. For VLSI layout, `Eval` combines component distance, unused area, and routing length.

The configuration space is too large to list, `Eval` may be expensive, and there is no efficient exact algorithm. A neighbourhood `Neighbours(X)` is the set of configurations one move away. Defining that neighbourhood well is the main design choice. The algorithm starts at `X0` and repeatedly evaluates some neighbours, picks one, and moves, until a stopping condition holds.

A global optimum is best over all of `S`. A local optimum is best only inside its neighbourhood. Each iteration can only test local optimality.

Hill climbing is greedy local search:

```text
current = initial state
repeat:
    neighbour = best-valued neighbour of current
    if neighbour is not better than current:
        return current
    current = neighbour
```

Failure modes:

- Local maximum or minimum: every neighbour is worse, but a better configuration exists elsewhere.
- Plateau: a flat region. A shoulder is a plateau with an exit.
- Ridge: the goal is not reachable by uphill moves in the chosen neighbourhood.

8-queens numbers to remember. The state space is `8^8`, about 17 million states.

- Steepest-ascent hill climbing, from a random start, succeeds on 14% of instances and gets stuck on 86%. Success takes about 4 steps. Failure takes about 3.
- Allowing sideways moves, with a cap of 100 consecutive sideways moves, raises success from 14% to 94%. Success then takes about 21 steps, and failure about 64. The slide mentions 8 shoulder states with `Eval = 12`.

Random-restart hill climbing runs independent climbs from random starts until a goal appears. If the success probability is `p`, the expected number of restarts is `1/p`.

- Without sideways moves, `p = 0.14`, so about 7 restarts (1 success and 6 failures). Expected steps: `1*4 + (1/0.14 - 1)*3`, about 22.
- With the sideways cap, `p = 0.94`, expected restarts about 1.06, expected steps about `1*21 + (1/0.94 - 1)*64`, about 25.

Stochastic hill climbing picks one neighbour at random (the slide says 1 of 56 in the 8-queens neighbourhood) rather than the best neighbour. Simulated annealing is named as a variant and is explicitly not taught in detail. The summary says these methods are black boxes: what matters is the state representation, the neighbourhood, the evaluation function, and any extra heuristics. Prefer a direct method when one exists.

TSP: 2-opt and 3-opt moves rearrange the tour. 3-opt is better than 2-opt. 4-opt is not worth the extra time. Random restart raises the chance of a good tour. Quality is reported as percent above an estimated minimum cost.

### Part 2: Constraint satisfaction

### Need to know

In ordinary search the state is a black box. In a CSP the state is an assignment of values to variables `Xi`, each with domain `Di`, and the goal test is a set of constraints on allowable combinations. That structure allows general algorithms that beat black-box search.

Map colouring: variables are WA, NT, Q, NSW, V, SA, T. Domain is `{red, green, blue}`. Adjacent regions differ. One solution on the slide: WA red, NT green, Q red, NSW green, V red, SA blue, T green. A solution is a complete and consistent assignment.

A binary CSP has only constraints on pairs of variables. The constraint graph has a node per variable and an arc per constraint.

Varieties:

- Finite discrete domains: `n` variables of size `d` give `O(d^n)` complete assignments. Boolean satisfiability is the NP-complete case.
- Infinite discrete domains, such as job start days, need a constraint language, for example `StartJob1 + 5 <= StartJob3`.
- Continuous variables with linear constraints can be solved by linear programming.

Constraint order: unary (`SA != green`), binary (`SA != WA`), higher-order (a cryptarithmetic column). Cryptarithmetic variables on the slide include `F, T, U, W, R, O` and carry variables `X1, X2, X3`, domain digits, with `Alldiff`, column equations, `X3 = F`, and `F` and `T` nonzero. Real uses: assignment, timetabling, transport, factory scheduling.

Incremental formulation: start from the empty assignment, assign a value that does not conflict, and stop when every variable is assigned. Every solution sits at depth `n`, so depth-first search fits. The path does not matter. Naive branching is `b = (n - l)*d` at depth `l`, which produces `n! * d^n` leaves.

Assignments are commutative: WA red then NT green is the same state as the reverse order. Backtracking therefore assigns one variable per node, so `b = d`, and there are `d^n` complete assignments rather than `n! * d^n` leaves. Backtracking is the basic uninformed CSP algorithm. It can solve n-queens up to about `n = 25`.

```text
function Backtrack(assignment, csp):
    if assignment is complete: return assignment
    var = Select-Unassigned-Var(assignment, csp)
    for value in Domain-Values(var, assignment, csp):
        if value is consistent with assignment:
            add {var = value}
            inferences = Inference(assignment, csp)
            if inferences != failure:
                add inferences
                result = Backtrack(assignment, csp)
                if result != failure: return result
            remove {var = value} and the inferences
    return failure
```

Ordering heuristics:

- MRV (minimum remaining values): pick the variable with the fewest legal values left.
- Degree heuristic: MRV tie-break. Pick the variable involved in the most constraints with unassigned variables.
- LCV (least constraining value): try the value that rules out the fewest values in the remaining variables.
- Together, these make 1000-queens feasible on the slides.

Forward checking tracks the remaining legal values of unassigned variables and fails as soon as any variable has none.

Constraint propagation goes further. Forward checking can miss a failure such as NT and SA both having only blue left. Arc consistency: arc `X -> Y` is consistent if every value of `X` has some allowed value of `Y`. If `X` loses a value, neighbours of `X` are rechecked. Arc consistency detects failure earlier than forward checking. It can run before search or after each assignment. AC-3 puts every arc on a queue, revises the tail, and if the domain becomes empty returns failure; otherwise it requeues arcs into the revised variable.

Local search on CSPs uses complete assignments that may violate constraints. A move reassigns a variable. Min-conflicts picks a conflicted variable at random and chooses the value that violates the fewest constraints. The heuristic is `h(n)` = number of violated constraints. For 4-queens there are `4^4 = 256` states if each column holds one queen. The slides say min-conflicts solves n-queens in almost constant time for arbitrary `n` with high probability, including `n = 10,000,000`.

Structure: independent subproblems are rare and valuable. A tree-structured CSP is solvable in time linear in the number of variables. Two reductions to trees are named: assign a cutset so the remainder is a tree, or build a tree decomposition of connected subproblems. Decomposing into subproblems of size `c` changes `O(d^n)` into `O(d^c * n/c)`.

The closing summary says simulated annealing is not introduced in this course, even though the outline slide names it.

### Check yourself

- Contrast path cost in Lecture 2 with "only the final configuration matters" here.
- Reproduce the 14% and 94% 8-queens figures and what change produces the second figure.
- Define MRV, degree, and LCV, and say which one orders variables and which one orders values.
- State the arc-consistency test in one sentence.

---

## Lecture 5: Machine learning basics

No set textbook pages on the title slide. Lab week 5 is the matching workshop.

### Need to know

Machine learning, in the slide wording, is programming a computer to optimise a performance criterion using example data or past experience. Arthur Samuel coined the term in the early 1960s. Learn when human expertise does not exist, cannot be explained, changes over time, or must be adapted to a case. Do not learn payroll: the rule is already known.

Notation: `xi` is an input feature, `yi` is the target, `(xi, yi)` is a training example. The superscript is an index, not a power. The hypothesis `h: X -> Y` predicts `y` from `x`.

Supervised learning learns `h` from input-output pairs.

- Regression: `y` is continuous. House price, share price, age from a photo, daily energy in kWh.
- Classification: `y` is discrete. Binary classification uses labels such as 1 and 0. House versus apartment, voting age, loan approval, rain versus no rain.

The same raw data can be either task. Predicting a price is regression. Predicting "sells above the asking price" is classification.

k-nearest neighbour: given an input, take the most common class among the `k` nearest training points. `k = 1` is ordinary nearest neighbour and is sensitive to a single odd point. The rain example on the slides shows a white point labelled rain by 1-NN and differently by 5-NN. A linear classifier instead uses a straight boundary `ax + by + c = 0`.

Classification applications named: face recognition, character recognition, speech, medical diagnosis, biometrics, outlier and attack detection. MNIST has 60,000 training images and 10,000 test images. A 2016 figure on the slide is about 0.21% error from an ensemble of five CNNs.

Uses of a learned rule: predict future cases, extract knowledge, compress the data, and detect outliers such as fraud.

Unsupervised learning has inputs and no output labels. It learns what normally happens. Clustering groups similar instances. The cocktail-party example is given as non-clustering structure discovery. Association rule learning finds relations such as `{onions, potatoes} => {burger}`. The slides note that some sources class association rules as supervised. There is no teacher to correct the model.

Semi-supervised learning mixes a small labelled set with a large unlabelled set. Pseudo-labelling: train on the labelled data, predict the unlabelled data, keep high-confidence predictions, retrain, and repeat. Uses: medical images, speech transcription, web pages.

Reinforcement learning learns a sequence of actions that maximises future reward. There is no supervised target, and the reward is often delayed. The credit-assignment problem is deciding which earlier action caused the later reward. The loop is state, action, reward, and a policy `pi` from states to actions. Algorithms named here, before the week 11 lecture: temporal difference, Q-learning, and deep adversarial networks. RLHF uses a reward model built from human preferences, with PPO and GRPO named as policy optimisers.

Evaluation:

- Learning searches a hypothesis space.
- A test set must be distinct from the training set.
- A hypothesis generalises when it predicts `y` on the test set.
- A consistent hypothesis agrees with every training pair. Two consistent hypotheses can exist. Ockham's razor prefers the one with fewer assumptions.
- There is a tradeoff: a complex hypothesis can be consistent and still generalise worse than a simpler hypothesis that misses some training points.
- If the model has as many degrees of freedom as the data, it can fit perfectly and still fail on new data. That is overfitting: the fit is too close to one data set.
- Dietterich's triple tradeoff: complexity of the hypothesis space `c(H)`, training set size `N`, and generalisation error `E`. As `N` grows, `E` falls. As `c(H)` grows, `E` first falls and then rises.
- Split: training 60-80%, validation 10-20%, test 10-20%. Resample when data are scarce.
- High bias: inaccurate on average, but stable. High variance: accurate on average, but unstable across samples.
- Loss functions: 0-1 loss is 0 if the prediction matches and 1 otherwise. L1 loss is the absolute error. L2 loss is the squared error.

### Lab week 5

Five scenarios to classify before you touch a model:

1. Loan default from income, credit, employment, and amount, with known outcomes: supervised classification.
2. Viewer segments from behaviour, with no labels: unsupervised clustering.
3. CPU and memory allocation scored by response time and energy: reinforcement learning.
4. A few clinician-labelled records plus many unlabelled records: semi-supervised learning.
5. Energy in kWh from temperature, occupancy, time, and day: supervised regression.

For the energy model, each row is one observation. Features are outdoor temperature, occupants, time of day, and day of week. The target is continuous kWh, so this is regression. Time and day are periodic and would normally be encoded as categories or cyclical features, not as plain integers.

The fitted line in the solution is `energy = 302.26 - 6.19 * temperature`. At 15 degrees C the prediction is `302.26 - 6.19*15 = 209.41` kWh. The negative coefficient means a heating-dominated building: warmer days use less energy. Check points on the solution: 10 degrees C gives 240.4 kWh, 20 gives 178.5, 30 gives 116.7. Equal temperature steps give equal energy steps. That is what a linear model does.

`R^2 = 0.948` means 94.8% of the variation in the training data is explained. It says nothing about new days. A U-shaped truth (heating when cold, cooling when hot, low use when mild) is not a straight line. A linear fit then underestimates both extremes and overestimates mild days.

Generalisation means the same relationship holds on a future day. Overfitting means the model has memorised a cold winter or a construction period in the training window.

### Check yourself

- Turn one regression problem into a classification problem by changing only the target.
- State what `k` changes in k-NN.
- Define consistent hypothesis, Ockham's razor, and overfitting in one sentence each.
- Compute `302.26 - 6.19 * T` for a new temperature and say what `R^2` does not tell you.

---

## Lecture 6: Linear models

Lab week 6 is the matching workshop.

### Need to know

A linear equation such as `2x + 3y - 12 = 0` cuts the plane into two half-planes. With several inputs, linear regression is

`y = w1*x1 + w2*x2 + ... + wn*xn + b = <w, x> + b`.

House-price features on the slide are beds, baths, garage, and land area. Absorb the bias by appending a constant 1 to `x` and appending `b` to `w`, giving `y = x w` as a matrix product.

L2 loss on one example is `(y - y_hat)^2`. It penalises large mistakes and is sensitive to outliers. Mean squared error on `n` examples is

`l = (1/n) * sum (yi - <xi, w> - b)^2`.

Training chooses `w*, b* = argmin l`. The gradient of `f` is the vector of partial derivatives. It points in the direction of steepest increase. For linear regression the loss is convex. With the bias folded into `w`, the closed form is

`w* = (X^T X)^(-1) X^T y`.

That inverse is impractical for large `X`, and other models have no closed form, so training uses gradient descent:

`w_t = w_(t-1) - eta * (partial l / partial w)`.

`eta` is the learning rate. Too small: slow progress. Too large: divergence or oscillation. Full gradient descent uses every training example. Stochastic gradient descent uses a mini-batch of `b` random examples. Too small a batch: noisy gradients and poor hardware use. Too large: memory cost, and wasted work if the batch repeats the same point. Common batch sizes on the slide: 32 to 512.

Linear classification uses a decision boundary. For the seismic data the equation line is `1.7*x1 - x2 - 4.7 = 0`, while the weight vector on the same slide is written `(-4.9, 1.7, 1)`. Treat the figure as the source if a question gives the picture. Predict class 1 when `w . x >= 0`, else 0. That is a hard threshold. Equivalently, `h_w(x) = Threshold(w . x)`.

The perceptron (Rosenblatt, 1957) is a linear function plus a hard threshold. With labels in `{+1, -1}`:

`y* = w0*x0 + w1*x1 + ...` with `x0 = 1`, and `S(y) = +1` if `y >= 0`, else `-1`.

The step function has gradient 0 everywhere except at 0, where it is undefined, so ordinary gradient descent is not used. The learning rule, applied to example `(x, y)`, is

`wi <- wi + alpha * (y - h_w(x)) * xi`.

Correct predictions leave the weights unchanged. The lecture also writes the `+1/-1` case as `w' = w + y * f`, where `y` is the true class: add `f` if a positive example was called negative, and subtract `f` if a negative example was called positive. Start from weights 0 and repeat over the training set.

Perceptron convergence theorem: if the training set is linearly separable, the algorithm reaches a linear separator in a finite number of updates. It does not say the separator is unique, or that one pass is enough. If the data are not linearly separable, the weights need not converge.

Logistic regression wants an output in `(0, 1)`. It is a linear score passed through the sigmoid (logistic) function. Classify 1 if the output is at least 0.5, else 0. The loss is binary cross-entropy. Learning is gradient descent. The decision boundary is still linear. The gain over the perceptron is a probability and a usable gradient.

Softmax regression is the multi-class extension: one score per class, softmax turns scores into probabilities, and the loss is cross-entropy. The predicted class is `argmax` of the scores. Examples: MNIST (10 classes), ImageNet (1000), a Kaggle protein task (28), a Kaggle malware task (9). Squared error is the regression loss. Classification wants a confident margin on the correct class, not a single unbounded number.

The slide summary also names Huber regression as a linear model plus an activation, without further detail.

### Lab week 6

Keep three models distinct:

|  | Linear regression | Logistic regression | Perceptron |
| --- | --- | --- | --- |
| Output | Any real number | Probability in `(0, 1)` | Hard `+1/-1` or `1/0` |
| Boundary | Not a classifier | Linear | Linear |
| Training | MSE, closed form or gradient descent | Cross-entropy, gradient descent | Update only on mistakes |
| Failure | Poor for class probabilities | Still linear | No convergence if not linearly separable |

XOR is the standard non-separable case (Minsky and Papert, 1969). A single perceptron cannot represent it.

Lab trace, labels in `{0, 1}`, learning rate 0.5, bias stored as `w3` with `x3 = 1`. Initial weights for the learning trace are `[0, 0, -1]`.

- Point `[1, 1, 1]`, `y = 0`: score `-1`, predict 0, no update.
- Point `[3, 2, 1]`, `y = 1`: score `-1`, predict 0, wrong. Update by `0.5 * (1 - 0) * x`, weights become `[1.5, 1, -0.5]`.
- Points `[2, 4, 1]` and `[3, 4, 1]`, both `y = 1`: scores 6.5 and 8, both correct, no update.
- Point `[2, 3, 1]`, `y = 0`: score 5.5, predict 1, wrong. Update by `0.5 * (0 - 1) * x`, weights become `[0.5, -0.5, -1]`.

One pass is not enough. The earlier fixed-weight check with `[0.5, -0.5, -1]` gets 2 of 5 points right (points 2, 3, and 4 wrong). Further epochs are required. The theorem promises a finite number of updates, not a single epoch, and not an optimal separator among the many that may exist.

### Check yourself

- Write MSE and the gradient-descent update, and say what `eta` and batch size do when set too high.
- Apply the perceptron update for one misclassified point in both the `+1/-1` form and the lab's `0/1` form.
- State the convergence theorem, including what it does not promise.
- Say what the sigmoid changes relative to a threshold.

---

## Lecture 7: Feed-forward neural networks

Reading: AIMA section 21.1. Lab week 7 is the hand calculation. Lab week 8 implements XOR.

### Need to know

A single perceptron outputs `o = sigma(<w, x> + b)` with `sigma(x) = 1` if `x > 0` and `0` otherwise. It does binary classification, not a real-valued regression output and not a probability. The update `wi <- wi + alpha * (y - h_w(x)) * xi` matches SGD with batch size 1 on that particular loss. XOR is not linearly separable, so one perceptron cannot learn it: `(0,0)->0`, `(1,0)->1`, `(0,1)->1`, `(1,1)->0`.

A multi-layer perceptron adds hidden layers and a non-linear activation. Without the non-linearity, stacked linear maps collapse to one linear map. All neurons in the feed-forward nets in this lecture are fully connected. Hyperparameters: number of hidden layers, and the width of each layer.

Forward pass for one hidden layer, as written on the architecture slide (`x` is the input, `W1` connects inputs to hidden units, `W2` connects hidden units to outputs):

`h = sigma(W1 x + b1)`

`o = W2 h + b2`

The slide's first formula line writes `W2 x` for the output. The surrounding text says the second matrix maps the hidden layer, so the intended product is with `h`. For multiclass outputs, `y = softmax(o)`. The output layer sometimes has no activation.

Back-propagation minimises the error between the network output and the target. It is gradient descent plus the chain rule. Steps:

1. Initialise weights to random numbers in `[-1, 1]`.
2. Forward pass: compute every hidden and output activation.
3. Backward pass: compute an error term at the outputs and send it back to update weights and biases.
4. Stop on an iteration limit or on an error threshold, and test on held-out data during training.

One hidden or output unit: weighted sum of inputs from the previous layer, plus bias, then a non-linear activation.

For a sigmoid unit, the update is `wij = wij + eta * delta_j * yi`, with `0 < eta < 1`.

- If `j` is an output unit: `delta_j = yj * (1 - yj) * (zj - yj)`, where `yj` is the sigmoid output and `zj` is the target.
- If `j` is hidden: `delta_j = yj * (1 - yj) * sum_k (delta_k * w_jk)`, using the error terms and weights of the units that `j` feeds. The slides say to use the updated outgoing weights in that sum, and to store deltas before changing weights, because deltas depend on the previous weights. Store neuron outputs as well.

`yj * (1 - yj)` is the sigmoid derivative. It is largest at `yj = 0.5`, where it equals `0.25`, and near 0 when `yj` is near 0 or 1.

Squared error for a net with no hidden layer is `L2(w) = [(y1 - y_hat1)^2 + (y2 - y_hat2)^2] / 2`. The factor `1/2` makes the derivative `(prediction - target)` rather than twice that. With hidden layers, use the chain rule: `d/dx f(g(x)) = f'(g(x)) * g'(x)`.

Worked sigmoid numbers on the slide, for the unit calculations rather than the messy bias side notes:

- Unit 4 weighted sum `-0.3`, output `1 / (1 + exp(0.3)) = 0.574`.
- Unit 5 weighted sum `-0.1`, output `1 / (1 + exp(0.1)) = 0.525`.
- Unit 6 weighted sum `0.11`, output `1 / (1 + exp(-0.11)) = 0.527`.

Learning-rate selection: try values spaced exponentially. Find one `eta` that is too small (smooth, very slow) and one that is too large (oscillation or divergence), then search between them. A schedule that shrinks `eta` is mentioned as an advanced option.

Stopping: a fixed number of iterations, or RMS error

`RMS = sqrt( sum_i sum_j (dij - oij)^2 / (p * m) )`,

where `m` is the number of outputs, `p` is the number of training pairs, `dij` is the desired output, and `oij` is the network output. Confirm the exact placement of `p*m` against the figure if a question quotes the formula; the slide text defines the symbols but the formula image is incomplete in the extract.

Momentum (Rumelhart et al., 1986):

`wij(t+1) = wij(t) + eta * delta_j * xi + eta * (wij(t) - wij(t-1))`.

The extra term speeds convergence and stabilises training. Another named variant adds a hidden unit when the net is stuck in a local minimum (Hirose, Yamashita, and Hijiya), demonstrated on XOR and on 8x8 character fonts.

The voice example is a fully connected net with 60 inputs, 6 hidden units, and 2 outputs (one-hot for "Steve" versus "David"). Training presents each pair, computes error, back-propagates, and adjusts weights, repeated over many sweeps. Applications listed: character and face recognition, sonar mine versus rock, car navigation, stock prediction, NETtalk pronunciation.

### Lab week 7

One forward and backward step with ReLU hidden units. Input `(x1, x2) = (0.5, -0.5)`. Target `y = 1`.

- `z1 = 1.0*0.5 + 0.5*(-0.5) + 0.5 = 0.75`. `a1 = ReLU(0.75) = 0.75`.
- `z2 = -1.0*0.5 + 2.0*(-0.5) + (-0.5) = -2`. `a2 = ReLU(-2) = 0`.
- `z = 1.5*0.75 + (-1.0)*0 + 0.5 = 1.625`. Linear output, so `o = 1.625`.
- Half squared loss: `L = 0.5 * (1.625 - 1)^2 = 0.5 * 0.390625 = 0.1953125`.
- With `eta = 0.1` and a given gradient `0.46875`: `W_out` goes from `1.5` to `1.453125`, and `W11` goes from `1.0` to `0.953125`. A positive gradient means the loss rises if the weight rises, so the update subtracts.

Dying ReLU: the derivative of `ReLU(z)` is 0 for `z <= 0`. Hidden unit 2 contributes nothing on the forward pass and receives a zero gradient, so its weights do not change on this step. If that happens for every training example, the unit stays dead. Leaky ReLU and ELU keep a small gradient for negative inputs.

### Lab week 8

This lab implements XOR. It belongs with Lecture 7. Lecture 8's theory (dropout, weight decay, early stopping) is not what the lab codes.

Architecture: inputs 2, hidden 4, output 1. Data `X = [[0,0],[0,1],[1,0],[1,1]]`, targets `[[0],[1],[1],[0]]`.

Shapes: `W1` is `(2, 4)`, `b1` is `(1, 4)`, `W2` is `(4, 1)`, `b2` is `(1, 1)`. Forward shapes: `X` is `(4, 2)`, `Z1 = X @ W1 + b1` is `(4, 4)`, `Z2` is `(4, 1)`. If `W1` were `(4, 2)`, the product would be illegal.

Initialise weights with uniform random values in `[-1, 1]`. If every weight starts equal, every hidden unit gets the same gradient and learns the same feature. That is the symmetry problem. Biases may start at 0 because each unit has its own bias.

`sigmoid(x) = 1 / (1 + exp(-x))`. `sigmoid(0) = 0.5`, `sigmoid(10)` is about `0.99995`, `sigmoid(-10)` is about `0.000045`. The derivative is `s * (1 - s)` and is computed from the stored output, so the pre-activation need not be kept. Maximum derivative is `0.25`. Each sigmoid layer therefore shrinks the gradient by at least 4. In a deep stack this is the vanishing gradient problem.

Loss: `mean(0.5 * (A2 - y)^2)`. The `1/2` cancels the 2 from differentiation, leaving gradient `(A2 - y)`. Binary cross-entropy is the more standard classification loss. MSE is used here because the lab treats the output as a continuous target.

Autograd's `grad(compute_loss)` returns a function that yields `[dW1, db1, dW2, db2]` with the same shapes as the parameters. `compute_loss` must be pure: no in-place updates inside it. The training loop then does `param -= learning_rate * grad`.

With 4 hidden sigmoid units the net learns XOR. A threshold of 0.5 on the final predictions gives the four correct labels (about 0.03, 0.97, 0.97, 0.03). A healthy curve falls quickly, then flattens, and stays smooth at learning rate 0.5. A flat curve suggests a tiny learning rate, a bad initialisation, or a gradient bug. Oscillation or a rising loss suggests `eta` is too large. A plateau well above zero suggests a local minimum or too little capacity. `NaN` suggests overflow, often from a huge learning rate or a missing factor in the loss.

Parameter count for this net: `2*4 + 4 + 4*1 + 1 = 17`. The lab notes that a larger net such as `784*30 + 30 + 30*10 + 10 = 23860` parameters cannot be differentiated by hand.

### Check yourself

- Explain why hidden layers need a non-linear activation.
- Compute a sigmoid output and its derivative factor `y(1-y)` for one unit.
- State the dying-ReLU condition and the symmetry problem in initialisation.
- Give the matrix shapes for a 2-4-1 XOR net.

---

## Lecture 8: Model selection and regularisation

Lab week 8 does not cover this lecture. Use the lecture slides themselves. The lab that week trains the XOR network from Lecture 7.

### Need to know

The loan example: 100 applicants, 5 defaults, and all 5 wore blue shirts. A model can lock onto that accident. Training error will look excellent and the rule will fail on new applicants.

Four errors:

- Training error: error on the data used to fit the model.
- Validation error: error on data used to choose hyperparameters. A common recipe is to hold out about 10% of the training pool and never fit on it.
- Generalisation error: error on new data.
- Test error: error on a set that is used once. Examples: a future exam, a house price you have not seen, a Kaggle private leaderboard.

Do not tune on the test set. Do not mix the validation rows back into training. The week 5 split was training 60-80%, validation 10-20%, test 10-20%.

K-fold cross-validation, used when data are scarce: split the training pool into `K` parts. For each part, train on the other `K-1` and validate on the held-out part. Report the average of the `K` validation errors. Typical `K` is 5 or 10.

Underfitting: training error is high, so test error is high too. The model is too simple for the data. Overfitting: training error is low and test error is high. The model is too complex and has fit noise. Capacity is the range of functions the model can fit. Low capacity underfits. High capacity can memorise.

Within one algorithm family, capacity depends on the number of parameters and on the values those parameters can take. Comparing a tree with a neural net by parameter count alone is not reliable. A linear model in `d` inputs has `d + 1` parameters if the bias is counted. The slide writes `(d+1)*m + (m+1)*k` for a one-hidden-layer net with `m` hidden units and `k` outputs.

VC dimension, for a classifier, is the size of the largest set of points that the model family can shatter: for every possible labelling of those points, some model in the family classifies them perfectly. A 2-D perceptron has VC dimension 3. It can realise any labelling of 3 points and cannot realise XOR on 4 points. A perceptron with `N` parameters has VC dimension `N`. Some multilayer perceptrons have VC dimension `O(N log2 N)`. The gap between training error and generalisation error can be bounded with VC dimension. The slides say the bounds are too loose for deep learning and that VC dimension is rarely computed in practice.

Data complexity depends on the number of examples, the number of elements in each example, time and space structure, and diversity.

Regularisation constrains effective complexity so the model overfits less. Four techniques:

- Early stopping. After each epoch, or every few epochs, measure validation loss. Both losses fall while the model learns real structure. Later, training loss keeps falling and validation loss flattens and then rises. Keep the weights from the best validation epoch. Patience is a run of epochs with no improvement, for example 10, after which you restore the saved weights.
- Data augmentation. Expand the training set with realistic modifications. Images: rotate, crop, flip, zoom, brightness, contrast, colour, noise, cutout. Text: synonym swap, back-translation, random deletion or swap. Audio: pitch shift, background noise, time stretch.
- Weight decay. Hard form: minimise the loss subject to `||w||^2 <= theta`. A smaller `theta` is stronger regularisation. The bias is often left unregularised; the slide says the practical difference is small. Soft form: add `(lambda/2) * ||w||^2` to the loss. `lambda = 0` removes the penalty. As `lambda` goes to infinity, the optimal weights go to 0. The gradient of the penalty is `lambda * w`, so the update is `w <- (1 - eta*lambda) * w - eta * (gradient of the data loss)`, assuming `eta*lambda < 1`. The factor `(1 - eta*lambda)` is why it is called weight decay. Benefit claimed on the summary slide: the model does not rely on one feature alone.
- Dropout. During training, randomly turn units off. Typical rates: 0.2 to 0.5 on hidden layers, 0.1 on the input layer. The motivation is robustness: a good model should tolerate modest input changes, and dropout injects noise inside the network so features cannot depend on one co-adapted unit.

Residual connections are not regularisation. In a plain feed-forward net, each layer's output is the next layer's input. A residual block sends `x` forward unchanged and adds a residual function: output `F(x) + x`, often followed by ReLU. This is useful because very deep nets are hard to optimise, and short paths from early layers to later layers make training easier. Sometimes the residual `H(x) - x` is easier to learn than `H(x)`. If the dimensions differ, use `F(x) + W x`. Several residual blocks can sit in one network. The benefit is optimisation, not a direct improvement in generalisation.

### Check yourself

- Separate training, validation, test, and generalisation error.
- Describe one epoch of early stopping and what "patience" means.
- Write the weight-decay update and the role of `lambda`.
- Say why a residual connection is not listed as regularisation.

---

## Lecture 9: Decision trees

Lab week 9 is the matching workshop.

### Need to know

A decision tree implements a function from attribute values to one output by a sequence of tests. Each internal node tests one attribute. Each branch is one value of that attribute. Each leaf is an output. The same tree is a set of if-then rules. Binary (Boolean) classification labels examples positive or negative.

Given positive and negative examples, learn a tree that fits them and is as small as possible. The number of possible trees is too large for exhaustive search. The algorithm is a greedy divide-and-conquer: test the most important remaining attribute, split into smaller problems, and repeat. The result is a small consistent tree, not a guaranteed smallest tree.

ID3 (Ross Quinlan, University of Sydney, about 1986) builds the tree top down.

```text
If all remaining examples are positive, return Yes.
If all remaining examples are negative, return No.
If no examples remain, return the majority class of the parent.
If no attributes remain, but the examples are mixed, return their majority class.
Otherwise choose the best attribute, create a child per value, send the matching examples to each child, and recurse.
```

`PLURALITY-VALUE` is that majority vote, with random tie-breaking. `IMPORTANCE` selects the attribute.

A good attribute splits the examples into subsets that are as pure as possible. In the restaurant example, Patrons separates well and Type does not. After the first split, the next test is chosen inside each child. Attributes that are not needed, such as Raining and Reservation in the worked restaurant tree, never appear. At a mixed leaf in a large data set, predict the majority class. The slide's large-node example is about `-95, +800` on one branch and the reverse on the other.

Two selection methods are named. Method 1 is classification error. If the root predicts the majority class, error is the fraction of the minority. The credit example has error `18/22 = 0.45` before any split. Method 2, the one used by ID3 in the lab, is entropy and information gain.

Entropy of a variable with values `vi` and probabilities `P(vi)`:

`I = sum_i -P(vi) * log2(P(vi))`.

For `p` positive and `n` negative examples, use the two proportions `p/(p+n)` and `n/(p+n)`. A coin that always lands heads has entropy 0. A fair coin has entropy 1 bit. A coin that lands heads 99% of the time has entropy near 0. For a Boolean label, entropy is 0 when the set is pure and 1 when the set is an even split.

Information gain of attribute `A` with values that partition the set `E` into subsets `E1, ..., Ev`:

`IG(A) = I(E) - sum_i (|Ei| / |E|) * I(Ei)`.

Choose the attribute with the largest gain. In the restaurant set, `p = n = 6`, so `I = 1`, and Patrons has the highest gain, so Patrons is the root.

Accuracy rises as the training set grows. One curve on the slides reaches about 95% and still looks as if more data would help. A learning-curve experiment trains on larger subsets and tests on a fixed test set. The lesson stated on the slide: every bias makes some functions easier and others harder.

Problems:

- Overfitting: the tree matches the training examples and fails on the test set. Pruning removes nodes that are not clearly relevant. A practical stop is to refuse a split whose best information gain is below a threshold.
- Information gain prefers attributes with many values (a unique time string, a social security number). Gain ratio divides the gain by the information content of the attribute itself, which penalises attributes with many values. The denominator is smaller for attributes with smaller domains.
- Splitting on one feature at a time misses some feature interactions. The slides call this the Costanza party problem and say there is no obvious easy fix.
- Missing values, multivalued attributes, infinite domains, and continuous outputs are limitations. Continuous outputs take the method outside ordinary classification trees. Many extensions exist.

Use a decision tree when examples are attribute-value pairs, the target is discrete, a disjunctive rule is acceptable, and the data may be noisy. Examples: equipment or medical diagnosis, credit risk.

### Lab week 9

Five houses, features Furniture (Yes/No), Nr rooms (3 or 4), New kitchen (Yes/No), target Rent (Yes/No). Supervised binary classification.

| House | Furniture | Rooms | New kitchen | Rent |
| --- | --- | --- | --- | --- |
| 1 | No | 3 | Yes | Yes |
| 2 | Yes | 3 | No | No |
| 3 | No | 4 | No | Yes |
| 4 | No | 3 | No | No |
| 5 | Yes | 4 | No | Yes |

Full set: 3 Yes, 2 No. `H(S) = -(0.6*log2(0.6)) - (0.4*log2(0.4)) = 0.971` bits.

Information gain at the root:

- Furniture: 0.020 bits.
- Nr rooms: 0.420 bits.
- New kitchen: 0.171 bits.

Root is Nr rooms. The rooms = 4 branch contains houses 3 and 5, both Yes, entropy 0, so it is a Yes leaf. The rooms = 3 branch contains houses 1, 2, and 4, entropy 0.918.

On that subset, information gain is 0.251 for Furniture and 0.918 for New kitchen. New kitchen splits it into two pure leaves: kitchen Yes is house 1 (Rent Yes), kitchen No is houses 2 and 4 (Rent No). Furniture is never used.

Rules:

- If rooms = 4 then Rent = Yes.
- If rooms = 3 and new kitchen = Yes then Rent = Yes.
- If rooms = 3 and new kitchen = No then Rent = No.

The tree has 2 internal nodes and 3 leaves and classifies all 5 training rows. A new house with 4 rooms is Yes regardless of the other features. A new house with 3 rooms and a new kitchen is Yes. Prediction is a walk from the root to a leaf, which is why the model is easy to explain.

### Check yourself

- State the four ID3 base cases.
- Compute entropy for a 3-and-2 split and explain why a pure child has gain.
- Say why a student ID is a bad split even if information gain looks high.
- Walk a new house through the lab tree.

---

## Lecture 10: Bayes nets

No lab solution in this folder.

### Need to know

A random variable is an uncertain aspect of the world. Examples: `R` raining in `{true, false}` (often `+r, -r`), `T` in `{hot, cold}`, `D` a drive time in `[0, infinity)`, `L` a ghost location. A distribution assigns a probability to each value. Each probability is at least 0, and the probabilities in one distribution sum to 1.

A joint distribution over `X1, ..., Xn` assigns a probability to every full assignment. Those probabilities are non-negative and sum to 1. If there are `n` variables each of domain size `d`, the table has `d^n` entries. That is impractical except for tiny models.

An event is a set of outcomes. Its probability is the sum of the joint entries in that set. From the joint you can answer AND, OR, and single-variable questions.

Marginalisation sums out the variables you do not want. In the weather table on the slides (`P(hot, sun) = 0.4`, `P(hot, rain) = 0.1`, `P(cold, sun) = 0.2`, `P(cold, rain) = 0.3`): `P(hot) = 0.5`, `P(sun) = 0.6`.

Conditional probability is defined by `P(a, b) = P(a | b) P(b)`, so `P(a | b) = P(a, b) / P(b)`. A conditional distribution is a distribution over some variables given fixed values of others. Check that each conditional row sums to 1. From the same table, `P(sun | hot) = 0.4/0.5 = 0.8`.

Bayes' rule follows from the two factorisations `P(a, b) = P(a | b) P(b) = P(b | a) P(a)`:

`P(b | a) = P(a | b) P(b) / P(a)`.

It is useful because one direction is often easy to estimate and the other is the one you need.

A Bayes net is a directed acyclic graph plus a conditional distribution for each node given its parents. Nodes are variables. A missing arc means a conditional independence. The local table is a CPT: each row is the distribution of the child given one setting of the parents. The net is topology plus those local probabilities.

The alarm network is the one to memorise.

- `P(B) = 0.001`, so `P(not B) = 0.999`.
- `P(E) = 0.002`, so `P(not E) = 0.998`.
- `P(A | B, E)`: both true 0.95, burglary only 0.94, earthquake only 0.29, neither 0.001.
- `P(J | A) = 0.90` and `P(J | not A) = 0.05`.
- `P(M | A) = 0.70` and `P(M | not A) = 0.01`.

Free parameters in a CPT: if the parents have domain sizes `d1, ..., dk` and the child has domain size `d`, the count is `(d - 1) * d1 * ... * dk`, because each row sums to 1. The alarm slide marks 1, 1, 4, 2, 2 free parameters on the five tables.

If `n` variables have maximum domain size `d` and at most `k` parents, the full joint is `O(d^n)` and the Bayes net is `O(n * d^k)`. Size grows linearly with `n` when each variable has a small local set of causes.

Global semantics, the chain rule for the graph:

`P(X1, ..., Xn) = product_i P(Xi | Parents(Xi))`.

Worked atom:

`P(b, not e, a, not j, not m) = P(b) P(not e) P(a | b, not e) P(not j | a) P(not m | a)`

`= 0.001 * 0.998 * 0.94 * 0.1 * 0.3 = 0.000028`.

Compare with the ordinary chain rule `P(Xi | X1, ..., X(i-1))`. In topological order, parents precede children, and the net asserts `P(Xi | earlier variables) = P(Xi | Parents(Xi))`. Equivalently: every variable is conditionally independent of its non-descendants given its parents. Choose parents that shield the node from the other earlier variables.

Inference by enumeration, for the probability of burglary given that both John and Mary call:

`P(B | j, m) = alpha * sum over e, a of P(B) P(e) P(a | B, e) P(j | a) P(m | a)`.

`alpha` restores the two values of `B` so they sum to 1. Exact inference is a sum of products. The naive sum has exponentially many terms. Factor repeated subexpressions, in the same spirit as rewriting `uwy + uwz + ... + vxz` as `(u+v)(w+x)(y+z)`, which drops 16 multiplies and 7 adds down to 2 multiplies and 3 adds.

### Check yourself

- Marginalise one variable out of a 2-by-2 joint and then form a conditional row.
- Expand one full assignment in the alarm net as a product of CPT entries.
- Count free CPT parameters for a Boolean child with two Boolean parents.
- Say what a missing arc means.

---

## Lecture 11: MDPs and reinforcement learning

No lab solution in this folder. Lecture 5 introduced the agent loop. This lecture is the formal version.

### Need to know

An MDP is:

- States `s` in `S`.
- Actions `a` in `A`.
- Transition `T(s, a, s') = P(s' | s, a)`.
- Reward `R(s, a, s')` on the transition.
- A start state, and possibly a terminal state.
- An additive utility of discounted rewards. The discount `gamma` in `[0, 1)` makes the infinite sum `1 + gamma + gamma^2 + ... = 1 / (1 - gamma)`.

A policy `pi(s)` maps a state to an action. The goal is a policy that maximises expected utility.

Reinforcement learning keeps the MDP but the agent does not know `T` or `R`. It must try actions. All learning uses observed samples `(s, a, s', r)`. The agent receives rewards, and its utility is defined by those rewards.

Four ideas: exploration (try unknown actions), exploitation (use what you know), sampling (repeat to estimate), and generalisation (a lesson in one state may apply in similar states).

Passive learning evaluates a fixed policy. The agent does not choose actions. This is not offline planning: the actions really occur.

Model-based passive learning counts outcomes. For each `(s, a)`, the fraction of times `s'` follows is the estimate of `T`, and the observed rewards estimate `R`. Then solve the learned MDP as if it were correct. In the grid example with `gamma = 1`: `T(B, east, C) = 1.00`, `T(C, east, D) = 0.75`, `T(C, east, A) = 0.25`, `R(D, exit, x) = +10`, and the ordinary moves reward `-1`. Advantage: each experience updates a model that links states. Limit: one state-action pair at a time does not scale, and a huge state space cannot be solved as a tabular MDP.

The age analogy: if you know `P(age)` you compute the expectation from the distribution (model-based). If you do not, you average samples (model-free). Samples appear with the right frequencies, so the average converges.

Direct evaluation, still passive: follow `pi`, and whenever you visit a state, record the sum of discounted rewards from there to the end of the episode. Average those samples. It needs no model and eventually gets the right averages. It wastes the links between states, so each state is learned separately and learning is slow. In the sample episodes, B and E can receive different values even though both move to C, because the averages do not share the successor.

Temporal-difference learning updates `V(s)` on every transition `(s, a, s', r)`, not at the end of the episode. Likely successors are sampled more often, so they dominate the average. The update is a running average that moves `V(s)` toward the sampled one-step target `r + gamma * V(s')`. With a fixed `alpha` this is an exponential moving average: recent samples count more, and old values are forgotten. Decreasing `alpha` can make the average converge. TD policy evaluation still does not produce a new policy, because choosing an action needs the result of each action, and `V` does not store that.

Q-learning stores action values instead.

- `Q(s, a)` is the expected value of taking `a` in `s` and thereafter acting optimally.
- `V(s) = max_a Q*(s, a)`.
- `pi*(s) = argmax_a Q*(s, a)`.
- Sample update:

`Q(s, a) <- (1 - alpha) * Q(s, a) + alpha * [r + gamma * max_a' Q(s', a')]`.

The `max` is what makes the update look one optimal step ahead. After learning, `pi_Q(s) = argmax_a Q(s, a)` needs no model. The Q table is larger than the V table: one entry per state-action pair, not per state.

Active learning chooses the actions. Passive learning does not. Q-learning is off-policy: it converges to the optimal policy even if the actions used to collect data are not optimal. Conditions: explore enough, and decrease `alpha`, but not so fast that updates stop too early. In the limit, the behaviour policy does not matter.

Exploration versus exploitation is the active-learning tradeoff. Epsilon-greedy: with probability `epsilon` act at random, otherwise follow the current policy. Lower `epsilon` over time, or you keep acting randomly after the values are known. An exploration function replaces the value `u` with an optimistic value that grows when the visit count `n(s, a)` is small, for example `u + k / n(s, a)` with a constant `k`. The bonus flows back to states that lead into unknown states, because those states' targets include the optimistic Q. The modified Q update uses that exploration value in place of the plain max.

Regret is the gap between the rewards you actually collected, including early mistakes, and the rewards of always acting optimally. Random exploration and an exploration function can both reach an optimal policy. Random exploration has higher regret.

Tabular Q-learning cannot visit or store every state in a large problem. Approximate Q-learning represents a state, or a state-action pair, by features: distance to the nearest ghost, distance to the nearest dot, ghost count, `1 / (distance to dot)^2`, whether Pac-Man is in a tunnel, whether the action moves toward food. A linear Q function is a weighted sum of those features. Experience is stored in a few weights. The cost is that two states can share features and still deserve different values. The weight update raises or lowers the weights of features that were active. If the outcome was worse than expected, features that were on are blamed, so similar states become less attractive.

### Check yourself

- List the MDP components and the meaning of `gamma`.
- Contrast model-based counts, direct evaluation, TD updates of `V`, and Q-learning.
- Write the Q update and say why the `max` makes it off-policy.
- Define regret, and say what epsilon-greedy still does after learning if `epsilon` stays high.

---

## Formula card

Search:

- Problem: `<S0, A, T, G, C>`.
- Node: state, parent, action, path cost.
- BFS time: `(b^(d+1) - 1) / (b - 1)`.
- UCS: expand smallest `g`. Goal test on expansion.
- A*: `f = g + h`. Admissible: `h <= h*`. Consistent: `h(n) <= cost(n, n') + h(n')`.

Local search and CSP:

- Hill climbing returns the first local optimum.
- Random-restart count about `1/p`.
- Backtracking: one variable per depth, domain values as the branch.
- MRV, then degree. LCV for values.
- Arc `X -> Y` is consistent when every `x` has a legal `y`.

Learning:

- Hypothesis `h: X -> Y`. Regression is continuous. Classification is discrete.
- Linear model: `y = <w, x> + b`.
- MSE: `(1/n) * sum (y - y_hat)^2`.
- Closed form: `w* = (X^T X)^(-1) X^T y`.
- Gradient step: `w <- w - eta * gradient`.
- Perceptron: update only if wrong, `w <- w + alpha * (y - y_hat) * x`.
- Sigmoid: `1 / (1 + exp(-z))`. Derivative `s * (1 - s)`.
- Sigmoid output delta: `y(1-y)(target - y)`.
- Entropy: `sum -p log2 p`. Gain: parent entropy minus the weighted child entropies.
- Joint from a Bayes net: product of `P(Xi | parents)`.
- Q update: `(1 - alpha) * Q(s, a) + alpha * [r + gamma * max Q(s', a')]`.
- Discounted infinite horizon sums to `1 / (1 - gamma)`.
