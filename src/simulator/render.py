import pygame
import numpy as np
from pygame import Surface
from classes.vehicle import Vehicle, get_vehicle_center_point
from manager.route import Node, Edge, Route
from manager.manager import Manager
from .helper import world_to_screen_vector, world_to_screen_scalar

pygame.font.init()
FONT = pygame.font.SysFont('Consolas', 20)

def render_nodes(screen: Surface, nodes: list[Node]):
    for node in nodes:
        node_position = world_to_screen_vector(node.position)
        pygame.draw.circle(screen, "red", node_position, 3)

def render_edges(screen: Surface, edges: list[Edge]):
    for edge in edges:
        if edge.curved == False:
            start_position = world_to_screen_vector(edge.start.position)
            end_position   = world_to_screen_vector(edge.end.position)
            pygame.draw.line(screen, "red", start_position, end_position)
        else:
            # define rect
            radius = world_to_screen_scalar(np.linalg.norm(edge.start.position-edge.center)) # norm describes distance
            diameter = radius*2
            arc_rect = pygame.Rect(0,0,diameter,diameter)
            arc_rect.center = world_to_screen_vector(edge.center)

            # find angle of start point
            vector_to_start = [edge.start.position[0]-edge.center[0],edge.start.position[1]-edge.center[1]]
            rad_angle_to_start = np.arctan2(-vector_to_start[1], vector_to_start[0]) # invert y to use rendering coords. Y is positive downward.

            # find angle of end point
            vector_to_end = [edge.end.position[0]-edge.center[0],edge.end.position[1]-edge.center[1]]
            rad_angle_to_end = np.arctan2(-vector_to_end[1], vector_to_end[0]) # invert y to use rendering coords. Y is positive downward.

            # ensure arc drawn in correct direction by cross product
            cross_product = np.cross(np.array([vector_to_start[0],-vector_to_start[1]]), np.array([vector_to_end[0],-vector_to_end[1]]))
            if cross_product < 0:
                rad_angle_to_start, rad_angle_to_end = rad_angle_to_end, rad_angle_to_start
            elif cross_product == 0:
                raise ValueError("cross product of curved edge vectors is 0. This implies a U-turn...")

            pygame.draw.arc(screen, "red", arc_rect, rad_angle_to_start, rad_angle_to_end)

def render_vehicles(screen: Surface, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        vehicle_pivot_screen_pos = world_to_screen_vector(vehicle.position)
        vehicle_screen_width = world_to_screen_scalar(vehicle.width)
        vehicle_screen_length = world_to_screen_scalar(vehicle.length)

        vehicle_center_point = get_vehicle_center_point(vehicle)
        vehicle_center_screen_pos = world_to_screen_vector(vehicle_center_point)

        img = pygame.transform.smoothscale(vehicle.image, (vehicle_screen_length, vehicle_screen_width))
        vehicle_angle = np.rad2deg(np.arctan2(-vehicle.direction[1], vehicle.direction[0]))
        img = pygame.transform.rotate(img, vehicle_angle)

        car_rect = img.get_rect()
        car_rect.center = vehicle_center_screen_pos
        screen.blit(img, car_rect)

        pygame.draw.circle(screen, "red", vehicle_pivot_screen_pos, 3)

def render_world(screen: Surface, nodes: list[Node], edges: list[Edge]):
    render_nodes(screen, nodes)
    render_edges(screen, edges)
    # render_scenery()
    # render_intersection()

def render_manager(screen, manager):
    # draw position
    manager_screen_pos = world_to_screen_vector(manager.position)
    pygame.draw.circle(screen, "green", manager_screen_pos, 5)

    # draw radius circle
    radius = world_to_screen_scalar(manager.radius)
    diameter = radius*2
    arc_rect = pygame.Rect(0,0,diameter,diameter)
    arc_rect.center = world_to_screen_vector(manager.position)
    pygame.draw.arc(screen, "green", arc_rect, 0, 2*np.pi)

    for i, vehicle in enumerate(manager.vehicles):
        text_surface = FONT.render(f"id: {vehicle.id}, pos: [{vehicle.position[0]:.2f} {vehicle.position[1]:.2f}]", False, (0, 0, 0))
        screen.blit(text_surface, (5,i*20 + 5))