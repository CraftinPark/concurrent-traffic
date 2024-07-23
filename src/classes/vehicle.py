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
    leading_vehicle             = None          # vehicle the current vehicle is trailing if any

    command: Command          = Command(np.array([0]), np.array([0]))             # Command

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
        self.leading_vehicle = None

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
            # print(i, len(old_cmd.accel_func.x))
            del_index = i
            break

    new_t = np.concatenate((old_cmd.accel_func.x[:del_index], t))
    new_a = np.concatenate((old_cmd.accel_func.y[:del_index], a))

    return Command(new_t, new_a)

### FUNCTIONS FOR STANDARD TRAFFIC

def driver_traffic_update_command(vehicles: list, cur_time: float) -> None:
    """Update command for standard traffic."""
    cmd = None
    # calculate command that achieves two things
    # 1. stop before any traffic stop line if that traffic light is red
    #    traffic light red? stop before it
    #    traffic light green? speed up
    # 2. maintain distance between car with closest collision (the car in front)
    #    if conditions match to calculate new command
    #    a. is our distance to that car within X?
    #       is their acceleration lower than ours?
    #       -> calculate slow down
    #    b. is our distance to that car more than Y?
    #       is their acceleration more than ours?
    #       -> calculate speed up

    # 1 and 2 need to work together. If 2. determines that we can speed up,
    # but the car is approaching a red traffic light,
    # then the final command should be to slow down

    updated_vehicles = update_lead_vehicle(vehicles, cur_time)

    # for vehicle in updated_vehicles:
    #     if vehicle.leading_vehicle:

    #         trailing_vehicle = vehicle
    #         leading_vehicle = vehicle.leading_vehicle

    #         initial_velocity = trailing_vehicle.velocity
    #         final_velocity = leading_vehicle.velocity

    #         distance_to_leading = abs(leading_vehicle.route_position - trailing_vehicle.route_position) 

    #         if initial_velocity <= final_velocity:
    #             trailing_vehicle.command = leading_vehicle.command
    #             trailing_vehicle.velocity = final_velocity
            
        
    #         else:
    #             leading_vehicle_delta_distance = leading_vehicle.velocity * (updated_vehicles[trailing_vehicle].time - cur_time)

    #             required_deceleration = (final_velocity**2 - initial_velocity**2) / (2 * (distance_to_leading + leading_vehicle_delta_distance ))
    #             new_t = np.array([cur_time, updated_vehicles[trailing_vehicle].time])
    #             new_a = np.array([trailing_vehicle.acceleration, required_deceleration])
    #             trailing_vehicle.command = update_cmd(trailing_vehicle.command, new_t, new_a, cur_time)



def update_lead_vehicle(vehicles: list[Vehicle], cur_time: float):
    from manager.manager import get_collisions
    
    collision_list = get_collisions(vehicles, cur_time)
    # store the trailing vehicle along with its Collision
    updated_vehicles = {}
    # run a for loop to update the leading vehicle 
    for collision in collision_list:
        print(collision.time)
        # vehicle0, vehicle1 = collision.vehicle0, collision.vehicle1

        # if vehicle0.route_position > vehicle1.route_position:
        #     leading_vehicle = vehicle0
        #     trailing_vehicle = vehicle1
        # else:
        #     leading_vehicle = vehicle1
        #     trailing_vehicle = vehicle0

        # distance_to_leading = abs(leading_vehicle.route_position - trailing_vehicle.route_position) 
        # if distance_to_leading > 30:
        #     trailing_vehicle.leading_vehicle = None
        #     continue

        # for edge in trailing_vehicle.route.pos_to_edge_map.values():
        #     if edge in leading_vehicle.route.pos_to_edge_map.values():
        #         trailing_vehicle.leading_vehicle = leading_vehicle
        #         updated_vehicles[trailing_vehicle] = collision

    return updated_vehicles
        
