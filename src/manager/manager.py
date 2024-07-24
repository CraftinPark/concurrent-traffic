import numpy as np
from classes.vehicle import Vehicle, update_cmd
from classes.route import Route, route_position_to_world_position
from itertools import combinations
from scipy.optimize import minimize_scalar
from random import randint

CAR_COLLISION_DISTANCE = 2.5 # meters

class Collision:
    """A Collision represents a collision between two Vehicles at a given time."""
    vehicle0: Vehicle
    vehicle1: Vehicle
    time: float

    def __init__(self, vehicle0: Vehicle, vehicle1: Vehicle, time: float) -> None:
        self.vehicle0 = vehicle0
        self.vehicle1 = vehicle1
        self.time = time

class Manager:
    """A Manager controls all Vehicles within its radius, calculating and sending commands to ensure that Vehicles do
    not collide with each other."""
    position: np.ndarray
    radius: float = 25
    vehicles: list[Vehicle] = []
    intersecting_points = None
    collisions: list[Collision] = []

    def __init__(self, position: np.ndarray, radius: float, routes: list[Route]) -> None:
        # initialize
        self.position = position
        self.radius = radius

def reset(manager: Manager) -> None:
    """Clear manager.vehicles attribute."""
    manager.vehicles.clear()

def manager_event_loop(manager: Manager, vehicles: list[Vehicle], cur_time: float) -> None:
    """Event loop for Manager. Updates manager.vehicles if a Vehicle enters its radius. Also recalculates and sends Commands on update of manager.vehicles."""
    if _update_manager_vehicle_list(manager, vehicles):
        _compute_and_send_acceleration_commands(manager, cur_time)
        manager.collisions = get_collisions(manager.vehicles, cur_time)

def _update_manager_vehicle_list(manager: Manager, vehicles: list[Vehicle]) -> bool:
    """Return True if new vehicles have been added to manager.vehicles."""
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

def get_collisions(vehicles: list[Vehicle], cur_time: float) -> list[Collision]:
    """Return list of Collisions between Vehicles in manager's radius."""
    collisions = []
    vehicle_pairs = combinations(vehicles, 2)
    
    for vehicle_pair in vehicle_pairs:
        vehicle_out_of_bounds_time = int(min(time_until_end_of_route(vehicle_pair[0]), time_until_end_of_route(vehicle_pair[1])))
        def distance_objective(t):
            wp0 = route_position_to_world_position(vehicle_pair[0].route, route_position_at_time(vehicle_pair[0], t, cur_time))
            wp1 = route_position_to_world_position(vehicle_pair[1].route, route_position_at_time(vehicle_pair[1], t, cur_time))
            return np.linalg.norm(wp1-wp0) - CAR_COLLISION_DISTANCE
        
        result = minimize_scalar(distance_objective, bounds=(0, vehicle_out_of_bounds_time), method='bounded')
        if result.success:
            time_of_collision = result.x + cur_time
            # print(f"The objects come within 2.5 meters of each other at t = {time_of_collision}")
            # print(f"{vehicle_pair[0].name}: {route_position_to_world_position(vehicle_pair[0].route, route_position_at_time(vehicle_pair[0], result.x, cur_time))}")
            # print(f"{vehicle_pair[1].name}: {route_position_to_world_position(vehicle_pair[1].route, route_position_at_time(vehicle_pair[1], result.x, cur_time))}")
            collisions.append(Collision(vehicle_pair[0], vehicle_pair[1], time_of_collision))
    return collisions

def route_position_at_time(vehicle: Vehicle, delta_time: float, cur_time: float) -> float:
    """Return vehicle's route position along its Route after delta_time seconds has passed."""
    # return vehicle.route_position + vehicle.velocity * delta_time
    distance = vehicle.route_position
    velocity = vehicle.velocity
    time = cur_time + delta_time
    
    if len(vehicle.command.accel_func.x) == 1:
        time_diff = time - vehicle.command.accel_func.x[0]
        distance = velocity * time_diff + 1/2 * vehicle.command.accel_func.y[0] * time_diff**2

    for i in range(len(vehicle.command.accel_func.x) - 1):
        if vehicle.command.accel_func.x[i+1] < time:
            time_diff = vehicle.command.accel_func.x[i+1] - vehicle.command.accel_func.x[i]
        else:
            time_diff = time - vehicle.command.accel_func.x[i]

        distance += velocity * time_diff + 1/2 * vehicle.command.accel_func.y[i] * time_diff**2
        velocity += vehicle.command.accel_func.y[i] * time_diff

        if vehicle.command.accel_func.x[i+1] > time:
            break

    return distance

def time_until_end_of_route(vehicle: Vehicle) -> float:
    """Return time til vehicle reaches the end of its route."""
    return (vehicle.route.total_length - vehicle.route_position) / vehicle.velocity

# def collision_preventing_adjustment():
#     # adjustment must be a timed acceleration/deceleration
#     return

def _compute_and_send_acceleration_commands(manager: Manager, elapsed_time: float) -> None:
    """Compute and send commands."""
    for v in manager.vehicles:
        t, a = _compute_command(elapsed_time)
        # if v.name == "acc":
        #     v.command = update_cmd(v.command, t, a, elapsed_time) # this will make cars crash for presets/collision_by_command.json
        v.command = update_cmd(v.command, t, a, elapsed_time)

def _compute_command(elapsed_time: float) -> tuple[np.array, np.array]:
    """Return np.array of acceleration and time values."""
    # t = [elapsed_time, elapsed_time + 2.5] # this will make cars crash for presets/collision_by_command.json
    # a = [0, 6]
    t = [elapsed_time, elapsed_time + randint(1, 3), elapsed_time + randint(3, 5)]
    a = [randint(1, 3), randint(-3, 3), 3]
    return np.array(t), np.array(a)