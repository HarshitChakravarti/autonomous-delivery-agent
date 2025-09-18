# Autonomous Delivery Agent

An AI-powered autonomous delivery agent that navigates a 2D grid city using various pathfinding algorithms including Breadth-First Search (BFS), Uniform-Cost Search (UCS), and A* search. The project also demonstrates dynamic replanning capabilities to handle unexpected obstacles.

## Project Structure

```
autonomous_delivery_agent/
│
├── main.py                 # Main entry point with CLI to run simulations
├── environment.py          # Defines the GridCity environment class
├── agent.py                # Defines the DeliveryAgent and its planning algorithms
├── utils.py                # Helper functions, data structures (e.g., PriorityQueue)
│
├── maps/
│   ├── small_map.txt
│   ├── medium_map.txt
│   ├── large_map.txt
│   └── dynamic_map.txt
│
└── README.md               # This file
```

## Map File Format

The map files are text files representing the grid with the following symbols:

- `S`: Start position
- `G`: Goal position
- `#`: Impassable static obstacle
- `.` or `1`: Standard terrain (movement cost of 1)
- `2`, `3`, ..., `9`: Difficult terrain with the corresponding integer movement cost

## Installation

No additional dependencies are required beyond Python 3.6+.

## Usage

Run the main script with the following command-line arguments:

```bash
python main.py --map <map_file> --algo <algorithm>
```

### Arguments

- `--map`: Path to the map file (required)
- `--algo`: Algorithm to use (required)
  - `bfs`: Breadth-First Search
  - `ucs`: Uniform-Cost Search
  - `a_star`: A* Search
  - `dynamic_demo`: Dynamic replanning demonstration

### Examples

```bash
# Run BFS on the small map
python main.py --map maps/small_map.txt --algo bfs

# Run UCS on the medium map
python main.py --map maps/medium_map.txt --algo ucs

# Run A* on the large map
python main.py --map maps/large_map.txt --algo a_star

# Run dynamic replanning demo
python main.py --map maps/dynamic_map.txt --algo dynamic_demo
```

## Output

The program outputs the following information for each algorithm:

- **Algorithm**: The algorithm used
- **Path Found**: Whether a path was found (Yes/No)
- **Path Cost**: Total cost of the path (if found)
- **Path Length**: Number of steps in the path (if found)
- **Path**: The actual path as a list of coordinates (if found)
- **Nodes Expanded**: Number of nodes explored during search
- **Time Taken**: Execution time in seconds

## Algorithms Implemented

### 1. Breadth-First Search (BFS)
- Explores all nodes at the current depth before moving to the next level
- Guarantees shortest path in terms of number of steps
- Uses a queue (FIFO) data structure

### 2. Uniform-Cost Search (UCS)
- Explores nodes in order of their path cost from the start
- Guarantees optimal path in terms of total cost
- Uses a priority queue ordered by path cost

### 3. A* Search
- Combines UCS with a heuristic function (Manhattan distance)
- More efficient than UCS while maintaining optimality
- Uses a priority queue ordered by f(n) = g(n) + h(n)

### 4. Dynamic Replanning
- Demonstrates the agent's ability to replan when obstacles appear
- Simulates agent movement and obstacle detection
- Shows the replanning process using A* search

## Features

- **Terrain Cost Support**: Different terrain types have different movement costs
- **Static Obstacles**: Impassable obstacles defined in the map
- **Dynamic Obstacles**: Obstacles that can appear during execution
- **Path Reconstruction**: Full path recovery from search results
- **Performance Metrics**: Detailed statistics on search performance
- **Error Handling**: Robust error handling for invalid maps and inputs

## Map Examples

### Small Map (5x4)
```
S.2.#
.1.3G
...##
#..1.
```

### Medium Map (8x8)
```
S.2.3.4.#
.1.2.3.4.5
..#.2.3.4.5
#..1.2.3.4G
#..#.2.3.4.5
#..#.2.3.4.5
#..#.2.3.4.5
#..#.2.3.4.5
```

## Technical Details

- **Grid Representation**: 2D list with terrain costs
- **Movement**: 4-connected (up, down, left, right)
- **Heuristic**: Manhattan distance for A* search
- **Data Structures**: 
  - `deque` for BFS
  - `PriorityQueue` (heapq) for UCS and A*
- **Time Complexity**: Varies by algorithm and map complexity
- **Space Complexity**: O(b^d) where b is branching factor and d is depth

## Contributing

Feel free to extend the project with additional algorithms, map formats, or features!
