import numpy as np
from .simulator import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

def world_to_screen_vector(pos: np.ndarray) -> np.ndarray:
    return np.array([(pos[0]+(WORLD_WIDTH/2))*SCREEN_WIDTH/WORLD_WIDTH, (pos[1]+(WORLD_HEIGHT/2))*SCREEN_HEIGHT/WORLD_HEIGHT])

def world_to_screen_scalar(x: float) -> float:
    return x*SCREEN_WIDTH/WORLD_WIDTH