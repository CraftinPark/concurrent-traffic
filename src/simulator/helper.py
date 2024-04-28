import numpy as np
from .simulator import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

def world_to_screen_vector(x: float, y: float):
    return [(x+(WORLD_WIDTH/2))*SCREEN_WIDTH/WORLD_WIDTH, (y+(WORLD_HEIGHT/2))*SCREEN_HEIGHT/WORLD_HEIGHT]

def world_to_screen_scalar(x: float):
    return x*SCREEN_WIDTH/WORLD_WIDTH

def distance(vector1: list, vector2: list):
    vec1 = np.array(vector1)
    vec2 = np.array(vector2)
    return np.linalg.norm(vec2-vec1)