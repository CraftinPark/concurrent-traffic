ORIGINAL_SCREEN_WIDTH = 1000
ORIGINAL_SCREEN_HEIGHT = 720

TOOLBAR_HEIGHT = 100

MIN_ZOOM_FACTOR = 1
MAX_ZOOM_FACTOR = 8
zoom_factor = 1

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
from .render import render_world, render_manager, render_vehicles, render_buttons, render_time, render_toolbar, render_title
from .update import update_world
from .helper import set_zoomed_helper, scroll_handler

def run_simulation(initial_vehicles: list[Vehicle], nodes: list[Node], edges: list[Edge], routes: list[Route], intersection_points, manager: Manager): # requires initialization of lanes, manager, vehicles
    pygame.init()
    screen = pygame.display.set_mode((ORIGINAL_SCREEN_WIDTH, ORIGINAL_SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True
    delta_time = 0
    time_elapsed = 0

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
        nonlocal time_elapsed

        vehicles = vehicle_copy(initial_vehicles)
        clock = pygame.time.Clock()
        delta_time = 0
        time_elapsed = 0
        manager.reset()
    
    def toggle_route_visibility() -> None:
        nonlocal route_visible
        route_visible = not route_visible

    def toggle_zoom() -> None: 
        global zoom_factor
        if zoom_factor == 1:
            zoom_factor = MAX_ZOOM_FACTOR
        else:
            zoom_factor = 1
        set_zoomed_helper(zoom_factor)
    
    toggle_button = Button((40, 40, 40), (255, 50, 50), (5, screen.get_height()-TOOLBAR_HEIGHT+50), (100, 30), 'toggle update', toggle_update, ())
    restart_button = Button((40, 40, 40), (255, 50, 50), (110, screen.get_height()-TOOLBAR_HEIGHT+50), (100, 30), 'restart', restart_func, ())
    routes_visibility_button = Button((40, 40, 40), (255, 50, 50), (215, screen.get_height()-TOOLBAR_HEIGHT+50), (150, 30), 'toggle route visibility', toggle_route_visibility, ())
    zoom_button = Button((40, 40, 40), (255, 50, 50), (370, screen.get_height()-TOOLBAR_HEIGHT+50), (70, 30), 'zoom', toggle_zoom, ())


    buttons = [toggle_button, restart_button, routes_visibility_button, zoom_button]
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                [b.click() for b in buttons]

            elif event.type == pygame.MOUSEWHEEL:
                global zoom_factor
                zoom_factor = scroll_handler(event, zoom_factor)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color(150,150,150))

        # optionally render nodes and edges. for now always on
        render_world(screen, nodes, edges, route_visible, intersection_points)
        render_manager(screen, manager)
        render_vehicles(screen, vehicles)
        render_toolbar(screen, time_elapsed, buttons)
        render_title(screen)

        # manager 'cpu'
        manager_event_loop(manager, vehicles, time_elapsed)

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
            time_elapsed += delta_time

        # updates the screen
        pygame.display.update()
        delta_time = clock.tick(60) / 1000
        
    pygame.quit()
