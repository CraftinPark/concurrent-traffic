import pygame
import numpy as np
from vehicle import Vehicle

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# world describes 100mx100m space
WORLD_WIDTH = 100
WORLD_HEIGHT = 100

def world_to_screen_vector(x, y):
    return [(x+(WORLD_WIDTH/2))*SCREEN_WIDTH/WORLD_WIDTH, (y+(WORLD_HEIGHT/2))*SCREEN_HEIGHT/WORLD_HEIGHT]

def world_to_screen_scalar(x):
    return x*SCREEN_WIDTH/WORLD_WIDTH

def render_vehicles(screen, vehicles: list):
    for vehicle in vehicles:
        vehicle_screen_x, vehicle_screen_y = world_to_screen_vector(vehicle.position[0], vehicle.position[1])
        vehicle_screen_width = world_to_screen_scalar(vehicle.width)
        vehicle_screen_height = world_to_screen_scalar(vehicle.height)
        print(vehicle_screen_x, vehicle_screen_y)
        car_rect = pygame.Rect(vehicle_screen_x, vehicle_screen_y, vehicle_screen_width, vehicle_screen_height)
        pygame.draw.rect(screen, "red", car_rect, 0)

def update_vehicles(delta_time: float, vehicles: list):
    for vehicle in vehicles:
        vehicle.position[0] = vehicle.position[0] + vehicle.velocity[0] * delta_time
        vehicle.position[1] = vehicle.position[1] + vehicle.velocity[1] * delta_time

def run_simulation(initial_vehicles: list): # requires initialization of lanes, manager, vehicles
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    vehicles = initial_vehicles

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        # render_scenery()

        # render_intersection()

        render_vehicles(screen, vehicles)

        # we do not yet consider that Manager is a parallel computation. We can directly apply the adjustments that Manager makes to the vehicles.
        # manager adjust function call

        update_vehicles(delta_time, vehicles)

        # flip() the display to put your work on screen
        pygame.display.flip()
        delta_time = clock.tick(60) / 1000
    pygame.quit()