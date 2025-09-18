# Main entry point with CLI interface for running autonomous delivery agent simulations
import argparse
import sys
import os
import json
from datetime import datetime
from environment import GridCity
from agent import DeliveryAgent

def main():
    parser = argparse.ArgumentParser(description="Run Autonomous Delivery Agent")
    parser.add_argument("--map", type=str, required=True, help="Path to map file.")
    parser.add_argument("--algo", type=str, required=True,
                        choices=['bfs', 'ucs', 'a_star', 'dynamic_demo'],
                        help="Algorithm to use.")
    parser.add_argument("--debug", action='store_true', help="Enable debug mode")
    parser.add_argument("--stats", action='store_true', help="Show performance statistics")
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    args = parser.parse_args()

    if not os.path.exists(args.map):
        print(f"Error: Map file '{args.map}' not found!")
        sys.exit(1)

    try:
        env = GridCity(args.map)
        agent = DeliveryAgent(env)
        
        if args.debug:
            agent.enable_debug_mode()
        
        if not env.start_pos:
            print("Error: No start position (S) found in the map!")
            sys.exit(1)
        if not env.goal_pos:
            print("Error: No goal position (G) found in the map!")
            sys.exit(1)

        print(f"Map loaded: {env.width}x{env.height}")
        print(f"Start position: {env.start_pos}")
        print(f"Goal position: {env.goal_pos}")
        print(f"Terrain types found: {sorted(env.map_metadata['terrain_types'])}")
        print()

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

        print(f"Algorithm: {args.algo.upper()}")
        print(f"Path Found: {'Yes' if result['path'] else 'No'}")
        if result['path']:
            print(f" -> Path Cost: {result['cost']}")
            print(f" -> Path Length: {len(result['path'])}")
            print(f" -> Path: {result['path']}")
        print(f"Nodes Expanded: {result['nodes_expanded']}")
        print(f"Time Taken: {result['time']:.6f} seconds")
        
        if args.stats:
            print("\n=== Performance Statistics ===")
            stats = agent.get_performance_summary()
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        if args.output:
            output_data = {
                'timestamp': datetime.now().isoformat(),
                'map_file': args.map,
                'algorithm': args.algo,
                'result': result,
                'environment_stats': env.get_visit_stats() if hasattr(env, 'get_visit_stats') else {},
                'agent_stats': agent.get_performance_summary()
            }
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\nResults saved to {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
