import numpy as np
import pygame
from pygame import Surface
from manager.command import Command
from classes.route import Route, route_position_to_world_position, direction_at_route_position, world_position_to_route_position
from classes.edge import get_length
from standard_traffic.traffic_light import get_light_state, TrafficState
from classes.edge import CircularEdge

MIN_LEADING_DIST = 30
MAX_ANGLE_DIFF = 50
# we want to stop the car "Safety Distance" away from leading car
SAFETY_DISTANCE_BEHIND_VEHICLE = 6
TRAFFIC_LIGHT_SAFETY_DISTANCE = 3
EMERGENCY_DISTANCE = 5
MAX_ACCELERATION = 3.5
NEXT_ACCELERATION_INTERVAL = 0.01

 
class Vehicle:
    """A Vehicle is given commands that it follows along a given route."""

    id: int                  = None            # vehicle identifier
    name: str                = None            # vehicle name
    route: Route             = None            # Route
    route_position: float     = 0               # float representing position in meters along the route

    default_velocity          = 0               # float representing default velocity in meters/second along route
    velocity: float           = 0               # float representing velocity in meters/second along route
    acceleration: float       = 0               # float representing acceleration in meters/second^2 along route

    width: float              = 2.23            # float representing width of car in meters. orthogonal to direction
    length: float             = 4.90            # float representing length of car in meters. parallel to direction
    pivot_distance: float     = 1.25            # float representing distance from pivot to center.
    collided: bool            = False           # if true, will render car red.
    image: Surface
    direction_angle           = 0
    leading_vehicle           = None          # vehicle the current vehicle is trailing if any

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
        self.default_velocity = velocity

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
    vehicle.direction_angle = direction_at_route_position(vehicle.route, vehicle.route_position)
            
def update_cmd(old_cmd: Command, t: np.array, a: np.array, elapsed_time: float=0) -> Command:
    """Return new Command, a concatenation of the old_cmd and new acceleration-time calculations."""
    del_index = None
    for i in range(len(old_cmd.accel_func.x)):
        if old_cmd.accel_func.x[i] >= elapsed_time:
            del_index = i
            break

    new_t = np.concatenate((old_cmd.accel_func.x[:del_index], t))
    new_a = np.concatenate((old_cmd.accel_func.y[:del_index], a))

    return Command(new_t, new_a)

### FUNCTIONS FOR STANDARD TRAFFIC

def driver_traffic_update_command(vehicles: list, cur_time: float) -> None:
    """Update command for standard traffic."""
    update_driver_lead(vehicles)

    for vehicle in vehicles:
        currentEdge = is_on_left_lane(vehicle)
        
        
        if vehicle.leading_vehicle and not currentEdge:
            drive_vehicle_with_leading(vehicle, cur_time)
        
        elif vehicle.leading_vehicle and currentEdge:
            if vehicle.direction_angle == vehicle.leading_vehicle.direction_angle:
                drive_vehicle_with_leading(vehicle, cur_time)
            else:
                # vehicle.leading_vehicle = None
                if is_safe_to_turn_left(vehicle, vehicles):
                    drive_vehicle_with_leading(vehicle, cur_time)
                    # print(str(vehicle.name) + " should GO")
                else:
                    step_in_front_of_traffic_light(vehicle, currentEdge, cur_time)  
            
        elif not vehicle.leading_vehicle and currentEdge:
            if is_safe_to_turn_left(vehicle, vehicles):
                drive_vehicle_without_leading(vehicle, cur_time)
            else:
                step_in_front_of_traffic_light(vehicle, currentEdge, cur_time)  
                
        # allow acceleration within +/- 10 degrees from a StraightEdge
        elif (vehicle.direction_angle % 90) in range(-10, 11):
            drive_vehicle_without_leading(vehicle, cur_time)
            
        check_traffic_lights(vehicle, cur_time)
            
def drive_vehicle_with_leading(vehicle, cur_time: float) -> None:
    """Handle the case where there is a leading vehicle."""
    
    leading_vehicle = vehicle.leading_vehicle
    initial_velocity = vehicle.velocity
    final_velocity = leading_vehicle.velocity
    distance = abs(vehicle.route_position - leading_vehicle.route_position)

    # this prevents division of negative and 0
    if distance < EMERGENCY_DISTANCE:
        vehicle.velocity = 0
        print("Invalid command: Distance to leading vehicle is too short")
        return
    
    # required deceleration to stop car at fake distance away
    required_deceleration = calculate_deceleration(final_velocity, initial_velocity, distance, SAFETY_DISTANCE_BEHIND_VEHICLE)

    # since we want to constantly update the vehicle's command, we update it every NEXT_ACCELERATION_INTERVAL rather than a long range of time 
    new_t = np.array([cur_time, cur_time + NEXT_ACCELERATION_INTERVAL])
    new_a = np.array([required_deceleration, leading_vehicle.acceleration])
    vehicle.command = update_cmd(vehicle.command, new_t, new_a, cur_time)


def drive_vehicle_without_leading(vehicle, cur_time: float) -> None:
    """Handle the case where there is no leading vehicle."""
    acceleration_distance = 10
    initial_velocity = vehicle.velocity

    # Deceleration reduces the vehicle's speed but doesn't exactly return it to its default velocity (vehicle.default_velocity).
    # The final speed is slightly different due to minor decimal variations.
    # if the below is true, it has yet to reach its "default" velocity (in "" since no vehicle will ever reach its exact default velocity)
    if abs(vehicle.velocity - vehicle.default_velocity) > 0.01:
        required_acceleration = (vehicle.default_velocity**2 - initial_velocity**2) / (2 * acceleration_distance)

        new_t = np.array([cur_time, cur_time + NEXT_ACCELERATION_INTERVAL])
        new_a = np.array([required_acceleration, vehicle.acceleration])
        vehicle.command = update_cmd(vehicle.command, new_t, new_a, cur_time)


def check_traffic_lights(vehicle, cur_time: float) -> None:
    """Check traffic lights and update commands based on their states."""
    for r in vehicle.route.pos_to_edge_map:
        if vehicle.route_position < r[1]:
            edge = vehicle.route.pos_to_edge_map[r]

            if edge.traffic_light and vehicle.leading_vehicle:
                if should_ignore_light_due_to_leading_vehicle(vehicle, edge):
                    continue

            if edge.traffic_light:
                handle_traffic_light(vehicle, edge, cur_time)


def should_ignore_light_due_to_leading_vehicle(vehicle, edge) -> bool:
    """Determine if the traffic light can be ignored due to the leading vehicle."""
    distance_to_leading_vehicle = abs(vehicle.route_position - vehicle.leading_vehicle.route_position)
    traffic_light_route_position = world_position_to_route_position(vehicle.route, edge, edge.traffic_light.node.position)
    distance_to_traffic_light = abs(vehicle.route_position - traffic_light_route_position)
    return distance_to_traffic_light > distance_to_leading_vehicle


def handle_traffic_light(vehicle, edge, cur_time: float) -> None:
    """Handle the traffic light's effect on the vehicle's command."""
    initial_velocity = vehicle.velocity
    traffic_light_state = get_light_state(edge.traffic_light)
    
    if traffic_light_state == TrafficState.GREEN:
        return

    traffic_light_route_position = world_position_to_route_position(vehicle.route, edge, edge.traffic_light.node.position)
    distance_to_traffic_light = traffic_light_route_position - vehicle.route_position

    if traffic_light_route_position < vehicle.route_position:
        return
    
    if traffic_light_state == TrafficState.RED or (traffic_light_state == TrafficState.YELLOW and yellow_light_decision(vehicle, traffic_light_route_position)):
        required_deceleration = calculate_deceleration(0, initial_velocity, distance_to_traffic_light, TRAFFIC_LIGHT_SAFETY_DISTANCE)

        new_t = np.array([cur_time, cur_time + NEXT_ACCELERATION_INTERVAL])
        new_a = np.array([required_deceleration, vehicle.acceleration])
        vehicle.command = update_cmd(vehicle.command, new_t, new_a, cur_time)
        

def yellow_light_decision(vehicle, distance_to_traffic_light):
    """Determines whether or not the the vehicle should run a yellow light"""
    
    distance_needed_to_stop = (-vehicle.velocity**2) / 2*(-vehicle.acceleration)
    
    return distance_needed_to_stop < distance_to_traffic_light - TRAFFIC_LIGHT_SAFETY_DISTANCE  

def calculate_deceleration(final_velocity: float, initial_velocity: float, distance: float, safety_distance: float) -> float:
    """Calculate the required deceleration to maintain a safe distance."""
    if distance == safety_distance:
        return 0
    return (final_velocity**2 - initial_velocity**2) / (2 * (distance - safety_distance))

def update_driver_lead(vehicles: list) -> None:
    """Update each vehicle's leading_vehicle."""
    for i, trailing_v in enumerate(vehicles):
        cur_leading_v = trailing_v.leading_vehicle
        cur_leading_v_wp = get_world_position_if_exists(cur_leading_v)

        # If the current leading vehicle is out of bounds, set to None
        if cur_leading_v is not None and cur_leading_v_wp is None:
            trailing_v.leading_vehicle = None
            continue

        trailing_v_wp = route_position_to_world_position(trailing_v.route, trailing_v.route_position)
        if trailing_v_wp is None:
            continue

        cur_leading_v_dist = calculate_distance(cur_leading_v_wp, trailing_v_wp) if cur_leading_v else None
        cur_leading_v, cur_leading_v_dist = find_closest_leading_vehicle(i, vehicles, trailing_v, trailing_v_wp, cur_leading_v, cur_leading_v_dist)

        update_leading_vehicle(trailing_v, cur_leading_v, cur_leading_v_dist)

def get_world_position_if_exists(vehicle: Vehicle) -> np.array:
    """Return world position of vehicle if it exists, otherwise None."""
    return route_position_to_world_position(vehicle.route, vehicle.route_position) if vehicle else None


def calculate_distance(leading_vehicle_wp: np.array, trailing_vehicle_wp: np.array) -> float:
    """Calculate the distance between two vehicles."""
    return np.linalg.norm(leading_vehicle_wp - trailing_vehicle_wp)


def find_closest_leading_vehicle(i: int, vehicles: list, trailing_v: Vehicle, trailing_v_wp: np.array, cur_leading_v: Vehicle, cur_leading_v_dist: float) -> Vehicle:
    """Find the closest leading vehicle based on distance and direction angle."""
    for j, potential_leading_v in enumerate(vehicles):
        if i == j:  # Skip the same vehicle
            continue

        if not is_potential_lead_valid(trailing_v, potential_leading_v):
            continue

        potential_leading_v_wp = route_position_to_world_position(potential_leading_v.route, potential_leading_v.route_position)
        if potential_leading_v_wp is None:
            continue

        potential_leading_v_dist = calculate_distance(potential_leading_v_wp, trailing_v_wp)

        # Update leading vehicle if the new potential lead is closer
        if cur_leading_v_dist is None or potential_leading_v_dist < cur_leading_v_dist:
            cur_leading_v = potential_leading_v
            cur_leading_v_dist = potential_leading_v_dist
            

    return cur_leading_v, cur_leading_v_dist


def is_potential_lead_valid(trailing_v: Vehicle, potential_leading_v: Vehicle) -> bool:
    """Check if a potential leading vehicle is valid based on route position and angle difference."""
    if trailing_v.route_position > potential_leading_v.route_position:
        return False

    if abs(trailing_v.direction_angle - potential_leading_v.direction_angle) > MAX_ANGLE_DIFF:
        return False
    
    if are_vehicles_in_diff_lane(trailing_v, potential_leading_v):
        return False

    return True


def update_leading_vehicle(trailing_v: Vehicle, cur_leading_v: Vehicle, cur_leading_v_dist: float) -> None:
    """Update the leading vehicle based on distance and angle difference."""
    if cur_leading_v is None:
        trailing_v.leading_vehicle = None
        return

    is_not_within_angle_scope = abs(trailing_v.direction_angle - cur_leading_v.direction_angle) > MAX_ANGLE_DIFF
    
    if cur_leading_v_dist > MIN_LEADING_DIST or is_not_within_angle_scope or are_vehicles_in_diff_lane(trailing_v, cur_leading_v):
        trailing_v.leading_vehicle = None
    else:
        trailing_v.leading_vehicle = cur_leading_v
        
        
# Functions for left turn
def is_on_left_lane(vehicle: Vehicle):
    """Determines whether the current vehicle is on the left turn lane."""
   
    currentEdge = None
    for r in vehicle.route.pos_to_edge_map:
        position = vehicle.route_position
        
        if position < r[1] and position >= r[0]:
            currentEdge = vehicle.route.pos_to_edge_map[r]
            break
        
    if currentEdge is not None and currentEdge.leftTurn:
        # returns the currentEdge if on left lane
        return currentEdge
    
    return None
    
def is_safe_to_turn_left(current_vehicle: Vehicle, vehicles: list) -> bool:
    """Confirms the safety of the current vehicle to turn left."""
    
    for potential_incoming_v in vehicles:
        if potential_incoming_v == current_vehicle:  # Skip the same vehicle
            continue
        
        # return False if the potential_incoming_v is incoming and is in the range of danger
        
        # return Falce if difference in angle is in range(-20, 21)
        not_facing_same_direction = (potential_incoming_v.direction_angle - current_vehicle.direction_angle) not in range(-20, 21)
        is_on_opposite_side = (potential_incoming_v.direction_angle - current_vehicle.direction_angle) % 180 in range(-20, 21)
        incoming_car_is_in_danger_zone = (55 < potential_incoming_v.route_position < 90)

        # return False if 
            
        if not_facing_same_direction and are_vehicles_in_diff_lane(current_vehicle, potential_incoming_v) and is_on_opposite_side and incoming_car_is_in_danger_zone:
            print(str(current_vehicle.name) + " is not going because of " + str(potential_incoming_v.name))
            return False
        
    return True
        
def step_in_front_of_traffic_light(vehicle: Vehicle, currentEdge, cur_time) -> None:
    """Makes the given vehicle that is about to turn left to step slightly in front of the traffic light."""
    if currentEdge.traffic_light == None:
        return
    
    initial_velocity = vehicle.velocity
    
    traffic_light_route_position = world_position_to_route_position(vehicle.route, currentEdge, currentEdge.traffic_light.node.position)
    
    distance_to_traffic_light = traffic_light_route_position - vehicle.route_position
    
    required_deceleration = calculate_deceleration(0, initial_velocity, distance_to_traffic_light, TRAFFIC_LIGHT_SAFETY_DISTANCE)

    new_t = np.array([cur_time, cur_time + NEXT_ACCELERATION_INTERVAL])
    new_a = np.array([required_deceleration, vehicle.acceleration])
    vehicle.command = update_cmd(vehicle.command, new_t, new_a, cur_time)
    
def are_vehicles_in_diff_lane(vehicle1: Vehicle, vehicle2: Vehicle):
    return (is_on_left_lane(vehicle1) and not is_on_left_lane(vehicle2)) or (not is_on_left_lane(vehicle1) and is_on_left_lane(vehicle2))
    
    
# X TODO: for the trailing car with a lead in the left lane, it will follow what the leading car is doing, instead of looking ahead to make sure it safe for IT.
# make sure to not following the lead when in left lane but to look for themselves 
# TODO: step_in_front_of_traffic_light is such a terrible way to code (dulicate of a diff fn)
# TODO: the driver_traffic_update_command is very messy