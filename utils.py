# utils.py
import heapq

class PriorityQueue:
    """A simple priority queue for UCS and A*."""
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def manhattan_distance(pos1, pos2):
    """
    Admissible heuristic for A*: Manhattan distance.
    Assumes a minimum movement cost of 1.
    """
    (x1, y1) = pos1
    (x2, y2) = pos2
    return abs(x1 - x2) + abs(y1 - y2)
