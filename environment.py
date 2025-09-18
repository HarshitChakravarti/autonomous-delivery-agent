# environment.py

class GridCity:
    def __init__(self, map_filepath):
        """
        Initializes the environment from a map file.
        - self.grid: 2D list representing terrain costs.
        - self.width, self.height: Dimensions of the grid.
        - self.start_pos, self.goal_pos: (row, col) tuples.
        - self.static_obstacles: A set of (row, col) tuples.
        - self.dynamic_obstacles: A dict mapping time_step -> [(row, col), ...].
                                  For this project, we can hardcode a simple schedule.
        """
        self.grid = []
        self.static_obstacles = set()
        self.dynamic_obstacles = {}
        self.start_pos = None
        self.goal_pos = None
        
        # Load map from file
        self._load_map(map_filepath)
        
        # Set up dynamic obstacles for demonstration
        self._setup_dynamic_obstacles()
    
    def _load_map(self, map_filepath):
        """Load the map from a text file."""
        with open(map_filepath, 'r') as file:
            lines = file.readlines()
        
        for row, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            grid_row = []
            for col, char in enumerate(line):
                if char == 'S':
                    self.start_pos = (row, col)
                    grid_row.append(1)  # Start position has cost 1
                elif char == 'G':
                    self.goal_pos = (row, col)
                    grid_row.append(1)  # Goal position has cost 1
                elif char == '#':
                    self.static_obstacles.add((row, col))
                    grid_row.append(float('inf'))  # Impassable
                elif char == '.' or char == '1':
                    grid_row.append(1)  # Standard terrain
                elif char.isdigit() and char != '0':
                    grid_row.append(int(char))  # Difficult terrain
                else:
                    grid_row.append(1)  # Default to standard terrain
            
            self.grid.append(grid_row)
        
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
    
    def _setup_dynamic_obstacles(self):
        """Set up dynamic obstacles for demonstration purposes."""
        # Add some dynamic obstacles that appear at specific time steps
        # This is for the dynamic replanning demo
        self.dynamic_obstacles = {
            3: [(1, 2)],  # Obstacle appears at time step 3
            5: [(2, 1), (2, 2)],  # More obstacles at time step 5
        }
    
    def get_cost(self, position):
        """Returns the movement cost for a given cell."""
        row, col = position
        if not self.is_valid(position):
            return float('inf')
        return self.grid[row][col]
    
    def is_valid(self, position):
        """Checks if a position is within the grid boundaries."""
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width
    
    def is_obstacle(self, position, time_step=0):
        """
        Checks if a cell is an obstacle (static or dynamic at a given time).
        """
        if not self.is_valid(position):
            return True
        
        # Check static obstacles
        if position in self.static_obstacles:
            return True
        
        # Check dynamic obstacles at the given time step
        if time_step in self.dynamic_obstacles:
            if position in self.dynamic_obstacles[time_step]:
                return True
        
        return False
    
    def get_neighbors(self, position):
        """
        Returns a list of valid, 4-connected neighbors for a given position.
        Returns [(neighbor_pos, cost), ...].
        """
        row, col = position
        neighbors = []
        
        # Define 4-connected movement (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self.is_valid(new_pos) and not self.is_obstacle(new_pos):
                cost = self.get_cost(new_pos)
                neighbors.append((new_pos, cost))
        
        return neighbors
    
    def add_dynamic_obstacle(self, position, time_step):
        """Add a dynamic obstacle at a specific time step."""
        if time_step not in self.dynamic_obstacles:
            self.dynamic_obstacles[time_step] = []
        self.dynamic_obstacles[time_step].append(position)
    
    def remove_dynamic_obstacle(self, position, time_step):
        """Remove a dynamic obstacle at a specific time step."""
        if time_step in self.dynamic_obstacles:
            if position in self.dynamic_obstacles[time_step]:
                self.dynamic_obstacles[time_step].remove(position)
                if not self.dynamic_obstacles[time_step]:
                    del self.dynamic_obstacles[time_step]
