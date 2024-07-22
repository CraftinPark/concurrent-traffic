from classes.vehicle import Vehicle

def update_vehicles(delta_time: float, vehicles: list[Vehicle]) -> None:
    """Updates Vehicle velocity and route_position in given delta_time."""
    for vehicle in vehicles:
        vehicle.velocity += vehicle.acceleration * delta_time 
        vehicle.route_position += vehicle.velocity * delta_time

def update_world(delta_time: float, vehicles: list[Vehicle]) -> None:
    """Update world components given delta_time."""
    update_vehicles(delta_time, vehicles)