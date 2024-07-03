import numpy as np
import pygame
from .simulator import WORLD_WIDTH, WORLD_HEIGHT, TOOLBAR_HEIGHT, ZOOM_FACTOR
from pygame import Surface

def get_x_y_shift(screen: Surface):
    x_shift = 0
    y_shift = 0
    difference = abs(screen.get_height()-TOOLBAR_HEIGHT - screen.get_width())
    if screen.get_width() > screen.get_height():
        x_shift = difference / 2
    return x_shift, y_shift

def world_to_screen_vector(screen: Surface, pos: np.ndarray, zoomed: bool) -> np.ndarray:
    if zoomed:
        pos = zoom_and_adjust_positions_within_bounds(pos)

    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    render_height = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    x_shift, y_shift = get_x_y_shift(screen)
    return np.array([(pos[0]+(WORLD_WIDTH/2))*render_width/WORLD_WIDTH+x_shift, (pos[1]+(WORLD_HEIGHT/2))*render_height/WORLD_HEIGHT+y_shift])

def world_to_screen_scalar(screen: Surface, x: float) -> float:
    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    return x*render_width/WORLD_WIDTH

def zoom_and_adjust_positions_within_bounds(position: np.ndarray) -> np.ndarray:
    # check if position is out of screen, if so, keep it in screen right on the border
    if position[0] * ZOOM_FACTOR >= 0 and position[1] * ZOOM_FACTOR >= 0:
        zoomed_position = np.array([min(position[0] * ZOOM_FACTOR, WORLD_WIDTH/2), min(position[1] * ZOOM_FACTOR, WORLD_HEIGHT/2)])
    
    elif position[0] * ZOOM_FACTOR >= 0 and position[1] * ZOOM_FACTOR <= 0:
        zoomed_position = np.array([min(position[0] * ZOOM_FACTOR, WORLD_WIDTH/2), max(position[1] * ZOOM_FACTOR, -WORLD_HEIGHT/2)])
   
    elif position[0] * ZOOM_FACTOR <= 0 and position[1] * ZOOM_FACTOR >= 0:
        zoomed_position = np.array([max(position[0] * ZOOM_FACTOR, -WORLD_WIDTH/2), min(position[1] * ZOOM_FACTOR, WORLD_HEIGHT/2)])
   
    else:
        zoomed_position = np.array([max(position[0] * ZOOM_FACTOR, -WORLD_WIDTH/2), max(position[1] * ZOOM_FACTOR, -WORLD_HEIGHT/2)])

    return zoomed_position

