from classes.vehicle import Vehicle

def update_vehicles(delta_time: float, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        vehicle.update(delta_time)

def update_world(delta_time: float, vehicles: list[Vehicle]):
    update_vehicles(delta_time, vehicles)