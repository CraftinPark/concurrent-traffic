import numpy as np

class Node():
    position: np.ndarray = np.array([0,0])

    def __init__(self, position: list):
        self.position = position
