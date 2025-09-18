class GridCity:
    def __init__(self, map_filepath):
        self.grid = []
        self.static_obstacles = set()
        self.dynamic_obstacles = {}
        self.start_pos = None
        self.goal_pos = None
        
        self._load_map(map_filepath)
        self._setup_dynamic_obstacles()
    
    def _load_map(self, map_filepath):
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
                    grid_row.append(1)
                elif char == 'G':
                    self.goal_pos = (row, col)
                    grid_row.append(1)
                elif char == '#':
                    self.static_obstacles.add((row, col))
                    grid_row.append(float('inf'))
                elif char == '.' or char == '1':
                    grid_row.append(1)
                elif char.isdigit() and char != '0':
                    grid_row.append(int(char))
                else:
                    grid_row.append(1)
            
            self.grid.append(grid_row)
        
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
    
    def _setup_dynamic_obstacles(self):
        self.dynamic_obstacles = {
            3: [(1, 2)],
            5: [(2, 1), (2, 2)],
        }
    
    def get_cost(self, position):
        row, col = position
        if not self.is_valid(position):
            return float('inf')
        return self.grid[row][col]
    
    def is_valid(self, position):
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width
    
    def is_obstacle(self, position, time_step=0):
        if not self.is_valid(position):
            return True
        
        if position in self.static_obstacles:
            return True
        
        if time_step in self.dynamic_obstacles:
            if position in self.dynamic_obstacles[time_step]:
                return True
        
        return False
    
    def get_neighbors(self, position):
        row, col = position
        neighbors = []
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self.is_valid(new_pos) and not self.is_obstacle(new_pos):
                cost = self.get_cost(new_pos)
                neighbors.append((new_pos, cost))
        
        return neighbors
    
    def add_dynamic_obstacle(self, position, time_step):
        if time_step not in self.dynamic_obstacles:
            self.dynamic_obstacles[time_step] = []
        self.dynamic_obstacles[time_step].append(position)
    
    def remove_dynamic_obstacle(self, position, time_step):
        if time_step in self.dynamic_obstacles:
            if position in self.dynamic_obstacles[time_step]:
                self.dynamic_obstacles[time_step].remove(position)
                if not self.dynamic_obstacles[time_step]:
                    del self.dynamic_obstacles[time_step]
