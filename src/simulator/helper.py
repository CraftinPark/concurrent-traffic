import numpy as np
import pygame
from .simulator import WORLD_WIDTH, WORLD_HEIGHT, TOOLBAR_HEIGHT, MAX_ZOOM_FACTOR, MIN_ZOOM_FACTOR
from manager.manager import Manager
from pygame import Surface

zoom_factor = 1

def set_zoomed_helper(updated_zoomed: float):
    global zoom_factor
    zoom_factor = updated_zoomed

def get_x_y_shift(screen: Surface):
    x_shift = 0
    y_shift = 0
    difference = abs(screen.get_height()-TOOLBAR_HEIGHT - screen.get_width())
    if screen.get_width() > screen.get_height():
        x_shift = difference / 2
    return x_shift, y_shift

def world_to_screen_vector(screen: Surface, pos: np.ndarray) -> np.ndarray:
    # not zoomed in when zoom_factor = 1 so we need to subtract by one for the condition below to be 
    if zoom_factor - 1:
        pos = zoom_and_adjust_positions_within_bounds(pos)

    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    render_height = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    x_shift, y_shift = get_x_y_shift(screen)
    return np.array([(pos[0]+(WORLD_WIDTH/2))*render_width/WORLD_WIDTH+x_shift, (pos[1]+(WORLD_HEIGHT/2))*render_height/WORLD_HEIGHT+y_shift])

def world_to_screen_scalar_exterior(screen: Surface, x: float) -> float:
    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)

    return x*render_width/WORLD_WIDTH

# same functionality as world_to_screen_scalar_exterior but zoom operation is applied for objects ONLY within the simulation screen
def world_to_screen_scalar_simulation_screen(screen: Surface, x: float) -> float:
    world_to_screen_scalar_value = world_to_screen_scalar_exterior(screen, x)

    if zoom_factor - 1:
        world_to_screen_scalar_value = world_to_screen_scalar_value * zoom_factor

    return world_to_screen_scalar_value

def zoom_and_adjust_positions_within_bounds(position: np.ndarray) -> np.ndarray:
    # check if position is out of screen, if so, keep it in screen right on the border
    if position[0] * zoom_factor >= 0 and position[1] * zoom_factor >= 0:
        zoomed_position = np.array([min(position[0] * zoom_factor, WORLD_WIDTH/2), min(position[1] * zoom_factor, WORLD_HEIGHT/2)])
    
    elif position[0] * zoom_factor >= 0 and position[1] * zoom_factor <= 0:
        zoomed_position = np.array([min(position[0] * zoom_factor, WORLD_WIDTH/2), max(position[1] * zoom_factor, -WORLD_HEIGHT/2)])
   
    elif position[0] * zoom_factor <= 0 and position[1] * zoom_factor >= 0:
        zoomed_position = np.array([max(position[0] * zoom_factor, -WORLD_WIDTH/2), min(position[1] * zoom_factor, WORLD_HEIGHT/2)])
   
    else:
        zoomed_position = np.array([max(position[0] * zoom_factor, -WORLD_WIDTH/2), max(position[1] * zoom_factor, -WORLD_HEIGHT/2)])

    return zoomed_position

# render only if vehicle is positioned within zoomed screen
def valid_vehicle_render_when_zoomed(vehicle_center_point: list):
        if zoom_factor - 1:
            zoomed_vehicle_center_point = zoom_and_adjust_positions_within_bounds(vehicle_center_point)
            if abs(zoomed_vehicle_center_point[0]) == WORLD_WIDTH / 2 or abs(zoomed_vehicle_center_point[1]) == WORLD_HEIGHT / 2:
                return False
        return True
        
def draw_radius_circle(screen: Surface, manager: Manager):
    radius = world_to_screen_scalar_simulation_screen(screen, manager.radius)
    manager_screen_pos = world_to_screen_vector(screen, manager.position)

    if zoom_factor - 1 :
        circle_radius = 5*zoom_factor
        diameter = radius*2*zoom_factor
        
    else:
        circle_radius = 5
        diameter = radius*2
         # draw radius circle ONLY when complelety zoomed out
        arc_rect = pygame.Rect(0,0,diameter,diameter)
        arc_rect.center = world_to_screen_vector(screen, manager.position)
        pygame.draw.arc(screen, "green", arc_rect, 0, 2*np.pi)

    pygame.draw.circle(screen, "green", manager_screen_pos, circle_radius)

def scroll_handler(event: pygame.event.Event, zoom_factor_simulator: float):

    if event.y > 0:
        zoom_factor_simulator *= 1.1
        if zoom_factor_simulator > MAX_ZOOM_FACTOR:
            zoom_factor_simulator = MAX_ZOOM_FACTOR
    elif event.y < 0:
        zoom_factor_simulator *= 0.9
        if zoom_factor_simulator < MIN_ZOOM_FACTOR:
            zoom_factor_simulator = MIN_ZOOM_FACTOR

    set_zoomed_helper(zoom_factor_simulator)
    return zoom_factor_simulator