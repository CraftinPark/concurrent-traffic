from __future__ import annotations # this enables Node from using declarations of Edge that come afterward
import numpy as np

class Node():
    position: np.ndarray = np.array([0,0])
    in_edges: list[Edge] = []
    out_edges: list[Edge] = []

    def __init__(self, position: list):
        self.position = position

def add_in_edge(self, node: Node, edge: Edge):
    node.in_edges.append(edge)

def add_out_edge(self, node: Node, edge: Edge):
    node.out_edges.append(edge)

class Edge():
    start: Node = None
    end: Node = None
    curved: bool = True
    center: np.ndarray = None # center is only required for curved edges

    def __init__(self, start: Node, end: Node, curved:bool=False, center=None, clockwise: bool=False):
        self.start = start
        self.end = end
        self.curved = curved
        if self.curved == True and center.shape == None: # if shape is None, this means center has not been initialized
            raise ValueError("center point must be provided if edge is not straight")
        self.center = center

        
def get_length(edge: Edge) -> float:
    if not edge.curved:
        return np.linalg.norm(edge.start.position - edge.end.position)

    radius = np.linalg.norm(edge.start.position-edge.center)

    vector_start = edge.start.position - edge.center.position
    vector_end = edge.end.position - edge.center.position

    # Dot product of the vectors
    dot_product = np.dot(vector_start, vector_end)

    # Magnitudes of the vectors
    magnitude_start = np.linalg.norm(vector_start)
    magnitude_end = np.linalg.norm(vector_end)

    # Cosine of the angle
    cos_theta = dot_product / (magnitude_start * magnitude_end)

    # Angle in radians
    theta = np.arccos(cos_theta)

    if edge.clockwise:
        theta = 2 * np.pi - theta

    return theta * radius


class Route():
    edges: list[Edge] = []
    length: float
    def __init__(self, edges: list[Edge]):
        self.edges = edges
        for e in self.edges:
            length += get_length(e)

def route_position_to_world_position(route: Route, position: float):
    return [0,0]