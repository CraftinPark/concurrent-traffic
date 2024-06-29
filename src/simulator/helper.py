import numpy as np
from .simulator import WORLD_WIDTH, WORLD_HEIGHT, TOOLBAR_HEIGHT
from pygame import Surface

def get_x_y_shift(screen: Surface):
    x_shift = 0
    y_shift = 0
    difference = abs(screen.get_height()-TOOLBAR_HEIGHT - screen.get_width())
    if screen.get_width() > screen.get_height():
        x_shift = difference / 2
    return x_shift, y_shift

def world_to_screen_vector(screen: Surface, pos: np.ndarray) -> np.ndarray:
    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    render_height = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    x_shift, y_shift = get_x_y_shift(screen)
    return np.array([(pos[0]+(WORLD_WIDTH/2))*render_width/WORLD_WIDTH+x_shift, (pos[1]+(WORLD_HEIGHT/2))*render_height/WORLD_HEIGHT+y_shift])

def world_to_screen_scalar(screen: Surface, x: float) -> float:
    render_width = min(screen.get_width(), screen.get_height()-TOOLBAR_HEIGHT)
    return x*render_width/WORLD_WIDTH