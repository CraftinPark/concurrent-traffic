import numpy as np
from classes.vehicle import Vehicle
from manager.command import Command
from classes.route import Route, route_position_to_world_position, world_position_to_route_position
from classes.edge import Edge, CircularEdge
from classes.node import Node
import sympy
from sympy import Point2D

def get_edge_intersections(route1: Route, route2: Route, edge1: Edge, edge2: Edge) -> set[int, int, tuple[Point2D]]: # route_position on r1, route_position on r2
    intersections = set(sympy.intersection(edge1.sympy_obj, edge2.sympy_obj))
    first, second = sorted([route1.current_id, route2.current_id])
    if isinstance(edge1, CircularEdge):
        intersections.intersection_update(check_circle(edge1, intersections, route1, route2, edge2))
    if isinstance(edge2, CircularEdge):
        intersections.intersection_update(check_circle(edge2, intersections, route2, route1, edge1))

    result = set()
    for i in intersections:
        intersect_node = Node(np.array([float(i.x), float(i.y)]))
        intersection = (first, second, intersect_node)
        result.add(intersection)

    return result

def check_circle(edge: CircularEdge, intersections: list[Point2D],route, other, other_edge):
    start_angle = normalize_angle(np.arctan2((edge.start.position[1] - edge.center[1]), edge.start.position[0] - edge.center[0]))
    end_angle = normalize_angle(np.arctan2((edge.end.position[1] - edge.center[1]), edge.end.position[0] - edge.center[0]))

    if edge.clockwise:
        if end_angle < start_angle:
            end_angle += 2*np.pi
    else:
        if start_angle < end_angle:
            start_angle += 2*np.pi

    true_intersects = set()
    for i in intersections:
        i_angle = normalize_angle(np.arctan2((float(i.y) - edge.center[1]), (float(i.x) - edge.center[0])))
        if is_angle_between(start_angle, end_angle, i_angle, edge.clockwise):
            true_intersects.add(i)
    return true_intersects

def normalize_angle(angle):
    while angle > np.pi:
        angle -= 2 * np.pi
    while angle <= -np.pi:
        angle += 2 * np.pi
    return angle

def is_angle_between(start_angle, end_angle, i_angle, clockwise):

    theta_1, theta_2 = sorted([start_angle, end_angle])

    if (start_angle <= end_angle and not clockwise) or (start_angle >= end_angle and not clockwise):
        return theta_1 <= i_angle <= theta_2
    elif (start_angle >= end_angle and clockwise) or (start_angle <= end_angle and clockwise):
        return i_angle >= theta_1 or i_angle <= theta_2

def get_intersections(routes: list[Route]):
    routes_set = set(routes)
    intersections = set()
    for r1 in routes_set:
        for e1 in r1.edges:
            for r2 in (routes_set - set([r1])):
                for e2 in (set(r2.edges) - set([e1])):
                    edge_intersections = get_edge_intersections(r1,r2,e1,e2)
                    if edge_intersections:
                        intersections.update(edge_intersections)
    # count = 0
    # for i in lst:
    #     count += 1
    #     print(f"r1:{i[0]} r2:{i[1]} points:{i[2]}")
    # print(count)
    return intersections