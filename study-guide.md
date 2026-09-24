# 2802ICT Intelligent Systems: Lecture Study Guide

These notes follow the lecture PDFs and the lab solutions in this folder. They are written so you can learn the idea, not only recognise the name. Pair them with the [quiz](Study%20MCQs.md) when you want to test recall.

Textbook: Russell and Norvig, *Artificial Intelligence: A Modern Approach*, 3rd edition.

Lecture numbers below match the PDF titles. Week 1's tentative timetable put decision trees earlier and neural networks later. The slides actually used are the order in this file.

`Lecture8.pdf` in the Lectures folder is a 3006ICT robotics lecture. Ignore it for this course.

## How to use this file

1. Open one lecture from the contents list.
2. Read **How to picture it** before the definitions. If the picture is clear, the formula is easier.
3. Use **Need to know** for the exam content, and **Memory hooks** when names start to blur.
4. Do **Check yourself** with the answer covered, then uncover it.
5. Lab sections exist only where this folder has a solution. Weeks 1 to 4, 10, and 11 do not.

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

From the week 1 slides: Assignment 1 and Assignment 2 are 30% each. The final exam is 40%, closed book, and you need at least 40/100 on the exam to pass the course. The exam window on the slides is 15-24 October 2026. Late work loses 5% per day for up to 7 days, unless an extension is granted.

The course has two strands, and the lectures follow them in order. Weeks 1 to 4 are classical AI: you write the rules and the program searches. Weeks 5 to 11 are learning: you give examples, or rewards, and the program finds the rule.

## Search algorithms at a glance

Before the table, fix the three letters you will see all through search.

- `b` is the branching factor: the most children any node has. A crossroads with 3 exits has `b = 3` if that is the worst junction.
- `d` is the depth of the shallowest goal. "How many steps is a nearby solution?"
- `m` is the longest path the search might follow. In a maze with loops, `m` can be infinite.
- `C*` is the cost of the cheapest solution, not the number of steps.
- `epsilon` is the smallest step cost. UCS needs this to be greater than 0, otherwise it can take infinitely many tiny steps.

| Algorithm | Frontier | Complete? | Optimal? | Time | Space |
| --- | --- | --- | --- | --- | --- |
| BFS | FIFO queue | Yes, if `b` is finite | Yes, if every step cost is equal | `O(b^d)` | `O(b^d)` |
| UCS | Priority queue by `g` | Yes, if every step cost is at least `epsilon` | Yes | `O(b^(C*/epsilon))` | `O(b^(C*/epsilon))` |
| DFS | LIFO stack | No, in infinite spaces or with loops | No | `O(b^m)` | `O(bm)` |
| Depth-limited | Stack, depth cap `l` | No, if the shallowest goal is deeper than `l` | No | `O(b^l)` | `O(bl)` |
| Iterative deepening | Repeated depth-limited search, `l = 0, 1, 2, ...` | Yes, if `b` is finite | Yes, if step costs are equal | About `O(b^d)` | `O(bd)` |
| Greedy best-first | Priority queue by `h` | No in general. Yes in a finite space with repeated-state checking | No | `O(b^m)` | `O(b^m)` |
| A* | Priority queue by `f = g + h` | Yes, if `b` is finite and step cost is at least `epsilon` | Yes, with an admissible heuristic for tree search, and a consistent heuristic for graph search | Exponential | Exponential |

**Complete** means "if a solution exists, this algorithm will find one." **Optimal** means "the one it finds is a cheapest one." A complete algorithm can still return a long expensive path. DFS is the usual example.

The frontier is the to-do list: states you have generated and not yet expanded. The data structure of that list is the whole strategy.

- Queue (FIFO, first in first out): like a bakery line. Whoever joined first is served first, so you finish an entire layer before the next. That is BFS.
- Stack (LIFO, last in first out): like a stack of plates. You always take the plate you just put down, so you dive deep. That is DFS.
- Priority queue: not arrival order. You always take the best score. UCS uses cost so far (`g`). Greedy uses the guess (`h`). A* uses `g + h`.

The slides call iterative deepening the best general uninformed choice: it uses about as much memory as DFS and finds a shallow goal like BFS. Use BFS when you know solutions are short and memory is available. Use DFS when solutions are common, because you may hit one quickly down a single branch. UCS is the only uninformed method that returns a lowest-cost path when step costs differ.

## Learning tasks at a glance

Ask two questions of any problem. "Do I have the right answer for each example?" and "Is that answer a category or a number?"

| Task | Labels? | Output | Examples from the slides and labs |
| --- | --- | --- | --- |
| Classification | Yes | Discrete class | Loan default, rain or no rain, digit recognition |
| Regression | Yes | Continuous number | House price, energy use in kWh |
| Clustering | No | Groups | Essay grouping, viewer segments |
| Association rules | No predefined class | Co-occurrence rules | `{onions, potatoes} => {burger}` |
| Semi-supervised | A few labels, many unlabelled | Usually a class | Pseudo-labelling, medical images |
| Reinforcement learning | No input-output pairs | A policy | Delayed reward, credit assignment |

**Memory hook.** Supervised: a teacher marks the homework. Unsupervised: you sort the pile yourself and nobody says the group names. Reinforcement: nobody marks each move, but the score at the end tells you the game went well or badly.

---

## Lecture 1: Introduction and agents

Reading: AIMA Chapters 1-2. No lab solution in this folder.

### How to picture it

This lecture is a map of the subject, not an algorithm. Every later lecture sits on it. Search (weeks 2 to 4) is the "rational action by explicit reasoning" corner. Learning (weeks 5 to 11) is how a system gets the knowledge it was not given by hand.

### Need to know

Traditional AI is top-down. A person writes the representation and the rules, and the machine reasons. Machine learning is bottom-up. The machine is shown examples and builds its own rule. Exam answers in this course are expected to say both how a method works and why you would choose it.

The four dimensions come from two questions. Does the system **think** or **act**? Is the standard **human** or **rational**?

|  | Human | Rational |
| --- | --- | --- |
| Thinking | Match human thought, including errors and biases. Cognitive science is top-down: computer models plus psychology experiments. Neuroscience is bottom-up: watch the physical brain. | Laws of thought. Start from Aristotle's syllogisms and end at first-order logic. The aim is valid inference, even when a person would not think that way. |
| Acting | Behave so that an observer accepts you as human. | Do the right thing: the best expected outcome given what you know. |

**Acting humanly** is the Turing Test (Alan Turing, 1950), also called the Imitation Game. A judge converses with a hidden human and a hidden machine. If the judge cannot tell which is which, the machine has passed. The slides list four things a machine needs before that test is a serious test of intelligence: natural language processing, knowledge representation, automated reasoning, and machine learning. A chatbot can fool a judge by pattern-matching and still lack those four. The slides call that cheating the test.

**Thinking humanly** splits in two. Cognitive science builds a model and checks it against how people behave. Neuroscience starts from brain measurements and works upward. Same goal, opposite direction.

**Thinking rationally** does not try to copy people. It tries to derive only what follows from the premises.

**Acting rationally** is the course's working definition of intelligence for an agent. "Rational" here does not mean "sounds logical in English." It means the action with the best expected result. A rational agent can still be uncertain. It uses the information it has.

Milestones the slides want you to attach to a technique:

- 1956, Dartmouth College: the name Artificial Intelligence is adopted. This is the birth label, not a technical result.
- 1997, Deep Blue beats Kasparov: search, not learning.
- 2016, AlphaGo beats Lee Sedol: deep reinforcement learning. The Go state space on the slide is about `10^170`, which is why brute-force search is hopeless and learning a policy matters.
- 2021-2026 on the slides, in order: generative models (DALL-E, ChatGPT, GPT-4, Sora), then reasoning models (o3, DeepSeek R1), then agentic systems that break a long task into steps, call tools, and revise their own work. You do not need the product names beyond being able to place "search", "deep RL", and "agents" on the timeline.

Symbolic AI, also called GOFAI (good old-fashioned AI), stores concepts as symbols and applies explicit rules. A medical rule "if fever then ..." is symbolic. So is heuristic search. You can read the derivation. You do not need a training set. The cost is brittleness: one unexpected input, and a hand-written rule has nothing to say. Writing the rules for a photo of a cat does not scale.

Subsymbolic AI, here meaning deep learning, stores numbers (weights) and learns them from raw inputs. It handles images, speech, and other data that have no tidy symbols. The cost is that the decision is a black box, and training wants a large labelled set and a lot of compute.

Neural-symbolic hybrids are named as the attempt to keep both: learned perception, plus a symbolic layer you can check. The slides do not ask you to implement one.

An **agent** is anything that senses an environment and acts on it. The slide equation is `agent = architecture + program`.

- Architecture is the body: processors, cameras, wheels, power.
- Program is the software that computes the agent function.
- The agent function is the mapping from what has been perceived to the action to take now.

A **state** is a complete snapshot of the agent and the world together. If your state leaves out "is the door open?", no algorithm can plan around the door. The representation is a ceiling on what the system can do. Choose the smallest state that still contains everything the decision depends on. That idea returns in search (week 2) and in approximate Q-learning (week 11), where a state is replaced by a few features.

Sensors take the world in. Actuators push the world out.

- Human sensors: eyes, ears, touch, smell. Human actuators: hands, legs, voice.
- Robot sensors: cameras, LiDAR, thermometers, infrared. Robot actuators: motors, hydraulics, speakers.

**PEAS** is how you specify an agent before you write code. The letters are Performance, Environment, Actuators, Sensors.

- Performance is the score, not the hardware. For a taxi: arrive safely, obey the law, keep the passenger comfortable, make a profit.
- Environment is everything that can change the score and that the agent does not fully control: roads, pedestrians, weather.
- Actuators are the controls: steering, throttle, brakes, horn, display.
- Sensors are the measurements: cameras, radar, GPS, engine sensors, compass.

Shopping agent, so you have a second example that is not a robot: performance is price, quality, recommendation quality, and speed. Environment is websites, shops, and shipping APIs. Actuators are form fills, redirects, and checkout requests. Sensors are HTML, scripts, JSON, and page layout.

When you write PEAS, performance measures must be things you could score. "Be intelligent" is not a performance measure. "Reach the destination without a collision" is.

### Memory hooks

- Four dimensions: draw a plus sign. Left/right is human versus rational. Up/down is thinking versus acting. Turing sits in acting-human. Logic sits in thinking-rational. "Best expected outcome" sits in acting-rational.
- PEAS: "How do I score it, where does it live, what can it move, what can it see?"
- Agent: body plus brain. State: the photograph the brain is allowed to look at.

### Check yourself

- Place cognitive science, neuroscience, the Turing Test, and laws of thought on the grid. **Answer.** Cognitive science and neuroscience are thinking-human (top-down and bottom-up). The Turing Test is acting-human. Laws of thought are thinking-rational.
- Write PEAS for a vacuum robot. **Answer.** Performance: clean floor, time, energy. Environment: rooms, dirt, furniture. Actuators: wheels, suck. Sensors: dirt sensor, bump sensor, position.
- One advantage and one limit of each paradigm. **Answer.** Symbolic: readable rules, but brittle and hard to scale. Subsymbolic: learns from raw data, but opaque and data-hungry.

---

## Lecture 2: Uninformed search

Reading: AIMA Chapter 3, pages 64-91. No lab solution in this folder. Assignment 1's maze is this lecture in code.

### How to picture it

You are in a building you have never seen. You know the room you started in, you can try doors, and you will recognise the exit when you enter it. You do not have a map and you do not have a hint about which corridor is "toward" the exit. That absence of a hint is what "uninformed" means. The only choice left is the order in which you open doors.

Solving the problem is three jobs, in order: formulate it (turn the story into states and actions), search (find a sequence of actions), execute (actually do them). In this course, one solution is enough when a solution exists. Optimal means the cheapest of those solutions, and only some algorithms promise that.

### Need to know

A search problem is the 5-tuple `<S0, A, T, G, C>`. Say it as "start, actions, transition, goal, cost."

- `S0` is the initial state. Once it is fixed, you only care about states you can reach from it. The rest of a huge world is irrelevant.
- `A(s)` is the set of actions that are legal in state `s`. In a maze, you cannot walk through a wall, so that action is not in `A(s)`.
- `T(s, a) = s'` is the transition model, also called the successor or result function. "If I am in `s` and I do `a`, I land in `s'`."
- `G` is the goal test. It can accept more than one state. The vacuum world is done when there is no dirt left, and the slides mark two such states (7 and 8).
- `C(s, a, s')` is the step cost of that one move. The path cost is the sum of step costs along the path. In Romania the step cost is kilometres. In the vacuum world every action costs 1.

A **solution** is a sequence of actions from `S0` to a state that passes `G`. An **optimal** solution has the lowest path cost among solutions.

A **state** is a situation in the world. A **node** is a notebook entry about how you got there. The node stores four fields: the state, the parent node, the action that was applied to the parent, and the path cost from the start. You need the parent pointers to walk backward and read off the action list. If you store only states, you know you reached Bucharest and you cannot say which roads you took.

Worked formulations you should be able to write from scratch:

- Romania. Start: in Arad. Goal: in Bucharest. Actions: drive to a neighbouring city. Transition: that drive puts you in the neighbour. Cost: distance in km. One solution on the slide is Arad, Sibiu, Fagaras, Bucharest. It is a solution. It is not the cheapest (see week 3: 450 km versus 418 km).
- Vacuum. Eight pictured states. Actions Left, Right, Suck. Example transition: `T(3, Right) = 4`. Goal: no dirt. Cost: 1 per action.
- Pac-Man, one ghost-free agent on the slide: same five components. Initial position and food layout, legal moves, the resulting grid cell, "all food eaten" or whatever goal the problem states, and a path cost.

The **state space graph** has one vertex per state and an edge per action. It can be too big to draw. The **search tree** is what the algorithm builds: the root is the start, and each child is the result of one action. The same state can appear in many branches if you do not check repeats. The tree can grow exponentially even when the graph is modest, because there are many paths to the same city.

General tree search:

1. Put the initial state on the frontier.
2. If the frontier is empty, there is no solution. You have run out of places to try.
3. Remove one node. If its state passes the goal test, return the path (follow parents back to the root).
4. Otherwise expand it: apply every legal action, and add the child nodes to the frontier.

The algorithm is the same for BFS, DFS, and UCS. Only step 3's choice of which node to remove changes.

**Graph search** adds an explored set. When you expand a node you record its state, and you refuse to add a child whose state is already on the frontier or already explored. That stops loops such as Arad to Sibiu and back to Arad forever. Two warnings from the slides. The check is on the **state**, not on the node object. And throwing away a second path to a state can throw away a cheaper path. Tree search can be exponentially larger, but optimality proofs are easier. Graph search saves work and can break optimality unless you add a repair. UCS adds that repair: if you later find a cheaper path to a state still on the frontier, replace the old node.

Four properties, and they are not synonyms:

- Complete: a solution is returned whenever one exists.
- Optimal: a lowest-cost solution is returned.
- Time: how many nodes are generated. Usually `O(b^d)` or `O(b^m)`.
- Space: how many nodes are stored at once.

**BFS** expands the shallowest node, implemented as a FIFO queue. New children join the back. It is complete when `b` and `d` are finite: every layer is finite, and you will reach depth `d`. It is optimal only when every action has the same cost, because then "fewest steps" and "lowest cost" are the same thing. If one step costs 100 and another costs 1, the path with fewer steps can cost more. Time is the sum of a geometric series: `1 + b + b^2 + ... + b^d = (b^(d+1) - 1) / (b - 1) = O(b^d)`. Space is also `O(b^d)`, because the explored set holds about `O(b^(d-1))` nodes and the frontier holds about `O(b^d)`. The slides say space, not time, is what stops BFS in practice. You run out of memory while still having CPU left.

**UCS** (uniform-cost search) expands the node with the smallest path cost `g`. The frontier is a priority queue ordered by `g`. If every step costs the same, UCS and BFS expand in the same order. Three differences from BFS matter in exams:

- Order is by cost, not by depth.
- The goal test runs when the node is **selected for expansion**, not when it is first generated. A cheap-looking partial path might later become expensive, and an expensive-looking node might be the first step of a cheap total. You may only declare victory when that node is the cheapest thing left on the frontier. At that moment, every other unfinished path costs at least as much, so no cheaper route to the goal can still be hiding.
- If a better path is found to a node still on the frontier, keep the better one.

UCS is complete if every step costs at least some `epsilon > 0`. Without that, an infinite chain of zero-cost moves never reaches the goal. It is optimal. Time and space are `O(b^(C*/epsilon))`. Read the exponent as "how many minimum-size steps fit into the optimal cost." If steps are large, the exponent is small and the search is smaller.

**DFS** expands the deepest node, implemented as a stack. It is not complete: an infinite branch, or a loop, can be followed forever while a goal sits on another branch. If you refuse to repeat a state along the current path, DFS becomes complete in a finite state space. Time is `O(b^m)`. That is worse than BFS when the longest path `m` is much deeper than the shallowest goal `d`. It can be better when goals are dense, because you may hit one without generating the rest of the tree. Space is `O(bm)`: only the current path and its unexplored siblings. That linear space is the reason anyone uses DFS. It is not optimal. The first goal you hit is whichever one sat at the bottom of the branch you tried first.

**Depth-limited search** is DFS that pretends nodes at depth `l` have no children. If the shallowest goal is deeper than `l`, it fails even though a solution exists.

**Iterative deepening** fixes that by trying `l = 0`, then `1`, then `2`, and so on, until a goal appears. It sounds wasteful because shallow nodes are regenerated. Most nodes are in the last layer, and that layer is generated only once, so the extra work is a small constant factor, not a new exponent. You get BFS's completeness and optimality (equal step costs) with DFS's `O(bd)` memory. The slides call it the practical default among uninformed searches.

The summary on the slides is worth memorising as advice, not as a theorem. Formulate by throwing away real-world detail until the state space can actually be searched. Prefer BFS when solutions are short. Prefer DFS when many solutions exist. Prefer iterative deepening when you want a shallow solution and you cannot store the BFS frontier.

### Memory hooks

- Five parts: "Where do I start, what can I do, where does that land me, how do I know I am done, what did it cost?"
- Node versus state: the state is the city. The node is the diary entry that says how you got there and what it cost.
- BFS: bread line, layer by layer. DFS: dive, then backtrack. UCS: always expand the cheapest receipt so far.
- "Complete finds a way. Optimal finds the cheap way."

### Check yourself

- Vacuum five-tuple. **Answer.** Start in a pictured state such as state 1. Actions Left, Right, Suck. `T` says where the agent is and whether the dirt is gone. Goal: no dirt. Cost 1 per action.
- Which node field rebuilds the route? **Answer.** Parent pointers, together with the action stored on each node.
- Why can BFS be suboptimal? **Answer.** It minimises the number of steps. If step costs differ, fewer steps can cost more.
- Why does UCS test the goal on expansion? **Answer.** The first time you generate the goal, a cheaper path to it may still be on the frontier. When you select it, it has the smallest `g` of anything left, so nothing cheaper remains.

---

## Lecture 3: Informed search

Reading: AIMA Chapter 3, pages 92-109. No lab solution in this folder.

### How to picture it

Uninformed search treats every legal road as equally promising. Informed search adds a hint. Driving from the Gold Coast toward Sydney, you already know that a town to the north is probably a waste, even before you add up the kilometres. That hint is a heuristic. It can be wrong. The whole lecture is about using the hint to search less, without letting a bad hint make you miss the best route.

### Need to know

A **heuristic** is a rule that estimates how far a state is from a goal, or how costly it will be to finish via that state. It is extra knowledge of this particular problem. UCS does not have one. A heuristic function `h(n)` is the calculation of that estimate.

Three numbers, and students mix them constantly:

- `g(n)` is money already spent to reach `n`. It is exact, not a guess. UCS sorts by `g`.
- `h(n)` is a guess of the money still to spend from `n` to a goal. Greedy search sorts by `h`.
- `f(n)` is the guess of the total cost of a path that goes through `n`. A* sorts by `f`.

**Best-first search** is the family name. Put nodes in a priority queue ordered by some `f`, and always expand the smallest `f`. UCS is best-first with `f = g`. The two informed members are greedy best-first and A*.

**Greedy best-first** sets `f(n) = h(n)`. It expands whichever node looks closest to the goal, and it ignores how expensive the trip was to get there. The Romania heuristic is straight-line distance to Bucharest. From Arad, Sibiu looks closer than Timisoara or Zerind, so Sibiu is expanded next.

Greedy is not optimal. The slides' numbers: Arad-Sibiu-Fagaras-Bucharest is 450 km, and the route Arad-Sibiu-Rimnicu Vilcea-Pitesti-Bucharest is 418 km. Greedy can take the 450 km route because Fagaras looks closer to Bucharest than Rimnicu does, even though the road via Rimnicu is shorter overall. It is not complete if it can loop (Iasi to a neighbour and back). With repeated-state checking in a finite map, it is complete. Time and space are `O(b^m)` in the worst case. A good heuristic often does much better than that bound. Space is large because, like BFS, it keeps the frontier.

**A\*** sets `f(n) = g(n) + h(n)`. The already-spent cost stops it from charging down a path that looked short and has become expensive. The heuristic stops it from exploring roads that go the wrong way, which is UCS's weakness.

A* is not automatically optimal. If `h` says "almost there" and the truth is "still a long way", A* may commit to a bad path and announce success too soon. The repair is a restriction on `h`.

**Admissible** means `h(n) <= h*(n)` for every node, where `h*(n)` is the true cheapest cost from `n` to a goal. The guess never overestimates. It is optimistic: it may think the goal is closer than it is, but it never thinks the goal is farther than it is. Straight-line distance is admissible because a road cannot be shorter than the straight line. Theorem from the slides: if `h` is admissible, A* **tree search** (no repeated-state check) is optimal. Admissibility is not enough once you start deleting repeated states. Graph search can close off a state along a path whose `f` looked good only because of an inconsistent guess, and then refuse the better path when it arrives.

**Consistent** (also called monotonic) is the stronger condition. For every node `n` and every successor `n'`:

`h(n) <= cost(n, n') + h(n')`.

Read it as a triangle inequality. The guess at `n` cannot drop, after one step, by more than that step actually cost. If it did, the guess was internally dishonest. From the inequality you can derive `f(n') >= f(n)` along any path, so `f` never decreases as you walk forward. Every consistent heuristic is admissible. The converse is not true: a heuristic can be admissible and still inconsistent. If `h` is consistent, A* **graph search** is optimal. Nodes come off the frontier in order of increasing `f`. Draw that as contours: first everything with `f` below 400, then below 420, and so on. Timisoara, on the Romania figure, sits outside the contour that already reached Bucharest, so it is never expanded.

Properties of A*: complete if `b` is finite and every step costs at least `epsilon`. Time and space are still exponential, because it keeps every generated node. Optimal under the heuristic conditions above: admissible for tree search, consistent for graph search.

The useful work in a hard problem is inventing the heuristic, not coding the queue. Both standard 8-puzzle heuristics are admissible because each is the exact cost of an easier puzzle.

The real rule is: a tile may move from A to B only if A is next to B **and** B is blank. Relaxations:

- Drop "B is blank", so a tile may step to any adjacent square, even through other tiles. The cheapest solution of that puzzle is the Manhattan distance. `h2(n)` is the sum of those distances. On the start state in the slides, `h2 = 3+1+2+2+2+3+3+2 = 18`.
- Drop both conditions, so a tile may jump anywhere. The cheapest solution is "one move per tile that is in the wrong place." `h1(n)` is the number of misplaced tiles. On that start state, `h1 = 8`. (The blank is not counted as a tile that is "misplaced" in the usual statement; the slide's 8 matches the eight tiles.)

Why is the relaxed cost admissible? Any legal solution of the real puzzle is also a legal solution of the easier puzzle. So the easiest real solution cannot be shorter than the easiest relaxed solution. The relaxed cost is a lower bound. That is the general method: write the problem formally, delete preconditions, and use the optimal cost of what remains as `h`.

**Dominance.** If `h2(n) >= h1(n)` for every `n`, and both are admissible, `h2` dominates `h1`. Closer to the truth, without crossing it, means fewer nodes expanded. Counts from the slides, for solution length `d`:

| Solution depth | IDS | A* with h1 | A* with h2 |
| --- | --- | --- | --- | 
| 12 | 3,644,035 | 227 | 73 |
| 24 | about 54,000,000,000 | 39,135 | 1,641 |

A* with the weaker heuristic still crushes iterative deepening. The stronger heuristic crushes the weaker one. "It all depends on `h` and the shape of the space" is the slide's conclusion.

Memory is A*'s practical failure. Three names, and the slides point the detail at AIMA section 3.5.3:

- IDA* is iterative deepening with a cutoff on `f`, not on depth.
- RBFS is recursive best-first search.
- SMA* is simplified memory-bounded A*.

RBFS and SMA* stay optimal, use a limited amount of memory, and can finish problems that kill A* by filling RAM.

### Memory hooks

- `g` has already Gone. `h` is How far you Hope is left. `f` is the Full estimate.
- Admissible: "Always a lower guess, never a higher one." Optimistic.
- Consistent: "the guess cannot fall faster than you actually travel."
- Tree search wants admissible. Graph search wants consistent. Consistent is the stricter one, and it implies admissible.
- Dominating heuristic: bigger `h`, still admissible, fewer nodes.

### Check yourself

- `g = 10`, `h = 6`. What is `f`? **Answer.** 16, the estimated total through this node.
- Why does an overestimate break optimality? **Answer.** A* may expand a worse path whose `f` looks smaller, reach a goal, and stop, while the true best path was left on the frontier with an unfairly large `h`.
- Which condition for which search? **Answer.** Admissible for tree search. Consistent for graph search.
- Where do `h1` and `h2` come from? **Answer.** `h1` relaxes the puzzle so a tile can move anywhere. `h2` relaxes it so a tile can move to any adjacent square.

---

## Lecture 4: Local search and CSPs

Reading: AIMA Chapter 4, pages 120-129. No lab solution in this folder. Assignment 1's crossword is a CSP.

### How to picture it

Weeks 2 and 3 hunt for a path. This week often does not care about the path at all. For 8 queens, the answer is a board where no two queens attack. Nobody asks which queen you moved first. That is local search: walk from configuration to configuration, keep the one with the best score, and throw the route away.

CSPs are the other half of the week. The state is no longer a black box. It is a form with blanks (variables), a list of allowed answers for each blank (domains), and rules about which combinations are legal (constraints). Once the problem has that shape, you can use algorithms that know about variables, instead of a generic tree search that does not.

### Need to know

**Local search.** You are given configurations `S` and a score `Eval(X)`. Find an `X*` that is best over all of `S`. For 8-queens, `Eval` is the number of attacking pairs, and the global solution is `Eval = 0` (a minimum). For VLSI layout, the configuration is where components sit and how wires run, and `Eval` mixes distance, unused area, and wire length.

Why not just list every configuration? There are too many, `Eval` may be expensive, and there is no fast exact method. You also often accept a very good configuration in place of the perfect one.

A **neighbourhood** `Neighbours(X)` is every configuration one move away. For queens, a move is "shift one queen to another row in its column" or similar. The neighbourhood is a design choice, and the algorithm's success depends on it. If the move is too small, you cannot escape a bad region. If the move is huge, "local" search is no longer local.

The loop is: start at `X0`, look at some neighbours, move to one of them, repeat until you are satisfied. At each step you can only see the neighbourhood, so you can only certify a **local** optimum: nothing one move away is better. A **global** optimum is better than everything in `S`, including configurations you have not visited. The whole difficulty is reaching a global optimum using only local moves.

**Hill climbing** always moves to the best neighbour, and stops when no neighbour is better:

```text
current = initial state
repeat:
    neighbour = best-valued neighbour of current
    if neighbour is not better than current:
        return current
    current = neighbour
```

It is greedy. It never steps downhill on purpose. Three landscapes explain the failures. Picture the score as height, and you are walking uphill.

- Local maximum: every neighbour is lower, but a taller peak exists somewhere else. You stop, wrongly convinced you are done. For a minimisation problem such as queens, the same trap is a local minimum: every neighbour has more attacks, but some distant board has zero.
- Plateau: a flat area where neighbours tie with you. A shoulder is a plateau that has an uphill exit if you are willing to walk sideways across the flat. A pure plateau may have no exit.
- Ridge: a rising line that your move set cannot follow. Every allowed step goes down the side of the ridge, so uphill moves cannot reach the top even though the top is "nearby" in a different sense.

8-queens numbers. State space `8^8`, about 17 million boards, if each column has one queen in one of eight rows.

- Steepest-ascent hill climbing from a random board succeeds on 14% of starts and gets stuck on 86%. When it works it takes about 4 steps. When it fails it takes about 3. So it is fast and usually wrong.
- Allow sideways moves, but cap them at 100 in a row so you do not wander a plateau forever. Success rises from 14% to 94%. Success now costs about 21 steps, and failure about 64. The slide mentions 8 shoulder states with `Eval = 12`. Sideways moves are how you leave a shoulder. The cap is how you refuse to loop on a flat plateau.

**Random-restart** hill climbing throws away a stuck board and starts from a new random board, until some climb hits the goal. If each climb succeeds with probability `p`, you expect `1/p` climbs (one success and the failures before it).

- No sideways moves: `p = 0.14`, so about `1/0.14`, roughly 7 climbs (1 success, 6 failures). Expected steps: `1*4 + (1/0.14 - 1)*3`, about 22.
- With the sideways cap: `p = 0.94`, expected climbs about 1.06, expected steps `1*21 + (1/0.94 - 1)*64`, about 25.

Read those two results together. Sideways moves make one climb much more reliable, so you rarely restart, but each climb is longer. Random restart without sideways moves fails often, but each failure is only 3 steps, so the total is still about 22 steps. Either way, 8-queens is easy for this family of methods, despite 17 million states.

**Stochastic** hill climbing does not take the best neighbour. It picks one of them at random. The slide says 1 of 56 neighbour states. You trade greed for a chance of not always walking into the same local optimum.

**Simulated annealing** is named in the outline and then the summary says it is not taught in this course. If an exam item mentions it, the expected fact is "a hill-climbing variant that sometimes accepts a worse move, not developed here." Do not invent a cooling schedule.

TSP (travelling salesman): a tour that visits each city once and returns. A 2-opt move deletes two edges and reconnects the tour. A 3-opt move deletes three. On the slides, 3-opt beats 2-opt, and 4-opt is not worth the extra time. Random restart helps. Quality is reported as percent above an estimated minimum cost, not only as "did we find the optimum?", because you often do not know the optimum.

The lecture's own moral: these algorithms are black boxes. What makes them work is the engineering you wrap around them: how you encode a state, what a neighbour is, what `Eval` rewards, and any extra hints. If a direct method exists (a formula, a CSP solver, A*), prefer it.

**CSPs.** In ordinary search the state is whatever data structure you like, as long as you can list successors and test the goal. In a CSP:

- Variables `X1, ..., Xn`.
- Each variable has a domain `Di` of allowed values.
- Constraints say which combinations of values are allowed.
- A solution is a **complete** assignment (every variable has a value) that is **consistent** (no constraint is broken).

Map colouring is the running example. Variables: WA, NT, Q, NSW, V, SA, T. Domain: `{red, green, blue}`. Constraint: regions that share a border get different colours. Tasmania does not border the others, so T is almost free. One solution on the slide: WA red, NT green, Q red, NSW green, V red, SA blue, T green. SA touches many regions, which is why it is hard. You will see SA again in the heuristics.

A **binary** CSP has only constraints on pairs. The **constraint graph** has a node per variable and an edge per binary constraint. Unary constraints (`SA != green`) involve one variable. Higher-order constraints involve three or more, such as a column in a cryptarithmetic puzzle.

Domain types:

- Finite discrete. `n` variables, domain size `d`, so `d^n` complete assignments. Boolean satisfiability is the famous NP-complete case.
- Infinite discrete, such as the start day of a job. You need a constraint language, for example `StartJob1 + 5 <= StartJob3`, because you cannot list the domain.
- Continuous, such as telescope observation times. Linear constraints on continuous variables can be solved by linear programming, in polynomial time.

Cryptarithmetic on the slide: letters `F, T, U, W, R, O` and carries `X1, X2, X3`, digits 0-9, all letters different, column addition constraints, `X3 = F`, and `F` and `T` not zero. You do not need to solve the puzzle. You need to see that a column constraint mentions several variables at once, so it is higher-order.

Real CSPs named: who teaches which class, timetabling, transport, factory scheduling. Many of those use real-valued variables.

**Formulation as search.** Start from the empty assignment. A successor assigns a value to one unassigned variable, and only if that value does not conflict with assignments already made. The goal test is "every variable is assigned." Every solution is at depth `n`, because you assign one variable per level, so depth-first search is a natural fit. The path does not matter: the order of decisions is not part of the answer. If at depth `l` you still had to choose both which variable and which value, branching would be `b = (n - l) * d`, and the tree would have `n! * d^n` leaves.

**Backtracking** uses a fact students skip: assignments are commutative. Colouring WA red and then NT green is the same state as the reverse order. So at each node you pick one variable and try its values. Branching drops to `b = d`, and there are `d^n` complete assignments to consider, not `n! * d^n`. Backtracking is depth-first search with that restriction. It is the basic uninformed CSP algorithm. The slides say it solves n-queens up to about `n = 25`.

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

The last lines are the "back" in backtracking. If a value leads every deeper attempt to failure, undo it and try the next value. If every value fails, return failure to the caller, who will undo their choice too.

Three heuristics, and you must know which one picks the variable and which one picks the value.

- **MRV**, minimum remaining values: choose the variable with the fewest legal values left. If SA has only one colour left and WA has three, colour SA now. If that one colour fails, you find out immediately, instead of after filling the easy variables. This is "fail first."
- **Degree heuristic**: only a tie-break for MRV. Among variables with the same number of remaining values, pick the one involved in the most constraints with other unassigned variables. It is the most entangled blank. Filling it tells you more about the rest.
- **LCV**, least constraining value: once the variable is chosen, try first the value that rules out the fewest options for the other variables. You want the current partial assignment to stay alive. MRV is pessimistic about variables (tackle the tight one). LCV is optimistic about values (try the gentle one).

The slides say MRV, degree, and LCV together make 1000-queens feasible. Plain backtracking stopped around 25.

**Forward checking** keeps, for every unassigned variable, the values that are still legal. When you assign WA red, delete red from NT's list. If any variable's list becomes empty, stop this branch now. You have proved failure without assigning the rest.

**Constraint propagation** keeps going after forward checking gives up. The slide's failure case: NT and SA both have only blue left, and they border each other. Forward checking may not notice until you assign one of them. Propagation notices that both cannot be blue.

**Arc consistency** is the simple version. The arc `X -> Y` (a directed pair) is consistent when every remaining value of `X` has at least one remaining value of `Y` that satisfies the constraint. If some `x` has no partner, delete `x`. If `X` loses a value, every neighbour of `X` must be checked again, because their options may have depended on the deleted value. Arc consistency detects failure earlier than forward checking. You can run it once before search, or after every assignment. AC-3 is the algorithm: put all arcs on a queue; pop `(X, Y)`; if revising `X` against `Y` deletes values, and `X`'s domain is now empty, fail; otherwise requeue arcs `(Z, X)` for neighbours `Z` other than `Y`.

**Min-conflicts** is local search for CSPs, not backtracking. Start with every variable assigned, even if constraints are broken. Repeatedly pick a variable that is currently in conflict, and set it to the value that violates the fewest constraints. The score is `h = number of violated constraints`, and you are hill-climbing downhill. For 4-queens, one queen per column gives `4^4 = 256` states. The slides say min-conflicts solves n-queens in almost constant time for arbitrary `n`, with high probability, including `n = 10,000,000`. That is a different regime from backtracking's `n` around 25.

**Structure.** If the constraint graph is several disconnected pieces, solve them separately. A tree-structured CSP (no loops in the constraint graph) can be solved in time linear in the number of variables. Two ways to get a tree are named: assign a small cutset of variables so the rest is a tree, or build a tree decomposition into overlapping subproblems. If you can split into subproblems of size `c`, the cost moves from `O(d^n)` toward `O(d^c * n/c)`. Independent subproblems are rare and worth finding.

### Memory hooks

- Path search asks "which sequence?" Local search asks "which picture at the end?"
- Hill climbing stops at the first peak it can see. Restart is "teleport and try again." Sideways moves cross a flat shoulder, with a cap so you do not live there.
- CSP solution: complete and consistent. Both words are required. A partial assignment can be consistent and still unfinished.
- MRV: most fragile variable first. Degree: if they are equally fragile, pick the busy one. LCV: gentlest value first.
- Arc `X -> Y`: "every x I might still use has some y that allows it."

### Check yourself

- Why is a queen board a local-search problem? **Answer.** Only the final placement matters. The sequence of moves is not part of the solution.
- What changes 14% success into 94%? **Answer.** Sideways moves, limited to 100 in a row.
- Variable heuristic or value heuristic? **Answer.** MRV and degree choose the variable. LCV chooses the value.
- When is an arc consistent? **Answer.** For every remaining value of the tail, some remaining value of the head is allowed.

---

## Lecture 5: Machine learning basics

No set textbook pages on the title slide. Lab week 5 matches this lecture.

### How to picture it

Search needed you to write the goal and the rules. Learning is for the problems where you cannot write the rule, but you can show examples. A bank cannot write a perfect formula for "will default", but it has a filing cabinet of past loans and what happened. The hypothesis is the rule the algorithm proposes after reading the cabinet.

### Need to know

The slide definition: machine learning is programming a computer to optimise a performance criterion using example data or past experience. Arthur Samuel used the phrase in the early 1960s. Use learning when human expertise does not exist (navigating Mars), cannot be explained (speech), changes over time (network routing), or must be tuned per person (biometrics). Do not use learning for payroll. The rule is already known exactly, and a learned approximation would be worse.

Notation, and the superscript is an index, not a power:

- `xi` is the input, also called the feature vector. For a house, living area.
- `yi` is the target, the thing you want to predict. For a house, price.
- `(xi, yi)` is one training example.
- `h` is the hypothesis, a function from inputs `X` to outputs `Y`. "Good" means it predicts `y` well, including on examples it did not train on.

**Supervised** learning: every training row has both `x` and `y`. You are learning a mapping.

- **Regression**: `y` is a continuous number. Price, age, kilowatt-hours. The word "continuous" means the output lives on a scale where 209.4 is meaningful, not a category name.
- **Classification**: `y` is a discrete label. Binary classification uses two labels, often 1 and 0, or +1 and -1. "Sells above the asking price" is classification even if the underlying price is a number. Changing the question changes the task. Predicting the price is regression. Predicting "above asking, yes or no" is classification. Predicting age from a photo is regression. Predicting "old enough to vote in Australia" is classification. A loan decision is classification.

**k-nearest neighbour** classifies a new point as the majority class among the `k` closest training points. With `k = 1` you copy the single nearest neighbour. That is fragile: one oddly labelled point near the query steals the decision. The rain slides show a white point called "rain" by 1-NN and a different label by 5-NN, because the larger vote outnumbers the one odd neighbour. Distance is usually Euclidean unless the lab says otherwise. k-NN does almost no work at training time. It stores the points and works at prediction time. That is why it is called lazy.

A linear classifier instead draws one straight cut, `a*x + b*y + c = 0`, and calls one side positive. It cannot represent a rule that needs a bend. Week 6 and week 7 exist because of that limit.

Classification uses named on the slides: face recognition (pose, light, glasses), handwriting, speech (time matters), diagnosis from symptoms, biometrics, and outlier detection such as network attacks. MNIST: 60,000 training digit images, 10,000 test images. A 2016 number on the slide is about 0.21% error from an ensemble of five convolutional nets. You are not examined on CNN internals here. The point is that classification includes images, and that test-set error is how you report it.

What a learned rule is for: predict a new case, state a rule a person can read, compress the data into something simpler, or flag outliers (fraud) that the rule does not cover.

**Unsupervised** learning has inputs and no `y`. There is no teacher. You are looking for what normally happens. Clustering groups similar rows. The essay example: 1000 essays, group them by word frequency, sentence length, and so on, without being told the group titles. The cocktail-party example is structure finding that is not clustering: separate voices from a mixed recording. Association rules find co-occurrence, such as `{onions, potatoes} => {burger}` in basket data, or symptom groups in medicine. The slides note that some sources, including a Wikipedia remark on the slide, class association rules as supervised. In this course, treat them as the unsupervised bullet unless a question quotes that caveat.

**Semi-supervised** learning has a few labelled rows and a large unlabelled pile. Labelling is expensive (a doctor's time). Raw data is cheap (MRI files). Pseudo-labelling, also called self-training: train on the labelled rows, predict the unlabelled rows, keep only the confident predictions, add them as if they were labels, and train again. Uses: medical images, speech transcripts, web-page categories.

**Reinforcement learning**, previewed here and formalised in week 11. No input-output pairs. An agent takes actions, the environment returns a reward, often late, and the agent wants more total reward. The **credit-assignment problem** is that the tip at the end of a taxi ride does not say which earlier turn caused it. The loop words: state `S`, action `A`, reward `R`, policy `pi` (the map from states to actions). Algorithms named in this lecture, before the detail arrives: temporal difference, Q-learning, and deep adversarial networks. RLHF is the later slide: a reward model trained on human preferences, then a policy optimiser such as PPO or GRPO, used to steer a language model. Most of that acronym list is context. The examinable core is agent, delayed reward, and policy.

**Evaluation** is where students lose marks by using the training score as if it were the truth.

Learning searches a space of hypotheses for a good `h`. A hypothesis **generalises** if it predicts `y` on a test set that was not used for training. A **consistent** hypothesis matches every training pair. Two different polynomials can both pass through the same dots. Consistency is not the same as "best."

**Ockham's razor**: among consistent hypotheses, prefer the one with fewer assumptions. William of Ockham, 14th century. A degree-1 polynomial that fits is preferred to a degree-12 polynomial that also fits, if both are consistent. Often you cannot be consistent and simple at the same time. A wiggly curve hits every noisy point and then fails on the next point. A smoother curve misses a few training points and predicts the next one better. That miss-on-purpose is the bias you accept to reduce variance.

**Overfitting**: the model has fitted this particular data set, including its noise, so closely that it fails on future data. If the model has as many degrees of freedom as there are points, it can fit perfectly and still be useless.

Dietterich's triple tradeoff. Three quantities move together:

1. `c(H)`, how rich the hypothesis space is.
2. `N`, how many training examples you have.
3. `E`, generalisation error on new data.

As `N` grows, `E` tends to fall. As `c(H)` grows, `E` first falls (the model becomes able to represent the truth) and then rises (the model becomes able to memorise noise).

The split that estimates `E` honestly:

- Training set, about 60-80%. The only rows used to set the model's parameters.
- Validation set, about 10-20%. Used to choose hyperparameters (learning rate, tree depth, `k`). Not used to fit the parameters.
- Test set, about 10-20%. Used once, at the end, to report error. If you peek and then change the model, it is no longer a test set.

If you have too few rows for three piles, resample (week 8's k-fold is the method).

**Bias and variance**, in the slide's wording. High bias: the model is consistently wrong in the same way. A straight line fit to a U-shape always misses the bend. The errors are stable across training sets. High variance: the model is right on average but jumps around when the training set changes. A very flexible curve redraws itself around whichever points you happened to sample. You want both small. You usually buy a reduction in one by accepting a bit of the other.

Loss functions, the score of "how wrong":

- 0-1 loss: 0 if the label matches, 1 otherwise. It counts mistakes. It does not say whether you were close.
- L1 loss: absolute error `|actual - predicted|`.
- L2 loss: squared error `(actual - predicted)^2`. Big mistakes dominate, because a error of 10 contributes 100.

### Lab week 5

Classify the scenario before you name an algorithm.

1. Income, credit score, employment, loan amount, and a known default or not: supervised classification. The label is a category.
2. Viewing behaviour, no predefined viewer types: unsupervised clustering. The groups are discovered.
3. Adjust CPU and memory, get response time and energy back, try to improve the total: reinforcement learning. Actions, delayed-style feedback, no labelled pairs.
4. A few clinician-labelled records plus many unlabelled records: semi-supervised. The labels anchor the categories. The unlabelled mass fills in the shape.
5. Temperature, occupants, time of day, day of week, and energy in kWh: supervised regression. The target is a number.

For the energy problem, one row is one observation. Features: outdoor temperature, number of occupants, time of day, day of week. Target: kWh. Time and day are periodic. Encoding Sunday as 7 and Monday as 1 makes them look far apart numerically when they are neighbours on the week. A real model would use categories or a cyclical encoding. The lab still treats the idea as "these columns are inputs."

The fitted line in the solution is `energy = 302.26 - 6.19 * temperature`.

At 15 degrees C: `302.26 - 6.19 * 15 = 302.26 - 92.85 = 209.41` kWh. The intercept, 302.26, is the prediction at 0 degrees C. It is a baseline, not "energy with no temperature." The slope, -6.19, means each extra degree is associated with about 6.19 kWh less. That fits a building that is mostly heating: warmer outside, less heating. Check the printed predictions: 10 degrees gives 240.4, 20 gives 178.5, 30 gives 116.7. The gap from 10 to 20 equals the gap from 20 to 30. Equal input steps, equal output steps. That is what "linear" means.

`R^2 = 0.948` means 94.8% of the variation in the **training** energy values is tracked by the line. The other 5.2% is unexplained. `R^2` does not measure a future month. A model can score 0.95 on the months it was fit to and then fail in deployment. That failure is overfitting: it has absorbed a cold winter or a construction period that will not repeat.

The deeper modelling point: real buildings use energy at both extremes. Cold means heating. Hot means cooling. Mild (around 18 to 22 degrees) means neither. The true curve is U-shaped. A straight line can follow only one arm. If the data include hot days, the line underestimates both extremes and overestimates mild days. Fixes named in the solution: polynomial regression, a piecewise line, or features such as heating degree days and cooling degree days separately.

### Memory hooks

- "Category or number?" decides classification or regression. The same spreadsheet can be either, depending on the column you call `y`.
- k in k-NN: more neighbours, more voting, less trust in one odd point.
- Ockham: simpler story if it still explains the data.
- Overfit: great on the homework, lost on the exam.
- Bias: always bent the same wrong way. Variance: a different wrong shape every time you resample.

### Check yourself

- Turn house-price regression into classification. **Answer.** Predict "sells above the asking price" instead of the price.
- What does a larger `k` do? **Answer.** The vote includes more neighbours, so one nearby outlier matters less. Too large, and you average in points that are not really similar.
- Define consistent, Ockham, overfitting. **Answer.** Consistent: matches every training pair. Ockham: prefer the simpler consistent hypothesis. Overfitting: matches this sample, including noise, and fails on new data.
- What does training `R^2` not say? **Answer.** How the model will do on days it was not fit to.

---

## Lecture 6: Linear models

Lab week 6 matches this lecture.

### How to picture it

A linear model is a weighted sum. Each feature pulls the prediction up or down in proportion to its value. Learning is the search for those weights. The three models in this lecture share the weighted sum and differ in what they do with it: emit the sum (regression), squash it into a probability (logistic regression), or threshold it into a hard yes or no (perceptron).

### Need to know

The line `2x + 3y - 12 = 0` cuts the plane into two sides: where the expression is positive and where it is negative. With several inputs the regression form is

`y = w1*x1 + w2*x2 + ... + wn*xn + b = <w, x> + b`.

`w` holds the weights, `x` holds the features, `b` is the bias (the intercept). The angle brackets mean the dot product: multiply matching pairs and add. House features on the slide: beds, baths, garage, land area. A positive weight means "more of this feature, higher predicted price," if the other features stay put.

You can hide `b` inside the dot product. Append a 1 to the feature vector and append `b` to the weight vector. Then `y = x w` as a matrix product. Do this when you see the closed-form solution, because that formula has no separate `b`.

**L2 loss** on one example is `(y - y_hat)^2`. An error of 2 costs 4. An error of 10 costs 100. Large mistakes dominate, and a single wild outlier can drag the line. **MSE** (mean squared error) averages that over `n` examples:

`l = (1/n) * sum (yi - <xi, w> - b)^2`.

Training picks `w*` and `b*` to minimise `l`. The **gradient** is the vector of partial derivatives. It points uphill, toward higher loss. Gradient descent walks the opposite way.

For this particular loss the surface is a bowl (convex): one bottom, no bad local valleys. With the bias folded into `w`, the bottom has a formula:

`w* = (X^T X)^(-1) X^T y`.

`X` is the matrix of all training inputs, `y` is the column of targets. This is the normal equation. It is exact for linear regression and a bad idea when `X` is huge, because inverting `X^T X` is expensive and numerically fragile. Logistic regression and neural nets do not have this closed form. They use gradient descent:

`w_t = w_(t-1) - eta * (partial l / partial w)`.

`eta` is the learning rate, the step length.

- Too small: you walk downhill correctly and arrive late, or appear stuck.
- Too large: you step over the bottom and the loss jumps or diverges.

**Full gradient descent** computes the gradient on every training row, then steps once. **SGD** (stochastic gradient descent) computes it on a mini-batch of `b` random rows. The slide's `b` here is batch size, not the search branching factor. A tiny batch is a noisy estimate of the true gradient, and it may not fill the hardware. A huge batch costs memory and wastes work if the rows are redundant. The slide's usual range is 32 to 512, depending on the machine.

**Linear classification.** A decision boundary is the set of points where the model is indifferent. For a linear model that set is a line in 2D and a hyperplane in higher dimensions. The seismic example separates earthquakes and explosions. The equation line on the slide is `1.7*x1 - x2 - 4.7 = 0`. The weight vector printed beside it is `(-4.9, 1.7, 1)`, which does not match -4.7. If a question gives a figure, use the figure. The decision rule is: predict class 1 when `w . x >= 0`, else 0. That is a hard threshold. There is no "maybe."

**The perceptron** (Rosenblatt, 1957) is that idea as a learning rule. Inputs are features, each with a weight, plus a bias feature `x0 = 1`. The weighted sum is passed through a sign function. One slide uses +1 and -1: output +1 if the sum is at least 0, else -1. Another uses 1 and 0. Read the question's labels before you update.

The step function is flat everywhere except at 0, where the derivative is undefined. Gradient descent has nothing to follow. The perceptron uses a hand-written update instead, and only when the prediction is wrong. If the prediction is correct, the weights stay put.

Lecture form, labels the true class `y`:

`wi <- wi + alpha * (y - h_w(x)) * xi`.

`alpha` is the learning rate. For +1/-1 labels the slides also write `w' = w + y * x` when the point is misclassified: add the feature vector if a positive point was called negative (you need the dot product to rise), and subtract it if a negative point was called positive (you need the dot product to fall). Those are the same direction. The factor in front differs: `(y - h)` is 2 or -2 for +1/-1 labels when you are wrong, while `w + y*x` uses a step of size 1. The lab uses 0/1 labels and keeps `alpha` explicit:

`w <- w + alpha * (y - y_hat) * x`.

Work one case so the sign is obvious. Truth `y = 1`, prediction 0, so `(y - y_hat)` is positive, so you add a portion of `x` to `w`. The next dot product `w . x` is larger, so the score moves toward the positive side. If truth is 0 and you predicted 1, `(y - y_hat)` is negative, so you subtract a portion of `x`, and the score falls.

**Perceptron convergence theorem.** If the training set is linearly separable, the algorithm reaches some separating weights after a finite number of updates. Linearly separable means a hyperplane exists with every positive point on one side and every negative point on the other. In 2D, you can draw one straight line between the classes.

What the theorem does not say:

- It does not promise one pass (one epoch) is enough.
- It does not promise a unique separator, or the "best" one. Any separating line counts.
- If the data are not separable, it need not stop. The weights can cycle forever.

XOR is the standard inseparable pattern: `(0,0)` and `(1,1)` in one class, `(0,1)` and `(1,0)` in the other. No straight line separates them. Minsky and Papert (1969) used this to show the single perceptron's limit. That limit is why week 7 adds a hidden layer.

**Logistic regression** keeps the linear score `z = w . x + b` and passes it through the sigmoid

`sigmoid(z) = 1 / (1 + e^(-z))`.

Any real `z` becomes a number strictly between 0 and 1. Large positive `z` goes toward 1. Large negative `z` goes toward 0. `z = 0` gives 0.5. You read the output as `P(y = 1 | x)`. The usual decision is: class 1 if the probability is at least 0.5, which is exactly when `z >= 0`. So the boundary is still the same straight cut as a perceptron. What changed is the training signal and the confidence. An output of 0.51 and an output of 0.99 are both "class 1", and they are not the same belief.

The loss is binary cross-entropy, not squared error. Training is gradient descent. The sigmoid is smooth, so a gradient exists. The perceptron step does not have one.

**Softmax regression** is the multi-class version. One linear score per class. Softmax turns the scores into positive numbers that sum to 1, so they can be read as class probabilities. The predicted class is the argmax, the class with the largest score. The loss is cross-entropy: it is small when the probability on the true class is near 1. Examples on the slides: MNIST has 10 digit classes, ImageNet has 1000, a protein image task has 28, a malware task has 9. Squared error is the natural loss when there is one continuous target. It is a poor match when you need a confident pick among many classes.

The summary slide also lists Huber regression as "linear function plus an activation," without a formula. Know the name sits with the robust-regression family. Do not invent the threshold.

### Lab week 6

|  | Linear regression | Logistic regression | Perceptron |
| --- | --- | --- | --- |
| Output | Any real number | Probability in (0, 1) | Hard +1/-1 or 1/0 |
| Boundary | Not a classifier | Linear | Linear |
| Training | MSE, closed form or gradient descent | Cross-entropy and gradient descent | Update only on mistakes |
| If the classes need a bend | Wrong tool | Still only a straight cut | Does not converge |

Lab trace. Labels are 0 and 1. Learning rate `alpha = 0.5`. The third weight is the bias, and `x3` is always 1. Learning starts at weights `[0, 0, -1]`.

- `[1, 1, 1]`, truth 0. Score `0*1 + 0*1 + (-1)*1 = -1`. Predict 0. Correct. Weights stay `[0, 0, -1]`.
- `[3, 2, 1]`, truth 1. Score `-1`. Predict 0. Wrong. Add `0.5 * (1 - 0) * [3, 2, 1]`. Weights become `[1.5, 1, -0.5]`.
- `[2, 4, 1]`, truth 1. Score `1.5*2 + 1*4 + (-0.5)*1 = 6.5`. Predict 1. Correct. No change.
- `[3, 4, 1]`, truth 1. Score `1.5*3 + 4 - 0.5 = 8`. Predict 1. Correct. No change.
- `[2, 3, 1]`, truth 0. Score `1.5*2 + 1*3 - 0.5 = 5.5`. Predict 1. Wrong. Add `0.5 * (0 - 1) * [2, 3, 1]`, which subtracts `[1, 1.5, 0.5]`. Weights become `[0.5, -0.5, -1]`.

A separate check with those final weights on the five points gets only 2 right (points 2, 3, and 4 still wrong). One epoch was not enough. The theorem still applies if the movies are separable: more passes will reach a separator. It will not tell you which separator, and it will not help if they are not separable.

The lab's comparison of the update with logistic gradient descent: the perceptron applies a fixed-direction kick when wrong, and the size does not grow with "how negative" the score was. A score of -0.01 and a score of -100 can trigger the same perceptron update. Gradient descent on cross-entropy scales the step by the gradient, so a very wrong probability moves the weights more than a slightly wrong one.

### Memory hooks

- Same dot product, three heads: raw number, sigmoid probability, hard threshold.
- Perceptron: "only kick the weights when you are wrong, and kick them along `x`."
- Convergence: "separable means it will stop sometime, not on the first lap, and not on the prettiest line."
- XOR: opposite corners, no straight cut, one layer is not enough.

### Check yourself

- Write the MSE gradient step and say what a huge `eta` does. **Answer.** `w <- w - eta * gradient`. A huge `eta` steps past the minimum. The loss oscillates or blows up.
- One perceptron update, truth +1, you predicted -1. **Answer.** Add a positive multiple of the feature vector so the next dot product is higher.
- What does the theorem refuse to promise? **Answer.** One epoch, uniqueness, optimality among separators, and any result at all when the data are not separable.
- What does the sigmoid add? **Answer.** A probability in (0, 1) and a derivative, so gradient descent can train the same linear boundary.

---

## Lecture 7: Feed-forward neural networks

Reading: AIMA section 21.1. Lab week 7 is the hand calculation. Lab week 8 codes XOR.

### How to picture it

A perceptron draws one straight cut. XOR needs two cuts, or equivalently a bend. A hidden layer builds new features that are combinations of the inputs. A second layer then draws a straight cut in that new feature space. The bend appears in the original space. The non-linearity is the whole trick. Without it, two linear layers multiply into one linear layer, and you are back to a perceptron with more arithmetic.

### Need to know

A single perceptron computes `o = sigma(<w, x> + b)` where `sigma(x) = 1` if `x > 0` and `0` otherwise. The output is a class, not a probability and not a regression value. The update `wi <- wi + alpha * (y - h(x)) * xi` is SGD with batch size 1 on that particular loss. XOR is not linearly separable: targets 0, 1, 1, 0 on inputs `(0,0), (1,0), (0,1), (1,1)`. One perceptron cannot learn it. That negative result is Minsky and Papert, 1969, already flagged in week 6.

A **multi-layer perceptron** (MLP) is a feed-forward net: information moves from input layer to hidden layers to output layer, with no cycles. In this lecture every unit in one layer connects to every unit in the next (fully connected). You choose two hyperparameters before training: how many hidden layers, and how wide each one is.

Forward pass for one hidden layer. `x` is the input column. `W1` maps inputs to hidden units. `b1` is one bias per hidden unit. `sigma` is a non-linear activation, applied element by element.

`h = sigma(W1 x + b1)`

`o = W2 h + b2`

The first formula line on the architecture slide writes `W2 x` for the output. The surrounding text says `W2` maps the hidden layer, so the product is with `h`, not with `x`. Use `h`. For several classes, `y = softmax(o)`. The output layer is sometimes left linear (no activation), which is what the regression-style lab does.

**Back-propagation** is gradient descent plus the chain rule, organised layer by layer so you do not rewrite the derivative from scratch for every weight. For each training example you want the network's output closer to the target. Steps:

1. Initialise weights to random numbers in `[-1, 1]`. Random, not identical. Lab week 8 explains why.
2. Forward pass: compute every hidden activation and the output.
3. Backward pass: start from the output error and send a share of the blame back to each weight that helped cause it.
4. Stop after a set number of iterations, or when an error measure such as RMS is small enough. Test on held-out data while you train, so you notice overfitting. Week 8 turns that advice into early stopping.

One unit, in words: take the outputs of the previous layer, multiply by this unit's weights, add the bias, then apply `f`. The thing inside `f` is the pre-activation, often called `z`. The thing after `f` is the activation.

**Sigmoid backprop**, the version the lecture derives by hand. Sigmoid output `y = 1 / (1 + exp(-z))` lies in `(0, 1)`. Its derivative is `y * (1 - y)`, which you can compute from the output you already stored. The largest value of `y(1-y)` is 0.25, at `y = 0.5`. Near 0 or near 1 the derivative is near 0. A saturated sigmoid unit almost stops learning. Stack several of them and the early layers receive a gradient that has been multiplied by 0.25 or less at every stage. That is the vanishing gradient.

Weight update: `wij = wij + eta * delta_j * yi`, with learning rate `0 < eta < 1`. Here `yi` is the activation that flowed into this weight (the previous layer's output), and `delta_j` is the error term at the unit on the far side.

- Output unit: `delta_j = yj * (1 - yj) * (zj - yj)`. `yj` is the sigmoid output. `zj` is the target. `(zj - yj)` is "how far below the target am I?", and `yj(1-yj)` gates it by how sensitive the sigmoid is there.
- Hidden unit: there is no target for a hidden unit. Its delta is the sigmoid gate times a weighted sum of the deltas it feeds: `delta_j = yj * (1 - yj) * sum_k (delta_k * w_jk)`. Blame is inherited from the units downstream.

The slides say to store outputs and deltas, and to be careful about using updated outgoing weights in the hidden-unit sum. Deltas depend on the weights from the forward pass. Compute the deltas first, then change the weights. If you overwrite weights while you are still sending error backward, the later deltas use a mix of old and new weights.

Squared error for a small net is often written with a `1/2`:

`L2 = [(y1 - y_hat1)^2 + (y2 - y_hat2)^2] / 2`.

The `1/2` cancels the 2 from differentiating a square, so the derivative with respect to the prediction is simply `(prediction - target)` or the reverse, depending on which way you subtract. It does not change which network is best. It changes the scale of the gradient, which you could also have absorbed into `eta`.

Chain rule, the one calculus fact the course actually uses: if the loss depends on `y` and `y` depends on `x`, then `d(loss)/dx = d(loss)/dy * dy/dx`. Backprop is that sentence applied at every layer, from the loss backward to the first weight.

Worked sigmoid values on the slide, so you recognise the arithmetic:

- Weighted sum `-0.3` gives `1 / (1 + exp(0.3)) = 0.574`.
- Weighted sum `-0.1` gives `1 / (1 + exp(0.1)) = 0.525`.
- Weighted sum `0.11` gives `1 / (1 + exp(-0.11)) = 0.527`.

Notice `exp(-z)` in the sigmoid. If `z` is negative, you negate it again and the exponent becomes positive. Students drop that sign and get a number on the wrong side of 0.5.

Picking `eta`: try values spaced by factors, not by 0.001. Find one that is clearly too small (loss falls, very slowly, smooth) and one that is clearly too large (loss oscillates or diverges). Search between them. A schedule that shrinks `eta` over time is mentioned as an optional extra.

Stopping: iteration count, or RMS error. RMS is the square root of the average squared difference between desired outputs `dij` and network outputs `oij`, over training pairs `i` and output units `j`. The slide's formula graphic does not survive text extraction cleanly. If a question prints the formula, use the printed one. The idea is "typical size of the output error."

**Momentum** (Rumelhart et al., 1986) adds a fraction of the previous weight change:

`wij(t+1) = wij(t) + eta * delta_j * xi + eta * (wij(t) - wij(t-1))`.

If the last few updates all pointed the same way, momentum keeps going. That speeds travel across a gentle slope and dampens zigzag. The slide claims faster and more stable training.

Another named variant (Hirose, Yamashita, and Hijiya): if training is stuck in a local minimum, add a hidden unit. The loss surface changes shape, so the old trap may no longer be a trap. They showed it on XOR and on 8x8 character fonts.

The voice demo is a fully connected net: 60 inputs (frequency bins), 6 hidden units, 2 outputs (one-hot for "Steve" versus "David"). Training is a sweep: present a pair, compute error, backpropagate, adjust weights, repeat for every pair, then repeat the sweep. Applications listed, as a catalogue rather than as algorithms: characters, faces, sonar mine versus rock, driving a car, stocks, NETtalk pronunciation.

### Lab week 7

Hand calculation with **ReLU** in the hidden layer, not sigmoid. `ReLU(z) = max(0, z)`. Positive pre-activations pass through. Negative ones become 0. The derivative is 1 when `z > 0` and 0 when `z < 0`. At 0 the derivative is conventionally taken as 0 in this lab.

Input `(0.5, -0.5)`. Target `y = 1`.

- Hidden unit 1: `z1 = 1.0*0.5 + 0.5*(-0.5) + 0.5 = 0.75`. `a1 = ReLU(0.75) = 0.75`.
- Hidden unit 2: `z2 = -1.0*0.5 + 2.0*(-0.5) - 0.5 = -2`. `a2 = ReLU(-2) = 0`.
- Output, linear: `o = 1.5*0.75 + (-1.0)*0 + 0.5 = 1.625`.
- Half squared loss: `L = 0.5 * (1.625 - 1)^2 = 0.5 * 0.390625 = 0.1953125`.

The network overshot the target by 0.625. With `eta = 0.1` and a provided gradient of `0.46875` on two weights: `1.5 - 0.1*0.46875 = 1.453125`, and `1.0 - 0.1*0.46875 = 0.953125`. Both gradients were positive, so both weights decrease. Positive gradient means "increasing this weight increases the loss." Descent subtracts.

**Dying ReLU.** Unit 2 output 0 and its ReLU derivative is 0, so the entire gradient through unit 2 is multiplied by 0. Its weights do not move on this example. If every training example drives `z2` negative, unit 2 never moves again. It is dead. Leaky ReLU and ELU keep a small slope for negative `z`, so a dead-looking unit can still receive a gradient.

### Lab week 8

This lab is still Lecture 7. It trains XOR. It does not implement dropout or weight decay.

Architecture: 2 inputs, 4 hidden sigmoid units, 1 sigmoid output. Rows: `[0,0] -> 0`, `[0,1] -> 1`, `[1,0] -> 1`, `[1,1] -> 0`.

Shapes, which are the usual bug:

- `X` is `(4, 2)`: 4 examples, 2 features.
- `W1` is `(2, 4)`, `b1` is `(1, 4)`.
- `Z1 = X @ W1 + b1` is `(4, 4)`. The bias broadcasts across the 4 rows.
- `W2` is `(4, 1)`, `b2` is `(1, 1)`.
- `Z2` is `(4, 1)`: one prediction per example.

If `W1` were `(4, 2)`, the inner dimensions of `(4, 2) @ (4, 2)` would not match, and NumPy would throw. Check shapes before you train.

**Symmetry.** If every weight starts at the same value, every hidden unit computes the same function and receives the same gradient. Extra units buy nothing. Draw `W1` from uniform random values in `[-1, 1]` so the units can specialise. Biases may start at 0. Each unit has its own bias, so equal biases do not force equal gradients once the weights differ.

Sigmoid facts to be able to say out loud: `sigmoid(0) = 0.5`. `sigmoid(10)` is about 0.99995, not 1. `sigmoid(-10)` is about 0.000045, not 0. Derivative `s*(1-s)` is largest at 0.25. Each sigmoid layer multiplies the gradient by at most 1/4. Deep stacks of sigmoids starve the first layer. That is vanishing gradient, in numbers.

Loss: `mean(0.5 * (A2 - y)^2)`. The 1/2 makes the derivative `(A2 - y)`. Binary cross-entropy is the more standard loss for a probability. MSE is used because the lab treats the target as a number in `{0, 1}` and wants a simple derivative. It is enough for four XOR rows.

Autograd: `grad(compute_loss)` returns a function that, given the parameters, returns `[dW1, db1, dW2, db2]` with the same shapes. `compute_loss` must be pure. If you subtract from `W1` inside it, the trace of operations is corrupted. Update in the training loop: `param -= learning_rate * grad`. This XOR net has `2*4 + 4 + 4*1 + 1 = 17` parameters. A net with `784*30 + 30 + 30*10 + 10 = 23860` parameters is the lab's illustration that you will not derive those gradients on paper. Autograd is the same two lines either way.

With 4 hidden units the net does learn XOR. Final predictions are about 0.03, 0.97, 0.97, 0.03. Threshold 0.5 recovers the four labels. A healthy curve at learning rate 0.5 falls quickly, then flattens, and does not spike. Flat from the start: `eta` too small, a bad init, or a gradient bug (often a sign error). Oscillating or rising loss: `eta` too large. A plateau well above zero: local minimum, or not enough hidden units. `NaN`: overflow, often a huge learning rate or a loss that forgot a factor and exploded the gradient.

### Memory hooks

- "Linear plus linear is linear." The hidden activation has to bend.
- Sigmoid derivative: `y(1-y)`. Biggest at one quarter, tiny at the extremes.
- ReLU: negative in, zero out, zero gradient, can die.
- Backprop: forward to predict, backward to assign blame, then step.
- Shapes: `(examples, features) @ (features, units) = (examples, units)`.

### Check yourself

- Why a hidden layer is useless if it is linear. **Answer.** The product of weight matrices is one weight matrix. The net collapses to a single perceptron.
- `sigmoid` output 0.8. What is the local derivative factor? **Answer.** `0.8 * 0.2 = 0.16`.
- When does ReLU kill a unit? **Answer.** When the pre-activation stays negative, output and gradient stay 0, and the weights never move.
- `W1` shape for 2 inputs and 4 hidden units, if `X` is `(n, 2)`? **Answer.** `(2, 4)`.

---

## Lecture 8: Model selection and regularisation

The week 8 lab trains the XOR net. It does not cover this lecture. Study the slides for the theory.

### How to picture it

You can always drive training error to zero by making the model flexible enough to memorise. The loan story is the warning. Among 100 applicants, 5 defaulted, and all 5 happened to wear a blue shirt at the interview. A flexible model will treat "blue shirt" as a strong rule. Training error looks brilliant. The next applicant in a blue shirt is not a higher risk. Week 5 called this overfitting. This lecture is the toolkit for noticing it and for constraining the model so it is less eager to memorise.

### Need to know

Four errors, and they are different datasets:

- **Training error**: on the rows used to fit weights. Optimistic if you report it as performance.
- **Validation error**: on rows used to make choices (learning rate, width, when to stop). A common recipe is to hold out about 10% of the training pool and never fit on it.
- **Generalisation error**: on new data the model will actually see.
- **Test error**: on a set you touch once. A future exam, a house price you have not seen, a Kaggle private leaderboard. If you tune after seeing the test score, you have used the test set as a validation set, and the number is no longer an honest estimate.

Do not mix validation rows back into the fit and then quote the validation score. That is the slide's "mistake number 1." The week 5 split remains: train about 60-80%, validation about 10-20%, test about 10-20%.

**K-fold cross-validation**, for when the pool is too small to spare a permanent validation set. Split the training pool into `K` blocks. For each block `i`, train on the other blocks and score block `i`. Report the average of the `K` scores. Usual `K` is 5 or 10. Every row is used for validation once, and for training `K-1` times. You pay for that with `K` training runs. The test set, if you have one, stays outside the folds.

**Underfitting**: training error is high, so test error is high too. The model cannot represent the pattern. A straight line on a U-shape. The fix is more capacity, better features, or training longer if you simply have not fit yet.

**Overfitting**: training error is low, test error is high. The model has capacity to spare and has used it on noise. The blue shirt.

**Capacity** is the variety of functions the model family can represent. Low capacity struggles to fit the training set. High capacity can memorise it. Inside one family, capacity grows with the number of parameters and with how large those parameters are allowed to be. Across families, a parameter count is a bad comparison: a decision tree and a neural net with the same number of numbers are not the same capacity. A linear model with `d` inputs has `d + 1` parameters including bias. A one-hidden-layer net with `m` hidden units and `k` outputs has `(d+1)*m + (m+1)*k` parameters, counting biases. That expression is on the slide as a way to estimate size inside the neural-net family.

**VC dimension** is the theoretical measure. For a classifier family, it is the size of the largest set of points the family can shatter: for every possible way of labelling those points, some model in the family classifies them perfectly. A 2D perceptron has VC dimension 3. Any 3 points (not on a pathological line) can be separated for every labelling. Four points arranged as XOR cannot. A perceptron with `N` parameters has VC dimension `N`. Some MLPs have VC dimension `O(N log2 N)`. VC dimension can bound the gap between training error and generalisation error. The slides say the bounds are too loose for deep nets, and that you rarely compute VC dimension in practice. Know the definition and the perceptron number 3. Do not pretend you use it to pick a learning rate.

Data complexity is not just "how many rows." It also includes how many elements sit in each row, whether there is time or space structure, and how diverse the rows are. A million near-duplicate photos are less informative than a thousand different ones.

**Regularisation** means any technique that limits effective complexity so the model is less free to overfit. Four from the slides:

**Early stopping.** After each epoch, or every few epochs, measure validation loss. Early on, both training loss and validation loss fall: the model is learning structure that exists in both sets. Later, training loss keeps falling and validation loss flattens, then rises: the extra fit is specific to the training rows. Keep the weights from the epoch with the best validation score. **Patience** is how long you wait after that best epoch before you give up, for example 10 epochs with no improvement, then restore the saved weights. You need a validation set. Watching only training loss cannot tell you the turning point.

**Data augmentation.** Make new training rows by modifying real ones in ways that should not change the label. You are not collecting new data. Images: rotate, crop, flip horizontally, zoom, change brightness, contrast, or colour, add slight noise, cut out a patch. Text: swap a synonym, translate to another language and back, delete or swap a random word. Audio: shift pitch, add background noise, stretch time. The label stays "this is a cat" because a flipped cat is still a cat. Do not augment in a way that changes the label (flipping a "6" into a "9").

**Weight decay.** Prefer smaller weights. A model with huge weights can make sharp, brittle decisions that fit noise.

- Hard form: minimise the loss subject to `||w||^2 <= theta`. A smaller `theta` is a tighter box, so stronger regularisation. The bias is often left out of the penalty. The slide says including it or not rarely matters in practice.
- Soft form: add `(lambda / 2) * ||w||^2` to the loss and minimise the sum with no hard box. `lambda = 0` means no penalty. As `lambda` goes to infinity, the best weights go to 0 (the model ignores the features). The gradient of the penalty is `lambda * w`, so the update is

`w <- (1 - eta*lambda) * w - eta * (data-loss gradient)`,

provided `eta*lambda < 1`. Each step multiplies the old weight by a number slightly below 1. That is why it is called decay, not only "penalty." The claimed benefit: the model cannot put a huge weight on one accidental feature, such as the blue shirt, unless that feature really reduces training loss enough to pay the penalty.

**Dropout.** During training, ignore a random subset of units on each step (their outputs treated as zero). A hidden unit cannot rely on one specific partner always being present, so features have to be individually useful. Typical rates on the slide: 0.2 to 0.5 for hidden layers, about 0.1 for the input layer. The motivation given: a good model should tolerate modest damage to its input, and dropout injects that kind of noise inside the net. At test time you use the full net (standard practice; the slide focuses on the training noise).

**Residual connections are not regularisation.** Say that explicitly if asked. Regularisation targets generalisation. A residual connection targets optimisation: very deep nets are hard to train because the gradient has a long path. In a plain feed-forward net, layer `n` sees only what layer `n-1` computed. A residual block also passes `x` forward unchanged and adds a learned residual:

output `= F(x) + x`,

often then a ReLU. If `F(x)` and `x` have different lengths, use `F(x) + W x` with a learned or fixed matrix `W`. You can stack many such blocks. The short path from early layers to later layers lets gradient flow back without crossing every non-linearity. Sometimes learning "what to add to `x`" is easier than learning the whole function `H(x)`. The slide's remark is: to learn `H(x)`, learn the residual and add `x`. The benefit is that training converges. It is not, by itself, a claim that the model overfits less.

### Memory hooks

- Train, validate, test: fit, choose, report. In that order. The test set is a sealed envelope.
- Underfit: high train error. Overfit: low train error, high test error.
- Weight decay shrinks weights. Dropout removes units at random. Early stopping throws away the late epochs. Augmentation invents extra legal examples.
- Residual: "add a skip so the layer learns the change, not the whole function." Not a regulariser.

### Check yourself

- Why is a test set ruined if you tune on it? **Answer.** The reported error then depends on choices made after seeing those rows, so it estimates performance on data you already used.
- What is patience? **Answer.** The number of epochs you allow with no validation improvement before you restore the best saved weights.
- Write the decay factor in the weight update. **Answer.** Multiply `w` by `(1 - eta*lambda)`, then subtract the scaled data gradient.
- Why is a residual connection not regularisation? **Answer.** It changes how easily the optimisation moves through a deep net. It does not directly constrain capacity to improve generalisation.

---

## Lecture 9: Decision trees

Lab week 9 matches this lecture.

### How to picture it

A decision tree is a flowchart. Each question is about one attribute. Each answer is a branch. You stop at a leaf that says the class. It is supervised classification when the leaf is a category. People like trees because you can read the flowchart aloud: "if rooms = 4, predict rent." The algorithm's job is to choose the questions, and their order, from examples.

### Need to know

A tree represents a function from attribute values to one output. An internal node tests one attribute. A branch is one possible value of that attribute. A leaf is the output. The same tree is a set of if-then rules, one rule per path. Binary classification means the output is positive or negative (yes or no).

**Learning** a tree: given labelled examples, build a tree that fits them and is as small as you can reasonably make it. The number of possible trees is too large to search exhaustively. The method is greedy divide and conquer. Pick the best question for the rows you still have, split into smaller groups, and repeat inside each group. You get a small tree that is consistent with the training rows. You do not get a proof that it is the smallest possible tree.

**ID3** (Iterative Dichotomiser 3) is Ross Quinlan's algorithm, University of Sydney, around 1986. Top down:

```text
If every remaining example is positive, return a Yes leaf.
If every remaining example is negative, return a No leaf.
If no examples remain, return the majority class of the parent.
If no attributes remain, but the rows are still mixed, return their majority class.
Otherwise choose the best remaining attribute, make one child per value,
send each example down the matching child, and recurse.
```

`PLURALITY-VALUE` is the majority vote, with random tie-breaking. `IMPORTANCE` is the function that picks the attribute. Two definitions of "best" appear. Classification error: if you labelled the node with its majority class, what fraction would you get wrong? The credit example predicts Safe at the root and is wrong on `18/22 = 0.45` of the rows. Entropy, below, is the one ID3 and the lab use.

A good attribute makes the children purer than the parent. In the restaurant example, asking "Patrons?" separates positive and negative bookings well. Asking "Type?" leaves each child as mixed as the parent, so it was a wasted question. After the first split, you choose the next question separately in each child. Attributes you never need, such as Raining and Reservation in the worked restaurant tree, simply do not appear. On a large, still-mixed node you predict the majority class. The slide's sketch is about 800 of one class and 95 of the other.

**Entropy** measures how mixed a set of labels is. For values with probabilities `P(vi)`:

`I = sum -P(vi) * log2(P(vi))`.

For a yes/no label, use `p = (# yes) / N` and `n = (# no) / N`:

`H = -(p * log2 p) - (n * log2 n)`.

Conventions: a pure set has entropy 0. There is nothing left to learn. Do not evaluate `0 * log 0`; take that term as 0. A fair coin, half and half, has entropy 1 bit. That is the maximum for two classes. A coin that lands heads 99% of the time has entropy near 0: you are rarely surprised. Entropy is "how many yes/no questions is the label still worth?" A pure node is worth zero.

**Information gain** of attribute `A` is the drop in entropy from asking `A`:

`IG(A) = H(parent) - sum (|child| / |parent|) * H(child)`.

The weights are the fraction of rows that go down each branch. A child with two rows should not count as much as a child with fifty. Pick the attribute with the largest gain. In the restaurant set, 6 positive and 6 negative, so `H = 1`. Patrons has the highest gain, so Patrons is the root.

Accuracy tends to rise as the training set grows. One curve on the slides is around 95% and still climbing. A learning curve trains on larger and larger subsets and always tests on the same held-out test set. The slide's lesson: every learning bias makes some functions easier and others harder. A tree bias (axis-aligned questions, one attribute at a time) suits diagnosis rules and suits a diagonal boundary in the plane badly.

Problems you should be able to name:

- **Overfitting.** The tree matches training rows, including noisy ones, and misses the test set. Pruning deletes nodes that are not clearly helping. A simple stop: do not split if the best gain is below a threshold. Otherwise you will split on noise.
- **Gain favours many-valued attributes.** A student ID or a timestamp splits the data into singletons, and each singleton is pure, so the gain looks perfect. The tree has memorised identities. **Gain ratio** divides information gain by the intrinsic information of the attribute (how mixed the attribute's own values are). Attributes with huge domains are penalised. The slide says the denominator is smaller for attributes with smaller domains, which is why a modest attribute can win on gain ratio even when raw gain liked the huge one.
- **One feature at a time.** Some patterns need two attributes together. The slides call this the Costanza party problem and say there is no obvious easy fix inside basic ID3.
- Missing values, attributes with very many values, infinite domains, and continuous targets. A continuous target is regression, and ordinary ID3 as taught here is for discrete class labels. Extensions exist. The course wants you to know these are the known limits.

Use a tree when rows are attribute-value pairs, the target is a discrete class, a disjunction of rules is an acceptable hypothesis ("rent if rooms = 4, or if rooms = 3 and new kitchen"), and the data may be noisy. Examples: equipment faults, medical diagnosis, credit risk.

### Lab week 9

Five houses. Features: Furniture (Yes/No), Nr rooms (3 or 4), New kitchen (Yes/No). Target: Rent (Yes/No). This is supervised binary classification.

| House | Furniture | Rooms | New kitchen | Rent |
| --- | --- | --- | --- | --- |
| 1 | No | 3 | Yes | Yes |
| 2 | Yes | 3 | No | No |
| 3 | No | 4 | No | Yes |
| 4 | No | 3 | No | No |
| 5 | Yes | 4 | No | Yes |

Parent entropy. 3 Yes and 2 No, so `p = 0.6`, `n = 0.4`.

`H = -(0.6 * log2 0.6) - (0.4 * log2 0.4) = 0.971` bits.

Near 1, so the label is still quite uncertain. Worth asking a question.

Gain at the root:

- Furniture: 0.020 bits. Almost useless. The Yes and No furniture groups stay mixed.
- Nr rooms: 0.420 bits. Best.
- New kitchen: 0.171 bits.

Root is Nr rooms. Why the gain is large: rooms = 4 contains houses 3 and 5, both Rent Yes, entropy 0. A pure child contributes nothing to the weighted sum. Rooms = 3 contains houses 1, 2, and 4, entropy 0.918, still mixed.

`IG = 0.971 - (3/5)*0.918 - (2/5)*0 = 0.971 - 0.551 = 0.420`.

Inside rooms = 3 only, compare the two remaining features.

- Furniture gain is 0.251.
- New kitchen gain is 0.918. It splits the three houses into pure groups: house 1 (kitchen Yes, Rent Yes) and houses 2 and 4 (kitchen No, Rent No).

So the second question is New kitchen, and both children are leaves. Furniture is never selected. Unused features do not appear. That is normal, not a bug.

Rules:

- If rooms = 4 then Rent = Yes.
- If rooms = 3 and new kitchen = Yes then Rent = Yes.
- If rooms = 3 and new kitchen = No then Rent = No.

The tree has 2 internal nodes and 3 leaves, and it classifies all 5 training rows. To classify a new house, start at the root and follow the matching branch. A house with 4 rooms is Yes even if the kitchen is old, because that branch never asks about the kitchen. A house with 3 rooms and a new kitchen is Yes. Furniture is irrelevant to this tree, even if the new house has a value for it.

### Memory hooks

- Entropy 0: certain. Entropy 1: a fair coin, for two classes.
- Gain: "parent surprise minus the average surprise of the children." Weight children by how many rows they hold.
- Pure child: stop. Mixed child: ask another question. No questions left: majority.
- Student ID looks like infinite gain and is memorisation. Gain ratio is the brake.
- ID3 is greedy: best question now, no promise of the smallest tree.

### Check yourself

- Four reasons ID3 makes a leaf. **Answer.** All yes, all no, no rows left (use the parent's majority), or no attributes left (use the remaining rows' majority).
- Why is a pure child good for gain? **Answer.** Its entropy is 0, so it does not add to the weighted sum, and the parent entropy is not cancelled.
- Why can a unique ID win on raw gain? **Answer.** Each branch holds one row, every child is pure, and the weighted entropy is 0.
- Walk a 4-room house with an old kitchen. **Answer.** Rooms = 4 goes straight to Yes. The kitchen is not consulted.

---

## Lecture 10: Bayes nets

No lab solution in this folder.

### How to picture it

A full probability table of "every variable at once" is honest and enormous. Five yes/no variables already have 32 rows. Twenty have about a million. A Bayes net is a way to write the same joint distribution as a product of small local tables, by drawing which variables directly influence which. The graph is the knowledge. The numbers are the strengths.

### Need to know

A **random variable** is one uncertain quantity. `R` might be raining, with values `{true, false}`, often written `+r` and `-r`. `T` might be `{hot, cold}`. `D`, a drive time, might be any non-negative real. `L`, a ghost's location, might be a grid cell. Capital letters are the variables. Lower case is a particular value.

A **distribution** puts a probability on each value. Each probability is at least 0, and they sum to 1. A probability is one number. A distribution is the whole table.

A **joint distribution** over `X1, ..., Xn` puts a probability on every full assignment, with the same two rules: non-negative, and the whole table sums to 1. If you have `n` variables and each has `d` values, there are `d^n` rows. That is why you almost never write the joint down.

An **event** is a set of those rows. Its probability is the sum of the rows in the set. From the joint you can answer "hot and sunny", "hot", and "hot or sunny". "Or" is the sum of the matching rows, and if a row matches both phrases you must not add it twice. It is easier to sum the rows you want than to memorise inclusion-exclusion under exam pressure.

**Marginalisation** (summing out) throws variables away by adding the rows that match on the variables you keep. Weather table from the slides:

| T | W | P |
| --- | --- | --- |
| hot | sun | 0.4 |
| hot | rain | 0.1 |
| cold | sun | 0.2 |
| cold | rain | 0.3 |

`P(hot) = 0.4 + 0.1 = 0.5`. `P(sun) = 0.4 + 0.2 = 0.6`. You added over the variable you were not asked about.

**Conditional probability** is a restriction of attention. `P(a | b)` is the probability of `a` once you know `b`. Definition:

`P(a | b) = P(a, b) / P(b)`,

which is the same statement as `P(a, b) = P(a | b) P(b)`. From the table, `P(sun | hot) = 0.4 / 0.5 = 0.8`. A conditional distribution is a whole distribution for the remaining variables, given the fixed ones. Each row of a conditional probability table must itself sum to 1. `P(sun | hot) + P(rain | hot) = 0.8 + 0.2 = 1`. If your conditional row does not sum to 1, you divided wrong.

**Bayes' rule** is the definition applied in both directions.

`P(a, b) = P(a | b) P(b) = P(b | a) P(a)`,

so

`P(b | a) = P(a | b) P(b) / P(a)`.

You use it when one direction is the one you can estimate and the other is the one you need. A doctor knows roughly `P(symptom | disease)` from textbooks, and `P(disease)` from how common the disease is. The patient needs `P(disease | symptom)`. Bayes' rule is that conversion. `P(a)` in the denominator is often computed by summing `P(a | b) P(b)` over the values of `b` (the law of total probability). If you only need to compare two diseases, the denominator is the same for both and you can compare the numerators.

A **Bayes net** is:

- one node per random variable,
- a directed acyclic graph (arrows, no directed loops),
- a conditional distribution for each node given its parents.

The arrows mean direct influence, in the sense the model builder chooses. A missing arrow is a claim of conditional independence, made precise below. The local table is a **CPT** (conditional probability table): each row is the distribution of the child for one setting of the parents. The net is the picture plus those numbers. Either alone is not a Bayes net.

**Alarm network**, the one to be able to compute with. Burglary `B` and earthquake `E` both influence alarm `A`. The alarm influences John calling `J` and Mary calling `M`. John and Mary do not influence each other directly.

- `P(B = true) = 0.001`, so `P(B = false) = 0.999`.
- `P(E = true) = 0.002`, so `P(E = false) = 0.998`.
- `P(A | B, E)` is 0.95 if both are true, 0.94 if only burglary, 0.29 if only earthquake, 0.001 if neither.
- `P(J | A) = 0.90`, and `P(J | not A) = 0.05`. John sometimes calls because he confused the phone.
- `P(M | A) = 0.70`, and `P(M | not A) = 0.01`.

Free parameters in a CPT: parents with domain sizes `d1, ..., dk`, child with domain size `d`. There are `d1*...*dk` rows, and each row has `d` numbers that sum to 1, so you may choose `d - 1` numbers per row. Count: `(d - 1) * d1 * ... * dk`. For a yes/no child, `d - 1 = 1`, so you store one number per parent combination and infer the other. The alarm slide marks 1, 1, 4, 2, 2 free parameters on `B`, `E`, `A`, `J`, and `M`. Check `A`: two binary parents give 4 rows, and a binary child stores 1 free number per row, so 4. Check `J`: one binary parent, 2 free numbers.

Size: `n` variables, domain size at most `d`, at most `k` parents each. The joint table is `O(d^n)`. The Bayes net is `O(n * d^k)`. If causes are local, `k` stays small and the net grows linearly with `n` while the joint grows exponentially. That is the reason to draw the graph.

**Global semantics.** If you multiply the local conditionals you get the joint:

`P(X1, ..., Xn) = product over i of P(Xi | Parents(Xi))`.

A node with no parents contributes its marginal, such as `P(B)`. Worked atom from the slides:

`P(b, not e, a, not j, not m) = P(b) * P(not e) * P(a | b, not e) * P(not j | a) * P(not m | a)`

`= 0.001 * 0.998 * 0.94 * 0.1 * 0.3 = 0.000028`.

Read each factor off the matching CPT row. `P(not j | a) = 1 - 0.9 = 0.1`. `P(not m | a) = 1 - 0.7 = 0.3`. `P(a | b, not e) = 0.94`, the "burglary only" row.

Why is this product equal to the chain rule? The ordinary chain rule is `P(Xi | X1, ..., X(i-1))`, everything earlier. Order the variables so parents come before children (a topological order, which exists because the graph has no cycles). The Bayes net claims that, once you know the parents, the earlier non-parents add nothing:

`P(Xi | earlier) = P(Xi | Parents(Xi))`.

In words: **a variable is conditionally independent of its non-descendants, given its parents.** Given whether the alarm is ringing, John's call does not depend on the burglary. The burglary already did its work by affecting the alarm. Choose parents that "shield" the node from the other earlier variables. If you forget an arrow that is a real influence, the independence claim is false and the product is the wrong joint.

**Inference by enumeration** answers a query by summing the hidden variables out of that product. Both neighbours call. What is the probability of a burglary?

`P(B | j, m) = alpha * sum over e and a of P(B) P(e) P(a | B, e) P(j | a) P(m | a)`.

You compute the sum twice, once for `B = true` and once for `B = false`. Those two numbers are not yet a distribution. `alpha` is the constant that makes them sum to 1 (divide each by their total). Exact inference is "sums of products of CPT entries." The naive sum has exponentially many terms. The speedup is the same idea as factoring algebra. The slide rewrites

`uwy + uwz + uxy + uxz + vwy + vwz + vxy + vxz`

which is 16 multiplies and 7 adds, as `(u+v)(w+x)(y+z)`, which is 2 multiplies and 3 adds. Shared pieces of the Bayes net product should be computed once. You are not expected to finish a variable-elimination trace unless a question sets one up. You are expected to expand one assignment as a product and to say why enumeration is exponential.

### Memory hooks

- Marginal: add away the variables you did not ask for.
- Conditional: restrict the table, then renormalise so the remaining rows sum to 1.
- Bayes: swap the condition. `P(cause | effect)` from `P(effect | cause)`.
- Bayes net joint: multiply one local conditional per node.
- Missing arrow: "given my parents, I do not care about those other earlier variables."
- Free CPT numbers: `(d - 1)` per parent combination, because the row sums to 1.

### Check yourself

- `P(hot, sun) = 0.4` and `P(hot) = 0.5`. What is `P(sun | hot)`? **Answer.** `0.4 / 0.5 = 0.8`.
- Expand `P(b, not e, a, not j, not m)`. **Answer.** `0.001 * 0.998 * 0.94 * 0.1 * 0.3 = 0.000028`.
- Free parameters for a yes/no child with two yes/no parents? **Answer.** 4 parent rows, 1 free number each, so 4.
- What does a missing arc claim? **Answer.** A conditional independence: the child is independent of that non-parent once the parents are known.

---

## Lecture 11: MDPs and reinforcement learning

No lab solution in this folder. Week 5 introduced the loop. This lecture is the formal version.

### How to picture it

In a maze from week 2, "move north" always goes north. In an MDP, "move north" might go north most of the time and sometimes slip east. The world is stochastic, and the goal is not a single target square. The goal is to collect as much reward as possible over time. A policy is the habit: in this state, take this action.

Reinforcement learning is the same problem after the map is taken away. You do not know the slip probabilities or the rewards. You have to move, see what happened, and learn.

### Need to know

An **MDP** (Markov decision process) has:

- States `s` in `S`.
- Actions `a` in `A`.
- A transition model `T(s, a, s') = P(s' | s, a)`. The probability that action `a` in state `s` lands in `s'`.
- A reward `R(s, a, s')` for that transition. Sometimes written as a reward for entering a state. Use the form the question uses.
- A start state, and sometimes terminal states where the episode ends (the exit squares).
- A utility that adds up rewards, usually discounted.

**Markov** means the next state depends on the current state and the action, not on the whole history. If "which room you came from" still matters, it has to be folded into the state, or the model is wrong. This is the same modelling lesson as week 1: the state must contain whatever the decision depends on.

**Discount** `gamma` is a number in `[0, 1)`. Reward `t` steps in the future is multiplied by `gamma^t`. A reward now counts fully. The same reward tomorrow counts less. Two reasons: the future is less certain, and without a discount an infinite episode can have an infinite sum and you cannot compare policies. The geometric series sums to

`1 + gamma + gamma^2 + ... = 1 / (1 - gamma)`.

If every step paid +1 forever, the total utility would be `1 / (1 - gamma)`, not infinity. `gamma` near 1 means you care about the distant future. `gamma` near 0 means you are shortsighted. The grid examples in the lecture often set `gamma = 1` for a finite episode that is guaranteed to end, where the sum cannot run forever.

A **policy** `pi(s)` says which action to take in state `s`. The optimal policy maximises expected utility. "Expected" matters because transitions are random: you average over the slips.

**Reinforcement learning** keeps the MDP and removes the agent's knowledge of `T` and `R`. The agent must try actions. Every update is based on samples `(s, a, s', r)` that actually happened. The environment returns the next state and the reward. The agent does not get to rewind and resample the same state at will.

Four words the slides want paired with a meaning:

- **Exploration**: try an action whose result you do not know yet.
- **Exploitation**: use the best action according to what you already learned.
- **Sampling**: repeat, because one outcome is not the probability.
- **Generalisation**: a lesson in one state may apply in a similar state. Tabular methods do not do this. Approximate Q-learning does.

**Passive** learning evaluates a fixed policy. The agent does not choose. It is "along for the ride," executes `pi`, and learns the values. This is not offline planning. The actions happen in the world.

**Model-based** passive learning builds a mini MDP from counts. For each pair `(s, a)`, the fraction of times you next saw `s'` is your estimate of `T(s, a, s')`. The rewards you saw estimate `R`. Then you solve that learned MDP as if the estimates were true. In the slide's grid, `gamma = 1`: from the episodes, `T(B, east, C) = 1.00` (every east from B went to C), `T(C, east, D) = 0.75`, `T(C, east, A) = 0.25` (three of four east moves from C went to D, one went to A), ordinary steps reward `-1`, and `R(D, exit) = +10`. Advantage: each trip updates a model, and the model connects states, so one experience informs many values when you solve the MDP. Limit: you learn one state-action pair at a time, and if `|S|` is huge you cannot store or solve the table.

The age analogy: if you know the distribution of ages, compute the expectation from the distribution. That is model-based. If you do not, average the ages you sampled. Samples show up in proportion to their probability, so the average converges. That is model-free.

**Direct evaluation** is the crude model-free method. Follow `pi`. Each time you leave a state, write down the sum of discounted rewards from there to the end of the episode. Average those sums. You need no `T` or `R`. Eventually the averages are right. You waste the connections: learning `C` does not help `B`, even if `B` always goes to `C`. In the sample output, B and E can show different values even though both move to C under the policy, because each state's samples are averaged in isolation. Learning is slow.

**Temporal-difference (TD)** learning fixes that waste without building `T`. On every transition `(s, a, s', r)`, nudge `V(s)` toward the one-step target `r + gamma * V(s')`:

think "my value should match what I just got, plus the discounted value of where I landed."

Likely successors appear more often, so they pull `V(s)` more often. That is a running average standing in for the unknown probabilities. You never rewind time. One sample per visit is enough, because the next visit brings another sample.

With a fixed step size `alpha`, this is an exponential moving average: recent samples weigh more, and old values fade. That is useful early, when the old value was a bad guess. If you decrease `alpha` over time, the average can converge instead of chasing noise forever. TD here is still **policy evaluation**. The policy is fixed. `V` tells you how good a state is under that policy. It does not tell you which action is better, so you cannot turn `V` into a new policy without knowing `T`. If two actions leave the same state, `V` does not say which one you should pick next.

**Q-learning** stores the missing piece. `Q(s, a)` is the expected utility of taking action `a` in state `s` and acting optimally afterward.

- `V(s) = max over a of Q*(s, a)`. The state's value is its best action's value.
- `pi*(s) = argmax over a of Q*(s, a)`. The optimal policy picks that action.

Sample update, the one to memorise:

`Q(s, a) <- (1 - alpha) * Q(s, a) + alpha * [r + gamma * max over a' of Q(s', a')]`.

`(1 - alpha) * old + alpha * new` is the running average. The new target is: reward just received, plus discounted value of the **best** action in the next state, according to the current Q table. The `max` is why you do not need `T`. You did not average over next states using probabilities. You used the next state you actually landed in, and you assumed that from then on you will pick the best known action.

After learning, the policy is `pi(s) = argmax_a Q(s, a)`. No model. The price is memory: a Q table has an entry per state-action pair, while `V` has one entry per state.

**Active** versus passive: an active agent chooses the actions. Q-learning is the active, model-free method in this lecture.

**Off-policy**, the "amazing result" on the slides: Q-learning converges to the optimal Q values even if the actions you used to explore were not optimal. The `max` in the target evaluates the best next action, not the action your behaviour policy actually took. Caveats, all required for the theorem: you explore enough that every relevant pair is tried infinitely often in the limit, and `alpha` goes to 0, but not so fast that the updates stop before the values settle. In that limit, how you picked actions does not matter. During a real finite run, it matters a lot, because of regret.

**Epsilon-greedy** is the simple exploration scheme. Each step, with probability `epsilon` take a random action, and with probability `1 - epsilon` take `argmax Q`. If `epsilon` stays high forever, you keep thrashing after you already know the policy. Decay `epsilon` over time.

**Exploration function**: do not explore at random. Explore where you are still ignorant. Replace the value `u` with something optimistic that shrinks as the visit count `n(s, a)` grows, for example `u + k / n(s, a)` with a constant `k`. Unvisited pairs look artificially good, so the `max` selects them, you visit them, `n` rises, and the bonus fades. The bonus propagates backward: a known state that leads into an unknown state gets a high target, because the next state's optimistic Q appears in the update. Random exploration and this bonus can both reach an optimal policy.

**Regret** is the cost of the mistakes you made while learning: the difference between the reward you actually collected and the reward you would have collected by following the optimal policy from the start. Minimising regret is harder than "eventually be optimal." Random exploration tends to have higher regret than an exploration function, because it keeps taking stupid actions after the values are known.

**Approximate Q-learning** is for when the table does not fit. Pac-Man cannot visit every grid configuration, and cannot store a Q for each one. Describe a state, or a state-action, by **features**: numbers you compute from the state. Examples: distance to the nearest ghost, distance to the nearest food, number of ghosts, `1 / (distance to food)^2`, whether Pac-Man is in a tunnel (0 or 1), whether this action moves toward food. A linear Q function is a weighted sum of the features that are on. Learning updates a handful of weights, not a giant table. If something unexpectedly bad happens, decrease the weights of the features that were active, so every similar state looks worse next time. That is generalisation. The failure mode is also generalisation: two positions can share features and still deserve different values, and the linear function cannot say so.

### Memory hooks

- MDP: states, actions, transition probabilities, rewards, discount. Policy: what I do in each state.
- Passive: the policy is given, learn its values. Active: I choose, and I have to explore.
- Direct evaluation waits until the episode ends and averages. TD updates after every step. Q-learning updates an action, using the best next action.
- The `max` inside the Q target is what makes it off-policy.
- Explore versus exploit: epsilon-greedy flips a coin. An exploration bonus prefers the under-visited.
- Regret: the tuition you paid while learning, not whether you eventually pass.

### Check yourself

- List the MDP pieces. **Answer.** `S`, `A`, `T(s, a, s')`, `R`, start, optional terminals, discounted additive utility.
- Why can B and E have different direct-evaluation values if both go to C? **Answer.** Each state's returns are averaged separately. Direct evaluation never copies C's value back to them.
- Write the Q update. **Answer.** Blend the old `Q(s, a)` with `r + gamma * max Q(s', a')`, using weight `alpha` on the new target.
- What goes wrong if `epsilon` never falls? **Answer.** You keep taking random actions after the Q values are already good, so regret keeps growing.
- What do features buy you, and what do they cost? **Answer.** A few weights generalise to unseen states. States that share features are forced to share value, even when they should not.

---

## Formula card

Search:

- Problem: `<S0, A, T, G, C>`. Start, actions, transition, goal, cost.
- Node: state, parent, action, path cost. The parent chain is the solution.
- BFS time: `(b^(d+1) - 1) / (b - 1)`.
- UCS: expand smallest `g`. Test the goal when the node is selected, not when it is generated.
- A*: `f = g + h`. Admissible: `h <= true remaining cost`. Consistent: `h(n) <= step cost + h(next)`.

Local search and CSP:

- Hill climbing returns the first local optimum it reaches.
- Expected restarts about `1/p`.
- Backtracking assigns one variable per depth.
- MRV then degree for the variable. LCV for the value.
- Arc `X -> Y` is consistent when every remaining `x` has a legal `y`.

Learning:

- Regression: continuous `y`. Classification: discrete `y`.
- Linear model: `y = <w, x> + b`.
- MSE: average of `(y - y_hat)^2`.
- Closed form: `w* = (X^T X)^(-1) X^T y`, bias folded into `w`.
- Gradient step: `w <- w - eta * gradient`.
- Perceptron: if wrong, `w <- w + alpha * (y - y_hat) * x`.
- Sigmoid: `1 / (1 + exp(-z))`. Derivative: `s * (1 - s)`.
- Sigmoid output error: `y(1-y)(target - y)`, then `delta * previous activation` updates the weight.
- Entropy: `sum -p log2 p`. Gain: parent entropy minus the size-weighted child entropies.
- Bayes net: joint equals the product of `P(variable | its parents)`.
- Q update: `(1 - alpha) * Q(s, a) + alpha * [r + gamma * max Q(next, a')]`.
- Infinite discounted sum of 1: `1 / (1 - gamma)`.
