import pygame
import numpy as np
from pygame import Surface
from classes.vehicle import Vehicle
from classes.node import Node
from classes.edge import Edge, StraightEdge, CircularEdge
from classes.route import Route, route_position_to_world_position, direction_at_route_position
from manager.manager import Manager
from classes.button import Button
from .helper import world_to_screen_vector, world_to_screen_scalar
from .simulator import WORLD_WIDTH, WORLD_HEIGHT, TOOLBAR_HEIGHT

pygame.font.init()
FONT = pygame.font.SysFont('Consolas', 20)

def render_nodes(screen: Surface, nodes: list[Node]):
    for node in nodes:
        node_position = world_to_screen_vector(screen, node.position)
        pygame.draw.circle(screen, "red", node_position, 3)

def render_edges(screen: Surface, edges: list[Edge]):
    for edge in edges:
        if isinstance(edge, StraightEdge):
            start_position = world_to_screen_vector(screen, edge.start.position)
            end_position   = world_to_screen_vector(screen, edge.end.position)
            pygame.draw.line(screen, "red", start_position, end_position)
        elif isinstance(edge, CircularEdge):
            # define rect
            radius = world_to_screen_scalar(screen, np.linalg.norm(edge.start.position-edge.center)) # norm describes distance
            diameter = radius*2
            arc_rect = pygame.Rect(0,0,diameter,diameter)
            arc_rect.center = world_to_screen_vector(screen, edge.center)

            theta_start = np.arctan2(-(edge.start.position[1] - edge.center[1]), edge.start.position[0] - edge.center[0])
            theta_end = np.arctan2(-(edge.end.position[1] - edge.center[1]), edge.end.position[0] - edge.center[0])

            if edge.clockwise:
                if theta_end < theta_start:
                    theta_end += 2*np.pi
                theta_end, theta_start = theta_start, theta_end
            else:
                if theta_start < theta_end:
                    theta_start += 2*np.pi

            pygame.draw.arc(screen, "red", arc_rect, theta_start, theta_end)

def render_intersections(screen: Surface, intersection_points):
    for intersection in intersection_points:
        node_position = world_to_screen_vector(screen, np.array(list(intersection[2])))
        pygame.draw.circle(screen, "blue", node_position, 3)

def render_vehicles(screen: Surface, vehicles: list[Vehicle]):
    for vehicle in vehicles:
        vehicle_screen_width = world_to_screen_scalar(screen, vehicle.width)
        vehicle_screen_length = world_to_screen_scalar(screen, vehicle.length)

        vehicle_center_point = route_position_to_world_position(vehicle.route, vehicle.route_position)
        vehicle_center_screen_pos = world_to_screen_vector(screen, vehicle_center_point)

        img = pygame.transform.smoothscale(vehicle.image, (vehicle_screen_length, vehicle_screen_width))
        vehicle_angle = direction_at_route_position(vehicle.route, vehicle.route_position)
        img = pygame.transform.rotate(img, vehicle_angle)

        car_rect = img.get_rect()
        car_rect.center = vehicle_center_screen_pos
        screen.blit(img, car_rect)

        pygame.draw.circle(screen, "red", vehicle_center_screen_pos, 3)

def render_background(screen: Surface):
    position = world_to_screen_vector(screen, [-WORLD_WIDTH/2,-WORLD_HEIGHT/2])
    width = world_to_screen_scalar(screen, WORLD_WIDTH)
    height = world_to_screen_scalar(screen, WORLD_HEIGHT)
    pygame.draw.rect(screen, "grey", pygame.Rect(position[0], position[1], width, height))

def render_border(screen: Surface):
    position = world_to_screen_vector(screen, [-WORLD_WIDTH/2,-WORLD_HEIGHT/2])
    width = world_to_screen_scalar(screen, WORLD_WIDTH)
    height = world_to_screen_scalar(screen, WORLD_HEIGHT)
    pygame.draw.rect(screen, "maroon", pygame.Rect(position[0]-3, position[1]-3, width+6, height+6),3)

def render_world(screen: Surface, nodes: list[Node], edges: list[Edge], route_visible: bool, intersection_points):
    render_background(screen)
    if route_visible:
        render_nodes(screen, nodes)
        render_edges(screen, edges)
        render_arrows(screen, edges)
    render_intersections(screen, intersection_points)
    render_border(screen)
    # render_scenery()

def render_manager(screen, manager):
    # draw position
    manager_screen_pos = world_to_screen_vector(screen, manager.position)
    pygame.draw.circle(screen, "green", manager_screen_pos, 5)

    # draw radius circle
    radius = world_to_screen_scalar(screen, manager.radius)
    diameter = radius*2
    arc_rect = pygame.Rect(0,0,diameter,diameter)
    arc_rect.center = world_to_screen_vector(screen, manager.position)
    pygame.draw.arc(screen, "green", arc_rect, 0, 2*np.pi)

    for i, vehicle in enumerate(manager.vehicles):
        font = pygame.font.SysFont('Segoe UI', 15)
        text_surface = font.render(f"id: {vehicle.id}, pos: {vehicle.route_position:.2f}", True, (0, 0, 0))
        screen.blit(text_surface, (5,i*20 + 5))

def render_time(screen, toolbar_rect, time_elapsed): 
    font = pygame.font.SysFont('Segoe UI', 15)
    text_surface = font.render(f"Time: {time_elapsed:.3f}", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.right = 150
    screen.blit(text_surface, text_surface.get_rect(topright = (screen.get_width()-3, screen.get_height()-TOOLBAR_HEIGHT)))

def render_buttons(screen: Surface, buttons: list[Button]) -> None:
    for b in buttons:
        b.y = screen.get_height()-TOOLBAR_HEIGHT+50
        pygame.draw.rect(screen, b.hover_color if b.is_selected() else b.color, [b.x , b.y, b.width, b.height])
        if b.text != '':
            font = pygame.font.SysFont('Segoe UI', 15)
            text = font.render(b.text, 1, (255, 255, 255))
            screen.blit(text, (b.x + (b.width/2 - text.get_width()/2), b.y + (b.height/2 - text.get_height()/2)))

def render_title(screen): 
    # draw title and version
    FONT = pygame.font.SysFont("Segoe UI", 15, bold=True, italic=False)
    text_surface = FONT.render(f"Concurent Traffic v0.0.2", True, (255, 255, 255))
    screen.blit(text_surface, (0, screen.get_height()-TOOLBAR_HEIGHT))

def render_toolbar(screen, time_elapsed, buttons):
    toolbar_rect = pygame.Rect(0, screen.get_height()-TOOLBAR_HEIGHT,screen.get_width(),TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, pygame.Color(80,80,80), toolbar_rect)
    render_time(screen, toolbar_rect, time_elapsed)
    render_buttons(screen, buttons)
    render_title(screen)

def render_arrows(screen: Surface, edges: list[Edge]):
    def create_rotation_matrix(degrees):   
        # creates rotation matrix    
        theta = np.radians(degrees)
        cos, sin = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array(((cos, -sin), (sin, cos)))
        return rotation_matrix
    
    def rotate_vector(size, matrix, edge_unit_vector, midpoint_position):
        # dot product of unit vector and its rotation matrix
        vector = size * np.dot(edge_unit_vector, matrix) + midpoint_position
        return vector
            
    for edge in edges:
        if isinstance(edge, StraightEdge):
            # converts start and end position to screen position
            start_position = world_to_screen_vector(screen, edge.start.position)
            end_position = world_to_screen_vector(screen, edge.end.position)
            
            # finds midpoint of edge
            midpoint_position = (start_position + end_position) / 2
            mid_pos_world = (edge.start.position + edge.end.position) / 2

            # finds direction of edge
            edge_vector = edge.end.position - edge.start.position
            edge_unit_vector = edge_vector / np.linalg.norm(edge_vector)

            # create rotation matrix to rotate edge_unit_vector
            rotation_pos_matrix = create_rotation_matrix(140)
            rotation_neg_matrix = create_rotation_matrix(-140)

            # rotates vectors to creates arrows
            positive_vector = rotate_vector(0.9, rotation_pos_matrix, edge_unit_vector, mid_pos_world)
            negative_vector = rotate_vector(0.9, rotation_neg_matrix, edge_unit_vector, mid_pos_world)
            
            # converts to screen position
            screen_pos_vector = world_to_screen_vector(screen, positive_vector)
            screen_neg_vector = world_to_screen_vector(screen, negative_vector)

            # draws onto screen
            pygame.draw.aaline(screen, "red", screen_pos_vector, midpoint_position, blend=40)
            pygame.draw.aaline(screen, "red", screen_neg_vector, midpoint_position, blend=40)

        elif isinstance(edge, CircularEdge):
            # define rect
            radius = np.linalg.norm(edge.start.position-edge.center) # norm describes distance

            theta_start = np.arctan2((edge.start.position[1] - edge.center[1]), edge.start.position[0] - edge.center[0])
            theta_end = np.arctan2((edge.end.position[1] - edge.center[1]), edge.end.position[0] - edge.center[0])

            if edge.clockwise:
                if theta_end < theta_start:
                    theta_end += 2*np.pi
                theta_end, theta_start = theta_start, theta_end
            else:
                if theta_start < theta_end:
                    theta_start += 2*np.pi
            
            theta_midpoint = (theta_start + theta_end) / 2
            center_point_world = (edge.center[0] + radius*np.cos(theta_midpoint), edge.center[1] + radius*np.sin(theta_midpoint)) # (x,y) = (a+r*cos(theta), b+r*sin(theta))
            tangent_line_world = (-radius*np.sin(theta_midpoint), radius*np.cos(theta_midpoint)) # derivative of center_point_world, finding tangent line of midpoint of the arc
            unit_vector = tangent_line_world / np.linalg.norm(tangent_line_world)
            
            # create rotation matrix
            pos_matrix = create_rotation_matrix(250)
            neg_matrix = create_rotation_matrix(-225)
            
            # rotate unit vector to create arrows
            positive_vector = rotate_vector(0.6, pos_matrix, unit_vector, center_point_world)
            negative_vector = rotate_vector(0.6, neg_matrix, unit_vector, center_point_world)

            # convert to screen vector & draw
            center_point = world_to_screen_vector(screen, center_point_world)
            positive_screen_vector = world_to_screen_vector(screen, positive_vector)
            negative_screen_vector = world_to_screen_vector(screen, negative_vector)

            pygame.draw.aaline(screen, "red", center_point, positive_screen_vector)
            pygame.draw.aaline(screen, "red", center_point, negative_screen_vector)



