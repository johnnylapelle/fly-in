*This project has been created as part of the 42 curriculum by jvacossi.*

# Fly-in

## Description
Fly-in is an **efficient drone routing system** that navigates multiple drones
through connected zones while minimizing simulation turns and handling movement
constraints.

This projecty efficiently route a fleet of drones from a **central base (start)** to a **target location (end)** while navigating this dynamic network under a set of strict constraints and optimization goals.

The drones are routed on graphes representing the network of zones and a set of constraints.
The graph is represented as a **network of connected zones**, where connections define possible movement paths between zones.

## Instruction
section containing any relevant information about compilation, installation and execution

## Algorithm
detailed description of the algorithm and implementation strategy

## Visual Representation
documentation of the visual representation features and how they enhance the user experience

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

## Workflow:
- Parser/MapLoad
- Creation of the Graph
- GUI with the visualisation of the Graph
- Pathfinding Algorithm
	- BFS -> Dijkstra (heuristic function for A*)
	- A* space/time
- GUI animation and UX
