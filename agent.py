# agent.py
from collections import deque
from utils import PriorityQueue, manhattan_distance
import time

class DeliveryAgent:
    def __init__(self, environment):
        self.env = environment
        self.start_pos = environment.start_pos
        self.goal_pos = environment.goal_pos

    def _reconstruct_path(self, came_from, current):
        """Reconstruct the path from start to goal using the came_from dictionary."""
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def bfs(self):
        """Breadth-First Search"""
        start_time = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {'path': None, 'cost': float('inf'), 'nodes_expanded': 0, 'time': 0}
        
        # BFS uses a queue (FIFO)
        queue = deque([self.start_pos])
        came_from = {self.start_pos: None}
        visited = {self.start_pos}
        nodes_expanded = 0
        
        while queue:
            current = queue.popleft()
            nodes_expanded += 1
            
            if current == self.goal_pos:
                path = self._reconstruct_path(came_from, current)
                # Calculate total cost
                total_cost = sum(self.env.get_cost(pos) for pos in path)
                elapsed_time = time.time() - start_time
                return {'path': path, 'cost': total_cost, 'nodes_expanded': nodes_expanded, 'time': elapsed_time}
            
            # Explore neighbors
            for neighbor, _ in self.env.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        # No path found
        elapsed_time = time.time() - start_time
        return {'path': None, 'cost': float('inf'), 'nodes_expanded': nodes_expanded, 'time': elapsed_time}

    def ucs(self):
        """Uniform-Cost Search"""
        start_time = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {'path': None, 'cost': float('inf'), 'nodes_expanded': 0, 'time': 0}
        
        # UCS uses a priority queue ordered by cost
        frontier = PriorityQueue()
        frontier.put(self.start_pos, 0)
        came_from = {self.start_pos: None}
        cost_so_far = {self.start_pos: 0}
        nodes_expanded = 0
        
        while not frontier.empty():
            current = frontier.get()
            nodes_expanded += 1
            
            if current == self.goal_pos:
                path = self._reconstruct_path(came_from, current)
                total_cost = cost_so_far[current]
                elapsed_time = time.time() - start_time
                return {'path': path, 'cost': total_cost, 'nodes_expanded': nodes_expanded, 'time': elapsed_time}
            
            # Explore neighbors
            for neighbor, move_cost in self.env.get_neighbors(current):
                new_cost = cost_so_far[current] + move_cost
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current
                    frontier.put(neighbor, new_cost)
        
        # No path found
        elapsed_time = time.time() - start_time
        return {'path': None, 'cost': float('inf'), 'nodes_expanded': nodes_expanded, 'time': elapsed_time}

    def a_star(self):
        """A* Search"""
        start_time = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {'path': None, 'cost': float('inf'), 'nodes_expanded': 0, 'time': 0}
        
        # A* uses a priority queue ordered by f(n) = g(n) + h(n)
        frontier = PriorityQueue()
        frontier.put(self.start_pos, 0)
        came_from = {self.start_pos: None}
        cost_so_far = {self.start_pos: 0}
        nodes_expanded = 0
        
        while not frontier.empty():
            current = frontier.get()
            nodes_expanded += 1
            
            if current == self.goal_pos:
                path = self._reconstruct_path(came_from, current)
                total_cost = cost_so_far[current]
                elapsed_time = time.time() - start_time
                return {'path': path, 'cost': total_cost, 'nodes_expanded': nodes_expanded, 'time': elapsed_time}
            
            # Explore neighbors
            for neighbor, move_cost in self.env.get_neighbors(current):
                new_cost = cost_so_far[current] + move_cost
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + manhattan_distance(neighbor, self.goal_pos)
                    came_from[neighbor] = current
                    frontier.put(neighbor, priority)
        
        # No path found
        elapsed_time = time.time() - start_time
        return {'path': None, 'cost': float('inf'), 'nodes_expanded': nodes_expanded, 'time': elapsed_time}

    def dynamic_replanning_demo(self):
        """
        Simulates the agent moving and replanning.
        1. Plan an initial path using A*.
        2. Simulate moving along the path for a few steps (e.g., 3-4 steps).
        3. Introduce a new, unexpected "dynamic" obstacle on the remaining path.
        4. Log that an obstacle was detected.
        5. Re-plan a new path from the agent's current position using A*.
        6. Log the new path and continue.
        Return a log string demonstrating the entire process.
        """
        log = []
        log.append("=== Dynamic Replanning Demo ===")
        log.append("")
        
        # Step 1: Plan initial path using A*
        log.append("Step 1: Planning initial path using A*")
        initial_result = self.a_star()
        
        if not initial_result['path']:
            log.append("ERROR: No initial path found!")
            return "\n".join(log)
        
        log.append(f"Initial path found: {initial_result['path']}")
        log.append(f"Initial path cost: {initial_result['cost']}")
        log.append(f"Nodes expanded: {initial_result['nodes_expanded']}")
        log.append("")
        
        # Step 2: Simulate moving along the path
        log.append("Step 2: Agent starts moving along the path")
        current_position = self.start_pos
        steps_taken = 0
        max_steps = min(4, len(initial_result['path']) - 1)  # Take up to 4 steps
        
        for i in range(max_steps):
            if i + 1 < len(initial_result['path']):
                current_position = initial_result['path'][i + 1]
                steps_taken += 1
                log.append(f"  Step {steps_taken}: Agent moves to {current_position}")
        
        log.append(f"Agent has moved {steps_taken} steps and is now at {current_position}")
        log.append("")
        
        # Step 3: Introduce dynamic obstacle
        log.append("Step 3: Unexpected obstacle detected!")
        
        # Find a position on the remaining path to block
        remaining_path = initial_result['path'][steps_taken + 1:]
        if remaining_path:
            obstacle_pos = remaining_path[0]  # Block the next position on the path
            self.env.add_dynamic_obstacle(obstacle_pos, steps_taken)
            log.append(f"Dynamic obstacle added at position {obstacle_pos}")
            log.append(f"Remaining original path: {remaining_path}")
        else:
            log.append("No remaining path to block - agent has reached the goal!")
            return "\n".join(log)
        
        log.append("")
        
        # Step 4: Re-plan from current position
        log.append("Step 4: Re-planning path from current position using A*")
        
        # Temporarily update start position for replanning
        original_start = self.start_pos
        self.start_pos = current_position
        
        replan_result = self.a_star()
        
        # Restore original start position
        self.start_pos = original_start
        
        if not replan_result['path']:
            log.append("ERROR: No replanned path found!")
            return "\n".join(log)
        
        log.append(f"Replanned path found: {replan_result['path']}")
        log.append(f"Replanned path cost: {replan_result['cost']}")
        log.append(f"Nodes expanded for replanning: {replan_result['nodes_expanded']}")
        log.append("")
        
        # Step 5: Continue with new path
        log.append("Step 5: Agent continues with the new path")
        log.append("Dynamic replanning demo completed successfully!")
        
        return "\n".join(log)
