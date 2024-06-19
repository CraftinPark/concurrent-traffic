SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# world describes 160mx160m space
WORLD_WIDTH = 160
WORLD_HEIGHT = 160

import pygame
from copy import deepcopy
import numpy as np

from classes.vehicle import Vehicle, vehicle_event_loop, vehicle_copy
from classes.button import Button
from manager.manager import Manager, manager_event_loop 
from classes.node import Node
from classes.edge import Edge
from classes.route import Route
from .render import render_world, render_manager, render_vehicles, render_buttons
from .update import update_world

def run_simulation(initial_vehicles: list[Vehicle], nodes: list[Node], edges: list[Edge], routes: list[Route], manager: Manager): # requires initialization of lanes, manager, vehicles
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    vehicles = vehicle_copy(initial_vehicles)
    is_run = True
    route_visible = True

    def toggle_update() -> None:
        nonlocal is_run
        is_run = not is_run

    def restart_func() -> None:
        nonlocal vehicles
        nonlocal clock
        nonlocal delta_time
        nonlocal manager

        vehicles = vehicle_copy(initial_vehicles)
        clock = pygame.time.Clock()
        delta_time = 0
        manager.reset()
    
    def toggle_route_visibility() -> None:
        nonlocal route_visible
        route_visible = not route_visible
    
    toggle_button = Button((0, 0, 0), (255, 50, 50), (SCREEN_WIDTH/6 -100, SCREEN_HEIGHT - 100), (200, 50), 'toggle update', toggle_update, ())
    restart_button = Button((0, 0, 0), (255, 50, 50), (SCREEN_WIDTH/2 -125, SCREEN_HEIGHT - 100), (200, 50), 'restart', restart_func, ())
    routes_visibility_button = Button((0, 0, 0), (255, 50, 50), (SCREEN_WIDTH/1.5, SCREEN_HEIGHT - 100), (250, 50), 'toggle route visibility', toggle_route_visibility, ())

    buttons = [toggle_button, restart_button, routes_visibility_button]
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                [b.click() for b in buttons]


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        render_buttons(screen, buttons)

        # optionally render nodes and edges. for now always on
        if route_visible:
            render_world(screen, nodes, edges)
        render_manager(screen, manager)
        render_vehicles(screen, vehicles)

        # manager 'cpu'
        manager_event_loop(manager, vehicles, delta_time)

        # vehicles 'cpu'
        for vehicle in vehicles:
            vehicle_event_loop(vehicle, delta_time)

        # vehicle removal 
        for vehicle in vehicles:
            if vehicle.route_position > vehicle.route.total_length:
                vehicles.remove(vehicle)

        if is_run:
            # physical changes to world (updating positions, velocity, etc.)
            update_world(delta_time, vehicles)

        # updates the screen
        pygame.display.update()
        delta_time = clock.tick(60) / 1000
    pygame.quit()
