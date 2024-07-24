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
    direction_angle           = 0

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
            print(i, len(old_cmd.accel_func.x))
            del_index = i
            break

    new_t = np.concatenate((old_cmd.accel_func.x[:del_index], t))
    new_a = np.concatenate((old_cmd.accel_func.y[:del_index], a))

    return Command(new_t, new_a)

### FUNCTIONS FOR STANDARD TRAFFIC

def driver_traffic_update_command(vehicles: list, cur_time: float) -> None:
    """Update command for standard traffic."""

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

    from manager.manager import get_collisions
    
    collision_list = get_collisions(vehicles, cur_time)

    # run a for loop to implement command for each collision
    for collision in collision_list:
        vehicle0, vehicle1 = collision.vehicle0, collision.vehicle1
        
        # assign leading and trailing vehicles based on their route_positions
        if vehicle0.route_position > vehicle1.route_position:
            leading_vehicle = vehicle0
            trailing_vehicle = vehicle1
        else:
            leading_vehicle = vehicle1
            trailing_vehicle = vehicle0

        initial_velocity = trailing_vehicle.velocity
        final_velocity = leading_vehicle.velocity
        distance_to_leading = abs(leading_vehicle.route_position - trailing_vehicle.route_position) 

        delta_vel = leading_vehicle.velocity - trailing_vehicle.velocity
        # calculate time of collision 
        if delta_vel != 0:
            time_of_collision = (trailing_vehicle.route_position - leading_vehicle.route_position) / (delta_vel) + cur_time
        else:
            # two vehicles have same velocity and will never collide
            time_of_collision = -1

        # this accounts for when the previous leading vehicle disappears
        if cur_time > time_of_collision and abs(trailing_vehicle.direction_angle - leading_vehicle.direction_angle) >= 90 and trailing_vehicle.leading_vehicle != None:
            trailing_vehicle.leading_vehicle = None
            final_velocity = 12 
            time_to_reach = 2   

            # Calculate the required acceleration
            required_acceleration = (final_velocity - initial_velocity) / time_to_reach
    
            new_t = np.array([cur_time, cur_time + time_to_reach])
            new_a = np.array([required_acceleration, 0])  # Maintain acceleration for 2 seconds, then set to 0

            trailing_vehicle.command = update_cmd(trailing_vehicle.command, new_t, new_a, cur_time)
            continue

        # safety distance remained. No action needed
        if distance_to_leading > 30:
            continue

        # emergency stop
        elif distance_to_leading < 8 and trailing_vehicle.leading_vehicle != None:
            trailing_vehicle.command = leading_vehicle.command
            trailing_vehicle.velocity = leading_vehicle.velocity

        # calculate the required deceleration and update command
        else:
            for edge in trailing_vehicle.route.pos_to_edge_map.values():
                # check if they have at least one common edge, if the trailing vehicle doesn't already have a leading vehicle, and if they are facing the same relative direction 
                if edge in leading_vehicle.route.pos_to_edge_map.values() and trailing_vehicle.leading_vehicle == None and abs(trailing_vehicle.direction_angle - leading_vehicle.direction_angle) < 90:
                    trailing_vehicle.leading_vehicle = leading_vehicle

                    leading_vehicle_delta_distance = leading_vehicle.velocity * (time_of_collision - cur_time)
                    required_deceleration = (final_velocity**2 - initial_velocity**2) / (2 * (distance_to_leading + leading_vehicle_delta_distance))
                    new_t = np.array([cur_time, time_of_collision])
                    new_a = np.array([required_deceleration, leading_vehicle.acceleration])
                    print(trailing_vehicle.velocity)
                    trailing_vehicle.command = update_cmd(trailing_vehicle.command, new_t, new_a, cur_time)