import numpy as np
from classes.vehicle import Vehicle

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

    # def update_distance_to_intersection(vehicle: Vehicle):
    #     if   vehicle.dir == Direction.NORTH_BOUND:   
    #         vehicle.distance_to_intersection = distance_between(vehicle, SOUTH_LINE)
    #     elif vehicle.dir == Direction.EAST_BOUND:
    #         vehicle.distance_to_intersection = distance_between(vehicle, WEST_LINE)
    #     elif vehicle.dir == Direction.WEST_BOUND:   
    #         vehicle.distance_to_intersection = distance_between(vehicle, EAST_LINE)
    #     elif vehicle.dir == Direction.SOUTH_BOUND:   
    #         vehicle.distance_to_intersection = distance_between(vehicle, NORTH_LINE)
    #     else:
    #         raise ValueError("car has no direction")

    def get_collisions():
        # list of collisions
        # maybe have car with priority first and other car second
        return

    def collision_preventing_adjustment():
        # adjustment must be a timed acceleration/deceleration
        return

    def update(self, vehicles: list[Vehicle]):
        for vehicle in vehicles:
            # vehicle already in list?
            vehicle_in_list = any(manager_vehicle.id == vehicle.id for manager_vehicle in self.vehicles)
            if vehicle_in_list: continue

            # vehicle within manager radius?
            distance_to_vehicle = np.linalg.norm(vehicle.position-self.position)
            if distance_to_vehicle > self.radius: continue

            # vehicle is not in list and within radius, add to list
            self.vehicles.append(vehicle)
    
    def reset(self):
        self.vehicles.clear()