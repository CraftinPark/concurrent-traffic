import numpy as np
from classes.vehicle import Vehicle
from .command import Command

class Manager:
    position: np.ndarray = [0,0]
    radius: float = 25
    vehicles: list[Vehicle] = []

    def __init__(self, position: np.ndarray, radius: float):
        # initialize
        self.position = position
        self.radius = radius
        print("manager initialized")

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

def manager_event_loop(manager: Manager, vehicles: list[Vehicle], time: float):
    _update_manager_vehicle_list(manager, vehicles)
    _compute_and_send_acceleration_commands(manager, vehicles)
    
def _update_manager_vehicle_list(manager: Manager, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        # vehicle already in list?
        vehicle_in_list = any(manager_vehicle.id == vehicle.id for manager_vehicle in manager.vehicles)
        if vehicle_in_list: continue

        # vehicle within manager radius?
        distance_to_vehicle = np.linalg.norm(vehicle.position-manager.position)
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