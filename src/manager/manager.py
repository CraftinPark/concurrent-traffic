import numpy as np
from classes.vehicle import Vehicle
from .command import Command
from classes.route import Route, route_position_to_world_position, world_position_to_route_position
from itertools import combinations
from scipy.optimize import minimize_scalar

class Manager:
    position: np.ndarray
    radius: float = 25
    vehicles: list[Vehicle] = []
    intersecting_points = None
    collisions: list = []

    def __init__(self, position: np.ndarray, radius: float, routes: list[Route]):
        # initialize
        self.position = position
        self.radius = radius

    def reset(self):
        self.vehicles.clear()

def manager_event_loop(manager: Manager, vehicles: list[Vehicle], cur_time: float):
    if _update_manager_vehicle_list(manager, vehicles):
        manager.collisions = get_collisions(manager, cur_time)
    _compute_and_send_acceleration_commands(manager, vehicles)

def _update_manager_vehicle_list(manager: Manager, vehicles: list[Vehicle]):
    new_vehicle = False
    for vehicle in vehicles:

        # vehicle within manager radius? 
        distance_to_vehicle = np.linalg.norm(route_position_to_world_position(vehicle.route, vehicle.route_position)-manager.position)

        # vehicle already in list and within manager radius?
        vehicle_in_list = any(manager_vehicle.id == vehicle.id for manager_vehicle in manager.vehicles)

        # append if not in list and inside radius
        if not vehicle_in_list and distance_to_vehicle <= manager.radius: 
            manager.vehicles.append(vehicle)
            new_vehicle = True

        # remove if in list and outside radius
        elif vehicle_in_list and distance_to_vehicle > manager.radius: 
            manager.vehicles.remove(vehicle)
    return new_vehicle

def get_collisions(manager: Manager, cur_time: float):
    collisions = []
    vehicle_pairs = combinations(manager.vehicles, 2)
    threshold_distance = 2.5 # will be replaced by Alex's defined safety radius
    
    for vehicle_pair in vehicle_pairs:
        vehicle_out_of_bounds_time = int(min(time_until_end_of_route(vehicle_pair[0]), time_until_end_of_route(vehicle_pair[1])))
        def world_pos_0(t):
            return route_position_to_world_position(vehicle_pair[0].route, route_position_at_time(vehicle_pair[0], t))
        def world_pos_1(t):
            return route_position_to_world_position(vehicle_pair[1].route, route_position_at_time(vehicle_pair[1], t))
        def distance(t):
            wp0 = world_pos_0(t)
            wp1 = world_pos_1(t)
            return np.linalg.norm(wp1-wp0)
        def objective(t):
            return distance(t) - threshold_distance
        
        result = minimize_scalar(objective, bounds=(0,vehicle_out_of_bounds_time), method='bounded')
        if result.success and distance(result.x) <= threshold_distance:
            time_of_collision = result.x + cur_time
            # print(f"The objects come within 2.5 meters of each other at t = {time_of_collision}")
            collisions.append({"vehicle0": vehicle_pair[0], "vehicle1": vehicle_pair[1], "time": time_of_collision})
    return collisions

def route_position_at_time(vehicle: Vehicle, time: float):
    return vehicle.route_position + vehicle.velocity * time

def time_until_end_of_route(vehicle: Vehicle):
    return (vehicle.route.total_length - vehicle.route_position) / vehicle.velocity

# def collision_preventing_adjustment():
#     # adjustment must be a timed acceleration/deceleration
#     return

def _compute_and_send_acceleration_commands(manager: Manager, vehicles: list[Vehicle]):
    for vehicle in manager.vehicles:
        if vehicle.command == None:
            command = _compute_command()
            vehicle.command = command
            pass

def _compute_command() -> Command:
    # TODO
    return