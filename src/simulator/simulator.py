SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# world describes 100mx100m space
WORLD_WIDTH = 160
WORLD_HEIGHT = 160

import pygame
from copy import deepcopy
import numpy as np
from classes.vehicle import Vehicle, vehicle_copy
from classes.button import Button
from manager.manager import Manager
from manager.route import Node, Edge, Route
from .render import render_world, render_manager, render_buttons
from .update import update_world

def run_simulation(initial_vehicles: list[Vehicle], nodes: list[Node], edges: list[Edge], routes: list[Route], manager: Manager): # requires initialization of lanes, manager, vehicles
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    vehicles = vehicle_copy(initial_vehicles)
    is_pause = True

    def toggle_update() -> None:
        nonlocal is_pause
        is_pause = not is_pause

    def restart_func() -> None:
        nonlocal vehicles
        nonlocal clock
        nonlocal delta_time
        nonlocal manager

        vehicles = vehicle_copy(initial_vehicles)
        clock = pygame.time.Clock()
        delta_time = 0
        manager.reset()
    
    toggle_button = Button((0, 0, 0), (255, 50, 50), (SCREEN_WIDTH/2 - 300, SCREEN_HEIGHT - 100), (300, 50), 'toggle update', toggle_update, ())
    restart_button = Button((0, 0, 0), (255, 50, 50), (SCREEN_WIDTH/2 + 100, SCREEN_HEIGHT - 100), (200, 50), 'restart', restart_func, ())

    buttons = [toggle_button, restart_button]

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

        if is_pause:
            #update manager
            manager.update(vehicles)

            # we do not yet consider that Manager is a parallel computation. We can directly apply the adjustments that Manager makes to the vehicles.
            # manager adjust function call
            update_world(delta_time, vehicles)

        # optionally render nodes and edges. for now always on
        render_world(screen, vehicles, nodes, edges)
        render_manager(screen, manager)

        # updates the screen
        pygame.display.update()
        delta_time = clock.tick(60) / 1000