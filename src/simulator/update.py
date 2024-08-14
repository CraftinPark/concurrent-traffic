from classes.vehicle import Vehicle

def update_vehicles(delta_time: float, vehicles: list[Vehicle]) -> None:
    """Updates Vehicle velocity and route_position in given delta_time."""
    for vehicle in vehicles:
        if vehicle.acceleration * delta_time != 0:
            print("vehicle", vehicle.name, "velocity from", vehicle.velocity, "to:", vehicle.velocity + vehicle.acceleration * delta_time)
        vehicle.velocity += vehicle.acceleration * (delta_time - vehicle.spawn_at)
        vehicle.route_position += vehicle.velocity * (delta_time - vehicle.spawn_at)

def update_world(delta_time: float, active_vehicles: list[Vehicle], scheduled_vehicles: list[Vehicle]) -> None:
    """Update world components given delta_time."""
    # update_scheduled_vehicles(delta_time, active_vehicles, scheduled_vehicles)
    update_vehicles(delta_time, active_vehicles)
    print(active_vehicles)

def update_scheduled_vehicles(delta_time: float, active_vehicles: list[Vehicle], scheduled_vehicles: list[Vehicle]) -> None:
    """Puts scheduled vehicles in the system their delta_time reaches their spawn_at time."""
    for vehicle in scheduled_vehicles:
        print(delta_time, vehicle.spawn_at)
        if delta_time > vehicle.spawn_at:
            active_vehicles.append(scheduled_vehicles.pop(0))
            print(vehicle.acceleration)
        else:
            break
