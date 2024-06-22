import numpy as np
from classes.vehicle import Vehicle
from manager.command import Command
from classes.route import Route, route_position_to_world_position, world_position_to_route_position
from classes.edge import Edge, CircularEdge
from classes.node import Node
import sympy
from sympy import Point2D
from itertools import combinations

def get_edge_intersections(route1: Route, route2: Route, edge1: Edge, edge2: Edge) -> set[int, int, tuple[float, float]]: # route_position on r1, route_position on r2
    intersections = set(sympy.intersection(edge1.sympy_obj, edge2.sympy_obj))
    if isinstance(edge1, CircularEdge):
        remove_false_circle_intersects(edge1, intersections)
    if isinstance(edge2, CircularEdge):
       remove_false_circle_intersects(edge2, intersections)

    result = set()

    for i in intersections:
        intersection = (route1.current_id, route2.current_id, (float(i.x), float(i.y)))
        result.add(intersection)

    return result

def remove_false_circle_intersects(edge: CircularEdge, intersections: list[Point2D]) -> None:
    start_angle = np.arctan2(-(edge.start.position[1] - edge.center[1]), edge.start.position[0] - edge.center[0])
    end_angle = np.arctan2(-(edge.end.position[1] - edge.center[1]), edge.end.position[0] - edge.center[0])

    to_remove = set()

    for i in intersections:
        i_angle = np.arctan2(-(float(i.y) - edge.center[1]), float(i.x) - edge.center[0])
        if not is_angle_between(start_angle, end_angle, i_angle, edge.clockwise):
           to_remove.add(i)

    intersections.difference_update(to_remove)

def is_angle_between(start_angle: float, end_angle: float, i_angle: float, clockwise: bool) -> bool:

    if start_angle <= end_angle and not clockwise:
        return start_angle <= i_angle <= end_angle
    
    elif start_angle <= end_angle and clockwise:
        return i_angle <= start_angle or i_angle >= end_angle
    
    elif start_angle >= end_angle and clockwise:
        return end_angle <= i_angle <= start_angle
    
    elif start_angle >= end_angle and not clockwise:
        return i_angle <= end_angle or i_angle >= start_angle

def get_intersections(routes: list[Route]):

    intersections = set()

    for r1, r2 in combinations(routes, 2):
        for e1 in r1.edges:
            for e2 in r2.edges:
                if e1 is e2:
                    continue
                intersections.update(get_edge_intersections(r1, r2, e1, e2))

    return intersections