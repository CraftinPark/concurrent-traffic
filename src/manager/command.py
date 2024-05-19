
class Command:
    acceleration_sets: list[float, float] = [] # symoblizes a piecewise function
                                               # 0: acceleration to set to
                                               # 1: the time to set corresponding acceleration
                                               # time should be based on world clock/manager clock

    def __init__(self, acceleration_sets: list[float, float]):
        self.acceleration_sets = acceleration_sets