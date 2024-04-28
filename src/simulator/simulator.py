import pygame
from pygame import Surface
import numpy as np
from classes import Vehicle
from manager import Node, Edge, Route

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

# world describes 100mx100m space
WORLD_WIDTH = 100
WORLD_HEIGHT = 100

def world_to_screen_vector(x: float, y: float):
    return [(x+(WORLD_WIDTH/2))*SCREEN_WIDTH/WORLD_WIDTH, (y+(WORLD_HEIGHT/2))*SCREEN_HEIGHT/WORLD_HEIGHT]

def world_to_screen_scalar(x: float):
    return x*SCREEN_WIDTH/WORLD_WIDTH

def distance(vector1: list, vector2: list):
    vec1 = np.array(vector1)
    vec2 = np.array(vector2)
    return np.linalg.norm(vec2-vec1)

def render_paths(screen: Surface, nodes: list[Node], edges: list[Edge]):
    for node in nodes:
        node_position = world_to_screen_vector(node.position[0], node.position[1])
        pygame.draw.circle(screen, "red", node_position, 3)
    for i, edge in enumerate(edges):
        if edge.curved == False:
            start_position = world_to_screen_vector(edge.start.position[0], edge.start.position[1])
            end_position   = world_to_screen_vector(edge.end.position[0], edge.end.position[1])
            pygame.draw.line(screen, "red", start_position, end_position)
        else:
            # define rect
            radius = world_to_screen_scalar(distance(edge.center, edge.start.position))
            diameter = radius*2
            arc_rect = pygame.Rect(0,0,diameter, diameter)
            arc_rect.center = world_to_screen_vector(edge.center[0], edge.center[1])

            # find angle of start point
            vector_to_start = [edge.start.position[0]-edge.center[0],edge.start.position[1]-edge.center[1]]
            rad_angle_to_start = np.arctan2(-vector_to_start[1], vector_to_start[0]) # invert y to use rendering coords. Y is positive downward.
            # find angle of end point
            vector_to_end = [edge.end.position[0]-edge.center[0],edge.end.position[1]-edge.center[1]]
            rad_angle_to_end = np.arctan2(-vector_to_end[1], vector_to_end[0]) # invert y to use rendering coords. Y is positive downward.

            cross_product = np.cross(np.array([vector_to_start[0],-vector_to_start[1]]), np.array([vector_to_end[0],-vector_to_end[1]]))
            if cross_product < 0:
                rad_angle_to_start, rad_angle_to_end = rad_angle_to_end, rad_angle_to_start
            elif cross_product == 0:
                raise ValueError("cross product of curved edge vectors is 0. This implies a U-turn...")

            pygame.draw.arc(screen, "red", arc_rect, rad_angle_to_start, rad_angle_to_end)

def get_vehicle_center_point(vehicle: Vehicle):
    vehicle_center_x = vehicle.position[0] + vehicle.direction[0] * vehicle.pivot_distance
    vehicle_center_y = vehicle.position[1] + vehicle.direction[1] * vehicle.pivot_distance
    return vehicle_center_x, vehicle_center_y

def render_vehicles(screen: Surface, vehicles: list):
    for vehicle in vehicles:
        vehicle_pivot_screen_pos = world_to_screen_vector(vehicle.position[0], vehicle.position[1])
        vehicle_screen_width = world_to_screen_scalar(vehicle.width)
        vehicle_screen_length = world_to_screen_scalar(vehicle.length)

        vehicle_center_point = get_vehicle_center_point(vehicle)
        vehicle_center_screen_pos = world_to_screen_vector(vehicle_center_point[0], vehicle_center_point[1])

        img = pygame.transform.smoothscale(vehicle.image, (vehicle_screen_length, vehicle_screen_width))
        vehicle_angle = np.rad2deg(np.arctan2(-vehicle.direction[1], vehicle.direction[0]))
        img = pygame.transform.rotate(img, vehicle_angle)

        car_rect = img.get_rect()
        car_rect.center = vehicle_center_screen_pos
        screen.blit(img, car_rect)

        pygame.draw.circle(screen, "red", vehicle_pivot_screen_pos, 3)

def update_vehicles(delta_time: float, vehicles: list):
    for vehicle in vehicles:
        vehicle.update(delta_time)

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