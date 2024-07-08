from classes.vehicle import Vehicle

playback_speed_factor = 6

def update_vehicles(delta_time: float, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        vehicle.velocity += vehicle.acceleration * delta_time 
        vehicle.velocity = 16
    
        print(vehicle.velocity)
        vehicle.route_position += vehicle.velocity * delta_time

def update_world(delta_time: float, vehicles: list[Vehicle]):
    update_vehicles(delta_time, vehicles)