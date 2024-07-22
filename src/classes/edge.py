import numpy as np
from .node import Node
from sympy import Segment, Circle, Point
from standard_traffic.traffic_light import TrafficState

class Edge():
    """This is an abstract class for Edges. An Edge consists of a start node and an end node."""
    start: Node = None
    end: Node = None
    edge_id: str
    sympy_obj: Segment | Circle = None
    traffic_state: TrafficState

    def __init__(self, edge_id: str, start: Node, end: Node, traffic_state: TrafficState) -> None:
        self.start = start
        self.end = end
        self.edge_id = edge_id
        self.traffic_state = traffic_state
    
    def change_state(self, state:TrafficState):
        self.traffic_state = state

    def get_state(self):
        return self.traffic_state

class StraightEdge(Edge):
    """A StraightEdge is an Edge that is linear."""

    def __init__(self, edge_id, start: Node, end: Node, traffic_state: TrafficState) -> None:
        Edge.__init__(self, edge_id, start, end, traffic_state)
        self.sympy_obj = Segment(Point(start.position[0], start.position[1]), Point(end.position[0], end.position[1]))
        
class CircularEdge(Edge):
    """A CircularEdge is an Edge that is curved around a center point."""
    center: Node
    radius: float
    clockwise: bool

    def __init__(self, edge_id: str, start: Node, end: Node, center: np.ndarray, traffic_state: TrafficState, clockwise: bool=False) -> None:
        Edge.__init__(self, edge_id, start, end, traffic_state)
        self.radius = np.linalg.norm(start.position - center)
        self.center = center
        self.clockwise = clockwise
        self.sympy_obj = Circle(Point(center[0], center[1]), self.radius)

def get_length(edge: Edge) -> float:
    """Return length of edge."""
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

    raise TypeError("get_length returned None.")