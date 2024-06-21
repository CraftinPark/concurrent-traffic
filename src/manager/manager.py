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