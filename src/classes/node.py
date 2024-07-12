import numpy as np

class Node():
    """A Node is a point consisting of x, y coordinates."""
    position: np.ndarray = np.array([0,0])

    def __init__(self, position: list) -> None:
        self.position = position