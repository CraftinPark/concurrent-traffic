from classes.vehicle import Vehicle

def update_vehicles(delta_time: float, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        vehicle.velocity[0] += vehicle.acceleration[0] * delta_time
        vehicle.velocity[1] += vehicle.acceleration[1] * delta_time
        vehicle.position[0] += vehicle.velocity[0] * delta_time
        vehicle.position[1] += vehicle.velocity[1] * delta_time

def update_world(delta_time: float, vehicles: list[Vehicle]):
    update_vehicles(delta_time, vehicles)