# DeliveryAgent class implementing BFS, UCS, A* pathfinding algorithms and dynamic replanning
from collections import deque
from utils import MyPriorityQueue, calculate_manhattan_heuristic
import time
import random

class DeliveryAgent:
    def __init__(self, environment):
        self.env = environment
        self.start_pos = environment.start_pos
        self.goal_pos = environment.goal_pos
        self.debug_mode = False
        self.path_history = []
        self.performance_stats = {'total_searches': 0, 'successful_searches': 0}

    def _build_path_backwards(self, parent_map, current_node):
        path_trace = []
        while current_node is not None:
            path_trace.append(current_node)
            current_node = parent_map.get(current_node)
        path_trace.reverse()
        return path_trace

    def bfs(self):
        self.performance_stats['total_searches'] += 1
        start_timer = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {'path': None, 'cost': float('inf'), 'nodes_expanded': 0, 'time': 0}
        
        search_queue = deque([self.start_pos])
        parent_tracker = {self.start_pos: None}
        explored_nodes = {self.start_pos}
        expansion_count = 0
        
        if self.debug_mode:
            print(f"Starting BFS from {self.start_pos} to {self.goal_pos}")
        
        while search_queue:
            current_node = search_queue.popleft()
            expansion_count += 1
            
            if self.debug_mode and expansion_count % 10 == 0:
                print(f"Expanded {expansion_count} nodes, current: {current_node}")
            
            if current_node == self.goal_pos:
                final_path = self._build_path_backwards(parent_tracker, current_node)
                total_path_cost = sum(self.env.get_cost(pos) for pos in final_path)
                execution_time = time.time() - start_timer
                self.performance_stats['successful_searches'] += 1
                self.path_history.append(('BFS', final_path, execution_time))
                return {'path': final_path, 'cost': total_path_cost, 'nodes_expanded': expansion_count, 'time': execution_time}
            
            for neighbor_node, _ in self.env.get_neighbors(current_node):
                if neighbor_node not in explored_nodes:
                    explored_nodes.add(neighbor_node)
                    parent_tracker[neighbor_node] = current_node
                    search_queue.append(neighbor_node)
        
        execution_time = time.time() - start_timer
        return {'path': None, 'cost': float('inf'), 'nodes_expanded': expansion_count, 'time': execution_time}

    def ucs(self):
        self.performance_stats['total_searches'] += 1
        start_timer = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {'path': None, 'cost': float('inf'), 'nodes_expanded': 0, 'time': 0}
        
        priority_frontier = MyPriorityQueue()
        priority_frontier.enqueue(self.start_pos, 0)
        parent_mapping = {self.start_pos: None}
        cost_tracker = {self.start_pos: 0}
        expansion_count = 0
        
        while not priority_frontier.is_empty():
            current_node = priority_frontier.dequeue()
            expansion_count += 1
            
            if current_node == self.goal_pos:
                final_path = self._build_path_backwards(parent_mapping, current_node)
                total_cost = cost_tracker[current_node]
                execution_time = time.time() - start_timer
                self.performance_stats['successful_searches'] += 1
                self.path_history.append(('UCS', final_path, execution_time))
                return {'path': final_path, 'cost': total_cost, 'nodes_expanded': expansion_count, 'time': execution_time}
            
            for neighbor_node, move_cost in self.env.get_neighbors(current_node):
                new_total_cost = cost_tracker[current_node] + move_cost
                
                if neighbor_node not in cost_tracker or new_total_cost < cost_tracker[neighbor_node]:
                    cost_tracker[neighbor_node] = new_total_cost
                    parent_mapping[neighbor_node] = current_node
                    priority_frontier.enqueue(neighbor_node, new_total_cost)
        
        execution_time = time.time() - start_timer
        return {'path': None, 'cost': float('inf'), 'nodes_expanded': expansion_count, 'time': execution_time}

    def a_star(self):
        self.performance_stats['total_searches'] += 1
        start_timer = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {'path': None, 'cost': float('inf'), 'nodes_expanded': 0, 'time': 0}
        
        search_frontier = MyPriorityQueue()
        search_frontier.enqueue(self.start_pos, 0)
        parent_mapping = {self.start_pos: None}
        cost_tracker = {self.start_pos: 0}
        expansion_count = 0
        
        while not search_frontier.is_empty():
            current_node = search_frontier.dequeue()
            expansion_count += 1
            
            if current_node == self.goal_pos:
                final_path = self._build_path_backwards(parent_mapping, current_node)
                total_cost = cost_tracker[current_node]
                execution_time = time.time() - start_timer
                self.performance_stats['successful_searches'] += 1
                self.path_history.append(('A*', final_path, execution_time))
                return {'path': final_path, 'cost': total_cost, 'nodes_expanded': expansion_count, 'time': execution_time}
            
            for neighbor_node, move_cost in self.env.get_neighbors(current_node):
                new_total_cost = cost_tracker[current_node] + move_cost
                
                if neighbor_node not in cost_tracker or new_total_cost < cost_tracker[neighbor_node]:
                    cost_tracker[neighbor_node] = new_total_cost
                    heuristic_value = calculate_manhattan_heuristic(neighbor_node, self.goal_pos)
                    f_score = new_total_cost + heuristic_value
                    parent_mapping[neighbor_node] = current_node
                    search_frontier.enqueue(neighbor_node, f_score)
        
        execution_time = time.time() - start_timer
        return {'path': None, 'cost': float('inf'), 'nodes_expanded': expansion_count, 'time': execution_time}

    def dynamic_replanning_demo(self):
        log = []
        log.append("=== Dynamic Replanning Demo ===")
        log.append("")
        
        log.append("Step 1: Planning initial path using A*")
        initial_result = self.a_star()
        
        if not initial_result['path']:
            log.append("ERROR: No initial path found!")
            return "\n".join(log)
        
        log.append(f"Initial path found: {initial_result['path']}")
        log.append(f"Initial path cost: {initial_result['cost']}")
        log.append(f"Nodes expanded: {initial_result['nodes_expanded']}")
        log.append("")
        
        log.append("Step 2: Agent starts moving along the path")
        current_position = self.start_pos
        steps_taken = 0
        max_steps = min(4, len(initial_result['path']) - 1)
        
        for i in range(max_steps):
            if i + 1 < len(initial_result['path']):
                current_position = initial_result['path'][i + 1]
                steps_taken += 1
                log.append(f"  Step {steps_taken}: Agent moves to {current_position}")
        
        log.append(f"Agent has moved {steps_taken} steps and is now at {current_position}")
        log.append("")
        
        log.append("Step 3: Unexpected obstacle detected!")
        
        remaining_path = initial_result['path'][steps_taken + 1:]
        if remaining_path:
            obstacle_pos = remaining_path[0]
            self.env.add_dynamic_obstacle(obstacle_pos, steps_taken)
            log.append(f"Dynamic obstacle added at position {obstacle_pos}")
            log.append(f"Remaining original path: {remaining_path}")
        else:
            log.append("No remaining path to block - agent has reached the goal!")
            return "\n".join(log)
        
        log.append("")
        
        log.append("Step 4: Re-planning path from current position using A*")
        
        original_start = self.start_pos
        self.start_pos = current_position
        
        replan_result = self.a_star()
        
        self.start_pos = original_start
        
        if not replan_result['path']:
            log.append("ERROR: No replanned path found!")
            return "\n".join(log)
        
        log.append(f"Replanned path found: {replan_result['path']}")
        log.append(f"Replanned path cost: {replan_result['cost']}")
        log.append(f"Nodes expanded for replanning: {replan_result['nodes_expanded']}")
        log.append("")
        
        log.append("Step 5: Agent continues with the new path")
        log.append("Dynamic replanning demo completed successfully!")
        
        return "\n".join(log)
    
    def enable_debug_mode(self):
        self.debug_mode = True
        print("Debug mode enabled - will show search progress")
    
    def disable_debug_mode(self):
        self.debug_mode = False
        print("Debug mode disabled")
    
    def get_performance_summary(self):
        success_rate = (self.performance_stats['successful_searches'] / 
                       self.performance_stats['total_searches'] * 100) if self.performance_stats['total_searches'] > 0 else 0
        return {
            'total_searches': self.performance_stats['total_searches'],
            'successful_searches': self.performance_stats['successful_searches'],
            'success_rate': f"{success_rate:.1f}%",
            'path_history_count': len(self.path_history)
        }
    
    def clear_history(self):
        self.path_history = []
        self.performance_stats = {'total_searches': 0, 'successful_searches': 0}
        print("Performance history cleared")
