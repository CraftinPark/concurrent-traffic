import numpy as np
import pygame
from pygame import Surface

class Vehicle:
    position: np.ndarray     = np.array([0,0]) # numpy array[2] describing world coordinates. position refers to pivot point, located between back wheels
    velocity: np.ndarray     = np.array([0,0]) # numpy array[2] describing euclidean velocity vector
    acceleration: np.ndarray = np.array([0,0]) # numpy array[2] describing euclidean acceleration vector
    direction: np.ndarray    = np.array([1,0]) # numpy array[2] describing unit directional vector
    width: float             = 2.23            # float representing width of car in meters. orthogonal to direction
    length: float            = 4.90            # float representing length of car in meters. parallel to direction
    pivot_distance: float    = 1.25            # float representing distance from pivot to center.

    image: Surface

    def __init__(self, position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray, direction: np.ndarray, width: float, length: float, image_source: str):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.direction = direction
        self.width = width
        self.length = length
        self.image = pygame.image.load(image_source)