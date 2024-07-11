from scipy.interpolate import interp1d
import numpy as np

class Command:
    """Command is sent to a Vehicle to dictate the Vehicle's acceleration over time."""
    accel_func: interp1d # symoblizes a piecewise function
                                               # 0: acceleration to set to
                                               # 1: the time to set corresponding acceleration
                                               # time should be based on world clock/manager clock

    def __init__(self, t: np.array, a: np.array) -> None:
        front = a[0] if len(a) > 0 else 0
        end = a[-1] if len(a) > 0 else 0
        self.accel_func = interp1d(t, a, kind='previous', bounds_error=False, fill_value=tuple((front, end)))
    
    def __call__(self, t: float) -> float:
        """Return the accleration value for a given time t."""
        return self.accel_func(t)