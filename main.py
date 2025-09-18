# main.py
import argparse
import sys
import os
from environment import GridCity
from agent import DeliveryAgent

def main():
    parser = argparse.ArgumentParser(description="Run Autonomous Delivery Agent")
    parser.add_argument("--map", type=str, required=True, help="Path to map file.")
    parser.add_argument("--algo", type=str, required=True,
                        choices=['bfs', 'ucs', 'a_star', 'dynamic_demo'],
                        help="Algorithm to use.")
    args = parser.parse_args()

    # Check if map file exists
    if not os.path.exists(args.map):
        print(f"Error: Map file '{args.map}' not found!")
        sys.exit(1)

    try:
        # 1. Initialize environment and agent
        env = GridCity(args.map)
        agent = DeliveryAgent(env)
        
        # Check if start and goal positions are defined
        if not env.start_pos:
            print("Error: No start position (S) found in the map!")
            sys.exit(1)
        if not env.goal_pos:
            print("Error: No goal position (G) found in the map!")
            sys.exit(1)

        print(f"Map loaded: {env.width}x{env.height}")
        print(f"Start position: {env.start_pos}")
        print(f"Goal position: {env.goal_pos}")
        print()

        # 2. Select and run the algorithm
        if args.algo == 'bfs':
            result = agent.bfs()
        elif args.algo == 'ucs':
            result = agent.ucs()
        elif args.algo == 'a_star':
            result = agent.a_star()
        elif args.algo == 'dynamic_demo':
            log = agent.dynamic_replanning_demo()
            print(log)
            return

        # 3. Print the results in a clean, readable format
        print(f"Algorithm: {args.algo.upper()}")
        print(f"Path Found: {'Yes' if result['path'] else 'No'}")
        if result['path']:
            print(f" -> Path Cost: {result['cost']}")
            print(f" -> Path Length: {len(result['path'])}")
            print(f" -> Path: {result['path']}")
        print(f"Nodes Expanded: {result['nodes_expanded']}")
        print(f"Time Taken: {result['time']:.6f} seconds")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
