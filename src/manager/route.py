import numpy as np
from .edge import Edge, get_length  

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

def route_position_to_world_position(route: Route, position: float):
    edge_of_position = None
    percentage_on_edge = None
    for r in route.pos_to_edge_map:
        if position < r[1] and position >= r[0]:
            edge_of_position = route.pos_to_edge_map[r]
            percentage_on_edge = (position - r[0]) / (r[1] - r[0])
            break
    if edge_of_position is None:
        return [-100, -100]
    if not edge_of_position.curved:
        world_x = (1-percentage_on_edge)*edge_of_position.start.position[0] + percentage_on_edge*edge_of_position.end.position[0]
        world_y = (1-percentage_on_edge)*edge_of_position.start.position[1] + percentage_on_edge*edge_of_position.end.position[1]
    else:
        theta_start = np.arctan2(edge_of_position.start.position[1] - edge_of_position.center[1], edge_of_position.start.position[0] - edge_of_position.center[0])
        theta_end   = np.arctan2(edge_of_position.end.position[1] - edge_of_position.center[1], edge_of_position.end.position[0] - edge_of_position.center[0])

        if edge_of_position.clockwise:
            if theta_end < theta_start:
                theta_end += 2*np.pi
        else:
            if theta_start < theta_end:
                theta_start += 2*np.pi

        theta_of_pos = theta_start + percentage_on_edge * (theta_end - theta_start)
        world_x = edge_of_position.center[0] + edge_of_position.radius * np.cos(theta_of_pos)
        world_y = edge_of_position.center[1] + edge_of_position.radius * np.sin(theta_of_pos)
    
    return [world_x, world_y]