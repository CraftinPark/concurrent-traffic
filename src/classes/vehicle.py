class Vehicle:
    position = None     # numpy array[2] describing world coordinates
    velocity = None     # numpy array[2] describing euclidean velocity vector
    acceleration = None # numpy array[2] describing euclidean acceleration vector
    direction = None    # numpy array[2] describing unit directional vector
    width = None        # float representing width of car in meters. orthogonal to direction
    length = None       # float representing length of car in meters. parallel to direction

    def __init__(self, position, velocity, acceleration, direction, width, height):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.dir = direction
        self.width = width
        self.height = height