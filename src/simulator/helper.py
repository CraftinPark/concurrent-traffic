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
    pos = np.array([pos[0] * zoom_factor,pos[1] * zoom_factor])

    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    render_height = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    x_shift, y_shift = get_x_y_shift(screen)
    return np.array([(pos[0]+(WORLD_WIDTH/2))*render_width/WORLD_WIDTH+x_shift, (pos[1]+(WORLD_HEIGHT/2))*render_height/WORLD_HEIGHT+y_shift])

def world_to_screen_scalar(screen: Surface, x: float) -> float:
    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    render_width = render_width * zoom_factor

    return x*render_width/WORLD_WIDTH

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