import numpy as np
from enum import Enum

class Direction(Enum):
    NORTH_BOUND = 0
    EAST_BOUND = 1
    WEST_BOUND = 2
    SOUTH_BOUND = 3

class Vehicle:
    def __init__(self, pos: list[2], vel: list[2], acc: list[2], dir: Direction):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.dir = dir
        self.distance_to_intersection = None