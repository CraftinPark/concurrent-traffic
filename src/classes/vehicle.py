import numpy as np
import pygame
from pygame import Surface
from manager.command import Command
from classes.route import Route

class Vehicle:
    """A Vehicle is given commands that it follows along a given route."""

    id: int                  = None            # vehicle identifier
    name: str                = None            # vehicle name
    route: Route             = None            # Route
    route_position: float     = 0               # float representing position in meters along the route

    velocity: float           = 0               # float representing velocity in meters/second along route
    acceleration: float       = 0               # float representing acceleration in meters/second^2 along route

    width: float              = 2.23            # float representing width of car in meters. orthogonal to direction
    length: float             = 4.90            # float representing length of car in meters. parallel to direction
    pivot_distance: float     = 1.25            # float representing distance from pivot to center.
    image: Surface

    command: Command          = Command([0], [0])             # Command

    def __init__(self,
                 name: str,
                 id: int,
                 route: Route,
                 route_position: float,
                 velocity: float,
                 acceleration: float,
                 width: float,
                 length: float,
                 pivot_distance: float,
                 image_source: str,
                 ) -> None:
        self.id = id
        self.name = name
        self.route = route
        self.route_position = route_position
        self.velocity = velocity
        self.acceleration = acceleration
        self.width = width
        self.length = length
        self.pivot_distance = pivot_distance
        self.image_source = image_source
        self.image = pygame.image.load(self.image_source)

# helpers

# def get_vehicle_center_point(vehicle: Vehicle):
    


#     vehicle_center_x = vehicle.position[0] + vehicle.direction[0] * vehicle.pivot_distance
#     vehicle_center_y = vehicle.position[1] + vehicle.direction[1] * vehicle.pivot_distance
#     return vehicle_center_x, vehicle_center_y

def vehicle_copy(vehicles: list[Vehicle]) -> list[Vehicle]:
    """Return a deep copy of a list of Vehicles."""
    return [Vehicle(v.id, v.name, v.route, v.route_position, v.velocity, v.acceleration, v.width, v.length, v.pivot_distance, v.image_source) for v in vehicles]
  
def vehicle_event_loop(vehicle: Vehicle, delta_time: float) -> None:
    """Event loop for Vehicle."""
    vehicle.acceleration = vehicle.command(delta_time)

def update_cmd(old_cmd: Command, t: np.array, a: np.array, elapsed_time: float=0) -> Command:
    """Return new Command, a concatenation of the old_cmd and new acceleration-time calculations."""
    del_index = None
    for i in range(len(old_cmd.accel_func.x)):
        if old_cmd.accel_func.x[i] >= elapsed_time:
            print(i, len(old_cmd.accel_func.x))
            del_index = i
            break

    new_t = np.concatenate((old_cmd.accel_func.x[:del_index], t))
    new_a = np.concatenate((old_cmd.accel_func.y[:del_index], a))

    return Command(new_t, new_a)