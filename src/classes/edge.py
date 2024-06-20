import numpy as np
from .node import Node
from sympy import Segment, Circle, Point

class Edge():
    start: Node = None
    end: Node = None
    sympy_obj: Segment | Circle = None

    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end

class StraightEdge(Edge):
    def __init__(self, start: Node, end: Node):
        Edge.__init__(self, start, end)
        self.sympy_obj = Segment(Point(start.position[0], start.position[1]), Point(end.position[0], end.position[1]))
        
class CircularEdge(Edge):
    center: Node
    radius: float
    clockwise: bool

    def __init__(self, start: Node, end: Node, center: np.ndarray, clockwise: bool=False):
        Edge.__init__(self, start, end)
        self.radius = np.linalg.norm(start.position - center)
        self.center = center
        self.clockwise = clockwise
        self.sympy_obj = Circle(Point(center[0], center[1]), self.radius)

def get_length(edge: Edge) -> float:
    if isinstance(edge, StraightEdge):
        return np.linalg.norm(edge.start.position - edge.end.position)
    elif isinstance(edge, CircularEdge):
        radius = np.linalg.norm(edge.start.position-edge.center)
        vector_start = edge.start.position - edge.center
        vector_end = edge.end.position - edge.center
        dot_product = np.dot(vector_start, vector_end)
        magnitude_start = np.linalg.norm(vector_start)
        magnitude_end = np.linalg.norm(vector_end)
        cos_theta = dot_product / (magnitude_start * magnitude_end)

        theta = np.arccos(cos_theta)
        return theta * radius