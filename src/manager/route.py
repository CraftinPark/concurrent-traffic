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

    radius = np.linalg.norm(edge.start.position-edge.center)

    vector_start = edge.start.position - edge.center
    vector_end = edge.end.position - edge.center

    # Dot product of the vectors
    dot_product = np.dot(vector_start, vector_end)

    # Magnitudes of the vectors
    magnitude_start = np.linalg.norm(vector_start)
    magnitude_end = np.linalg.norm(vector_end)

    # Cosine of the angle
    cos_theta = dot_product / (magnitude_start * magnitude_end)

    # Angle in radians
    theta = np.arccos(cos_theta)

    return theta * radius


class Route():
    edges: list[Edge]
    total_length: float = 0
    pos_to_edge_map: dict[tuple, Edge]
    def __init__(self, edges: list[Edge]):
        self.edges = edges
        self.pos_to_edge_map = {}
        for e in self.edges:
            curr_length = get_length(e)
            self.pos_to_edge_map[(self.total_length, self.total_length + curr_length)] = e
            self.total_length += curr_length


# {
#     range(0):   edge1
#     range(20m):  edge2
#     range(45m):
# }

# pos = 30
# 30 - 20 (start) = 10
# end - start = 25
# ======> 10 / 25 = 0.4


# r / route.total_length             x,y
def route_position_to_world_position(route: Route, position: float):
    edge_of_position = None
    percentage_on_edge = None
    for r in route.pos_to_edge_map:
        if position < r[1] and position >= r[0]:
            print(r)
            edge_of_position = route.pos_to_edge_map[r]
            percentage_on_edge = (position - r[0]) / (r[1] - r[0])
            break
    if edge_of_position is None:
        return [0, 0]
    if not edge_of_position.curved:
        # parametric equations
        if r == (74.0, 86.0):
            pass
        world_x = (1-percentage_on_edge)*edge_of_position.start.position[0] + percentage_on_edge*edge_of_position.end.position[0]
        world_y = (1-percentage_on_edge)*edge_of_position.start.position[1] + percentage_on_edge*edge_of_position.end.position[1]
    else:
        print("im in curved")
        # curved behavior
        theta_start = np.arctan2(edge_of_position.start.position[1] - edge_of_position.center[1], edge_of_position.start.position[0] - edge_of_position.center[0])
        theta_end   = np.arctan2(edge_of_position.end.position[1] - edge_of_position.center[1], edge_of_position.end.position[0] - edge_of_position.center[0])

        if edge_of_position.clockwise:
            theta_of_pos = theta_start + percentage_on_edge * (theta_start - theta_end)
        else:
            theta_of_pos = theta_start + percentage_on_edge * (theta_end - theta_start)

        world_x = edge_of_position.center[0] + edge_of_position.radius * np.cos(theta_of_pos)
        world_y = edge_of_position.center[1] + edge_of_position.radius * np.sin(theta_of_pos)
        print(f"radius: {edge_of_position.radius}")
        print(f"world_x: {world_x}")
        print(f"world_y: {world_y}")
    
    return [world_x, world_y]