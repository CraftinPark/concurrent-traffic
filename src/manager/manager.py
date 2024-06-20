import numpy as np
from classes.vehicle import Vehicle
from .command import Command
from classes.route import Route, route_position_to_world_position, world_position_to_route_position
from classes.edge import Edge, CircularEdge
from classes.node import Node
import sympy
from sympy import Point2D

class Manager:
    position: np.ndarray
    radius: float = 25
    vehicles: list[Vehicle] = []
    intersecting_points = None

    def __init__(self, position: np.ndarray, radius: float, routes: list[Route]):
        # initialize
        self.position = position
        self.radius = radius
        self.intersecting_points = calculate_intersecting_points(routes)

    def reset(self):
        self.vehicles.clear()

    # def distance_between(vehicle: Vehicle, line) -> float:
    #     return np.abs(vehicle.pos[0]*line[0]+vehicle.pos[1]*line[1]+line[2])/np.sqrt(np.square(line[0])+np.square(line[1]))

# helpers
# def get_collisions():
#     # list of collisions
#     # maybe have car with priority first and other car second
#     return

# def collision_preventing_adjustment():
#     # adjustment must be a timed acceleration/deceleration
#     return

# 1. print pretty and see routes of intersection
# 2. filter out the intersections that aren't in the right range
# 3. correct return with route_position?
# i going cuz sister picking me up
# i need to cap it
# are u able to wrap up
# i can get back on in like 5ish min
# but i am cooking dinner too
# im good
# cyu cya

def get_intersections(route1: Route, route2: Route, edge1: Edge, edge2: Edge) -> set[int, int, tuple[Point2D]]: # route_position on r1, route_position on r2
    intersections = set(sympy.intersection(edge1.sympy_obj, edge2.sympy_obj))
    first, second = sorted([route1.current_id, route2.current_id])
    if isinstance(edge1, CircularEdge):
        intersections.intersection_update(check_circle(edge1, intersections))
    if isinstance(edge2, CircularEdge):
        intersections.intersection_update(check_circle(edge2, intersections))

    result = set()
    for i in intersections:
        intersect_node = Node(np.array([float(i.x), float(i.y)]))
        intersection = (first, second, intersect_node)
        result.add(intersection)

    return result

def check_circle(edge: CircularEdge, intersections: list[Point2D]):
    start_angle = np.arctan2(edge.start.position[1] - edge.center[1], edge.start.position[0] - edge.center[0]) + np.pi
    end_angle = np.arctan2(edge.end.position[1] - edge.center[1], edge.end.position[0] - edge.center[0]) + np.pi
    true_intersects = set()
    for i in intersections:
        i_angle = np.arctan2(float(i.y) - edge.center[1], float(i.x) - edge.center[0]) + np.pi
        if is_angle_between(start_angle, end_angle, i_angle, edge.clockwise):
            true_intersects.add(i)
    return true_intersects

def normalize_angle(angle):
    while angle > np.pi:
        angle -= 2 * np.pi
    while angle <= -np.pi:
        angle += 2 * np.pi
    return angle

def is_angle_between(theta_1, theta_2, theta_3, clockwise):
    theta_1 = normalize_angle(theta_1)
    theta_2 = normalize_angle(theta_2)
    theta_3 = normalize_angle(theta_3)

    if (theta_1 <= theta_2 and not clockwise) or (theta_1 >= theta_2 and clockwise):
        return theta_1 <= theta_3 <= theta_2
    else:
        return theta_3 >= theta_1 or theta_3 <= theta_2

def calculate_intersecting_points(routes: list[Route]):
    routes_set = set(routes)
    lst = set()
    for r1 in routes_set:
        for e1 in r1.edges:
            for r2 in (routes_set - set([r1])):
                for e2 in (set(r2.edges) - set([e1])):
                    intersections = get_intersections(r1,r2,e1,e2)
                    if intersections:
                        lst.update(intersections)
    # count = 0
    # for i in lst:
    #     count += 1
    #     print(f"r1:{i[0]} r2:{i[1]} points:{i[2]}")
    # print(count)
    return lst

def manager_event_loop(manager: Manager, vehicles: list[Vehicle], time: float):
    _update_manager_vehicle_list(manager, vehicles)
    _compute_and_send_acceleration_commands(manager, vehicles)

def _update_manager_vehicle_list(manager: Manager, vehicles: list[Vehicle]):
    for vehicle in vehicles:

        # vehicle within manager radius? 
        distance_to_vehicle = np.linalg.norm(route_position_to_world_position(vehicle.route, vehicle.route_position)-manager.position)

        # vehicle already in list and within manager radius?
        vehicle_in_list = any(manager_vehicle.id == vehicle.id for manager_vehicle in manager.vehicles)

        # append if not in list and inside radius
        if not vehicle_in_list and distance_to_vehicle <= manager.radius: 
            manager.vehicles.append(vehicle)

        # remove if in list and outside radius
        elif vehicle_in_list and distance_to_vehicle > manager.radius: 
            manager.vehicles.remove(vehicle)

def _compute_and_send_acceleration_commands(manager: Manager, vehicles: list[Vehicle]):
    for vehicle in manager.vehicles:
        if vehicle.command == None:
            command = _compute_command()
            vehicle.command = command
            pass

def _compute_command() -> Command:
    # TODO
    return