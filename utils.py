# Utility functions including priority queue implementation and Manhattan distance heuristic
import heapq

class MyPriorityQueue:
    def __init__(self):
        self.heap_data = []
        self._counter = 0

    def is_empty(self):
        return len(self.heap_data) == 0

    def enqueue(self, item, priority):
        self._counter += 1
        heapq.heappush(self.heap_data, (priority, self._counter, item))

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return heapq.heappop(self.heap_data)[2]

def calculate_manhattan_heuristic(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return abs(x1 - x2) + abs(y1 - y2)
