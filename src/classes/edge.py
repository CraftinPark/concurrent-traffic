import numpy as np
from .node import Node

class Edge():
    start: Node = None
    end: Node = None
    curved: bool = True
    center: np.ndarray = None # center is only required for curved edges
    radius: float = None
    clockwise: bool = None

    def __init__(self, start: Node, end: Node, curved:bool=False, center=None, clockwise: bool=False):
        self.start = start
        self.end = end
        self.curved = curved
        if self.curved == True and center.shape == None: # if shape is None, this means center has not been initialized
            raise ValueError("center point must be provided if edge is not straight")
        if center is not None:
            self.radius = np.linalg.norm(start.position - center)
            self.center = center
        self.clockwise = clockwise


def get_length(edge: Edge) -> float:
    if not edge.curved:
        return np.linalg.norm(edge.start.position - edge.end.position)
    elif edge.curved:
        radius = np.linalg.norm(edge.start.position-edge.center)
        vector_start = edge.start.position - edge.center
        vector_end = edge.end.position - edge.center
        dot_product = np.dot(vector_start, vector_end)
        magnitude_start = np.linalg.norm(vector_start)
        magnitude_end = np.linalg.norm(vector_end)
        cos_theta = dot_product / (magnitude_start * magnitude_end)

        theta = np.arccos(cos_theta)
        return theta * radius