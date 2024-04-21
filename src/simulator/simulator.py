import pygame
from pygame import Surface
import numpy as np
from vehicle import Vehicle
from route import Node, Edge, Route

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# world describes 100mx100m space
WORLD_WIDTH = 100
WORLD_HEIGHT = 100

def world_to_screen_vector(x: float, y: float):
    return [(x+(WORLD_WIDTH/2))*SCREEN_WIDTH/WORLD_WIDTH, (y+(WORLD_HEIGHT/2))*SCREEN_HEIGHT/WORLD_HEIGHT]

def world_to_screen_scalar(x: float):
    return x*SCREEN_WIDTH/WORLD_WIDTH

def render_paths(screen: Surface, nodes: list[Node], edges: list[Edge]):
    for node in nodes:
        node_position = world_to_screen_vector(node.position[0], node.position[1])
        pygame.draw.circle(screen, "red", node_position, 3)
    for edge in edges:
        start_position = world_to_screen_vector(edge.start.position[0], edge.start.position[1])
        end_position   = world_to_screen_vector(edge.end.position[0], edge.end.position[1])
        pygame.draw.line(screen, "red", start_position, end_position)

def render_vehicles(screen: Surface, vehicles: list):
    for vehicle in vehicles:
        vehicle_screen_x, vehicle_screen_y = world_to_screen_vector(vehicle.position[0], vehicle.position[1])
        vehicle_screen_width = world_to_screen_scalar(vehicle.width)
        vehicle_screen_height = world_to_screen_scalar(vehicle.height)
        car_rect = pygame.Rect(0, 0, vehicle_screen_width, vehicle_screen_height)
        car_rect.center = vehicle_screen_x, vehicle_screen_y
        pygame.draw.rect(screen, "red", car_rect, 0)

def update_vehicles(delta_time: float, vehicles: list):
    for vehicle in vehicles:
        vehicle.position[0] = vehicle.position[0] + vehicle.velocity[0] * delta_time
        vehicle.position[1] = vehicle.position[1] + vehicle.velocity[1] * delta_time

def run_simulation(initial_vehicles: list[Vehicle], nodes: list[Node], edges: list[Edge], routes: list[Route]): # requires initialization of lanes, manager, vehicles
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    delta_time: float = 0

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

        # optionally render nodes and edges. for now always on
        render_paths(screen, nodes, edges)

        render_vehicles(screen, vehicles)

        # we do not yet consider that Manager is a parallel computation. We can directly apply the adjustments that Manager makes to the vehicles.
        # manager adjust function call

        update_vehicles(delta_time, vehicles)

        # flip() the display to put your work on screen
        pygame.display.flip()
        delta_time = clock.tick(60) / 1000
    pygame.quit()