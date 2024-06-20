import numpy as np
from classes.vehicle import Vehicle
from .command import Command
from classes.route import Route, route_position_to_world_position
from classes.edge import Edge, StraightEdge, CircularEdge
from sympy import Point, intersection

class Manager:
    position: Point = (0,0)
    radius: float = 25
    vehicles: list[Vehicle] = []

    def __init__(self, position: Point, radius: float, routes: list[Route]):
        # initialize
        self.position = position
        self.radius = radius
        calculate_intersecting_points(routes)

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
#


def get_intersections(route1: Route, route2: Route, edge1: Edge, edge2: Edge) -> tuple[float, float]: # route_position on r1, route_position on r2
    result = intersection(edge1.sympy_obj, edge2.sympy_obj)
    return result

def calculate_intersecting_points(routes: list[Route]):
    routes_set = set(routes)
    lst = []
    for r1 in routes_set:
        for e1 in r1.edges:
            for r2 in (routes_set - set([r1])):
                for e2 in (set(r2.edges) - set([e1])):
                    intersections = get_intersections(r1,r2,e1,e2)
                    if intersections:
                        lst.append(intersections)
    print(intersections)
    return lst

def manager_event_loop(manager: Manager, vehicles: list[Vehicle], time: float):
    _update_manager_vehicle_list(manager, vehicles)
    _compute_and_send_acceleration_commands(manager, vehicles)

def _update_manager_vehicle_list(manager: Manager, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        # vehicle already in list?
        vehicle_in_list = any(manager_vehicle.id == vehicle.id for manager_vehicle in manager.vehicles)
        if vehicle_in_list: continue

        # vehicle within manager radius?
        distance_to_vehicle = np.linalg.norm(route_position_to_world_position(vehicle.route, vehicle.route_position)-manager.position)
        if distance_to_vehicle > manager.radius: continue

        # vehicle is not in list and within radius, add to list
        manager.vehicles.append(vehicle)

def _compute_and_send_acceleration_commands(manager: Manager, vehicles: list[Vehicle]):
    for vehicle in manager.vehicles:
        if vehicle.command == None:
            command = _compute_command()
            vehicle.command = command
            pass

def _compute_command() -> Command:
    # TODO
    return