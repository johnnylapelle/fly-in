*This project has been created as part of the 42 curriculum by jvacossi.*

# Fly-in
![](assets/banner2.png)

## Description
Fly-in is an **efficient drone routing system** that navigates **multiple drones** (represented by fishes) through **connected zones** while minimizing **simulation turns** and handling **movement constraints**.

This project efficiently route a fleet of drones from a **central base (start)** to a **target location (end)** while navigating this dynamic network under a set of strict constraints and optimization goals.

The drones are routed on **graphes** representing the network of zones and a set of constraints.
The graph is represented as a **network of connected zones**, where connections define possible movement paths between zones.

### The Constraints
The constraints are represented by different zones types:
- **Normal zone**: Default and standard zone with 1 turn movement cost.
- **Priority zone**: A preferred zone. Movement to this zone costs 1 turn but should be prioritized in pathfinding.
- **Restricted zone**: A sensitive or dangerous zone. Movement to this zone costs 2 turns.
- **Blocked zone**: Inaccessible zone. Drones must not enter or pass through this zone. Any path using it is invalid.


Each zones can have metadatas:
- **zone=\<type\>**: to specify the type of the zone. By default it's normal.
- **max_drones=\<number\>**: Maximum drones that can occupy this zone simultaneously. By default it's 1.
- **color=\<value\>**: The color of the zone. Not a real constraint, just usefull for the visualisation.

The connections in-between zones can also have metadatas:
- **max_link_capacity=\<number\>**: Maximum drones that can traverse this connection simultaneously. By default it's 1.

### The Map/Graph
Here is a **file example** of a graph that represent the network of zones:
```
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 4 4 [color=yellow]
hub: roof1 1 2 [zone=restricted color=red]
hub: roof2 3 1 [zone=normal color=blue]
hub: corridorA 2 1 [zone=priority color=green max_drones=2]
hub: tunnelB 3 2 [zone=normal color=red]
hub: obstacleX 2 2 [zone=blocked color=gray]

connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```
Rules:
- The first line defines the number of drones using nb_drones: <number>.
- start_hub: <name> <x> <y> [metadata] marks the starting zone.
- end_hub: <name> <x> <y> [metadata] marks the end zone.
- hub: <name> <x> <y> [metadata] defines a regular zone.
- All metadata is optional and enclosed in brackets [...] with default values:
- zone=<type> (default: normal)
- color=<value> (default: none)
- max_drones=<number> (default: 1) - Maximum drones that can occupy this zone simultaneously
- Tags inside brackets can appear in any order.

Wich will give:
![](assets/example_map.png)

## Instruction
Install the dependencies.
``` sh
make install
```

Run the program, by default the program will run a map from the maps folder. You can optionally specify custom paths using the --map argument.
``` sh
make run

make run ARGS="--map maps/map.txt"
```

Run the program in debug mode.
```sh
make debug
```

## Algorithm

### Overview
Each drone is assigned a path sequentially. For each drone, a
**Space-Time A*** algorithm finds the optimal route through the graph,
taking into account both spatial constraints (zone and connection
capacities) and temporal constraints (which zones and connections are
already reserved at a given turn).

To guide A* efficiently, a **reverse Dijkstra** is run once before any
drone is processed. Starting from the end zone, it computes the minimum
travel cost from every zone to the destination. This serves as an heuristic.

Conflicts between drones are resolved through a **reservation table**,
which tracks zone and connection occupancy at each turn. Once a drone's
path is computed, its zones and connections are reserved, constraining
the search space for subsequent drones. If a route is blocked, a drone
can wait in place until it becomes available.

### Heuristic - Reverse Dijkstra
Before any drone is processed, a **reverse Dijkstra** run backward, from the end to every single zone. This produce a cost estimate for every zone. Roughly, how far is this zone from the destination ?

This estimate is used by A*. Its work like a compass, at each step, the algortihm prioritizes zones that appears closest to the goal. This reduces the number of routes evaluated before finding the optimal path.

### Pathfinding - Space-Time A*
The classic **A\* Algorithm** finds the shortest path from a starting point from and end point.
But in our case this is not enough due to the zone's and connection's capacity constraints.

To handle this, the algorithm operates on **zones and turns** instead of just zones. This time dimension allow the algorithm to distinguish between "drone at zone X at turn 3" and "drone at zone X at turn 7" and to plan around congestion rather than just distance.

At each step a drone has two options:
-	**Move** to a neighboring zone if the route is available at that turn.
-	**Wait** in place.

### Multi-drone resolution
Drones are processed one-by-one. The first drone finds its optimal path freely. Each subsequent drone is constrained by the reservations left by previous drones.

Once a path is computed, every zone and connection it uses is reserved in a **reservation table**, keyed by location and turn. This table is the shared memory between drones, it is what prevents collisions.

### Complexity
**Reverse Dijkstra** runs once and visits every zone in the graph.
Its time complexity is **O(N log N)**, where N is the number of zones.

**Space-Time A*** operates on a graph of **(zone, turn)** states. In the
worst case, every zone is visited at every turn, giving a state space of
**O(N × T)** per drone, where T is the maximum number of turns required
to reach the destination. With D drones processed sequentially, the
total time complexity is **O(D × N × T × log(N × T))**.

In practice, the heuristic significantly reduces the number of states
explored — most routes are pruned early, and drones rarely need to wait
long. Real-world performance is considerably better than the worst case.

### Visual Representation
The simulation comes with an interactive graphical interface that renders
the graph and animates each drone moving through it in real time. This
makes it straightforward to verify that paths are correct, spot
congestion, and observe how drones coordinate around each other.

Maps can be loaded directly from the interface, making it easy to switch
between scenarios without restarting the application. Playback controls
allow stepping through the simulation turn by turn, playing it
automatically, or jumping forwards and backwards to inspect any moment
of the flight.

## Resources
### Pathfinding algorithm
- https://www.redblobgames.com/pathfinding/a-star/introduction.html
- https://ojs.aaai.org/index.php/AIIDE/article/view/18726/18503
- https://fr.wikipedia.org/wiki/Distance_de_Manhattan
- https://tracker.pathfinding.ai/ (Benchmark for MAPF Algo)
- https://github.com/Jiaoyang-Li/CBSH2-RTC (one of the best MAPF algo)

### Graphical User Interface
- https://www.pythonguis.com
- https://doc.qt.io/qtforpython-6/index.html

### Miscellaneous
- https://fr.wikipedia.org/wiki/PSPACE

## AI Usage
- **Socratic guidance**: Rather than requesting direct solutions, AI was used as a thinking partner — asking the right questions to guide independent implementation decisions.
- **Code review**:
- **Documentation**: AI assisted in writing docstrings following PEP 257 (Google style) and drafting README sections including Algorithm Explanation and Complexity.
- **Research synthesis**: AI summarized academic papers and blog posts on Pathfinding Algorithm and identified which concepts were applicable to the project.
- **PyQt6**: Learned with help of AI.

