from scipy.interpolate import interp1d
import numpy as np

class Command:
    accel_func: interp1d # symoblizes a piecewise function
                                               # 0: acceleration to set to
                                               # 1: the time to set corresponding acceleration
                                               # time should be based on world clock/manager clock

    def __init__(self, t: list[float], a: list[float]) -> None:

        front = a[0] if len(a) > 0 else 0
        end = a[-1] if len(a) > 0 else 0

        self.accel_func = interp1d(t, a, kind='previous', bounds_error=False, fill_value=tuple((front, end)))
    
    def __call__(self, t: float) -> float:
        return self.accel_func(t)
    
def update_cmd(old_cmd: Command, t: list[float], a: list[float], elapsed_time: float=0) -> Command:

    del_index = None
    for i in range(len(old_cmd.accel_func.x)):
        if old_cmd.accel_func.x[i] >= elapsed_time:
            print(i, len(old_cmd.accel_func.x))
            del_index = i
            break

    new_t = list(old_cmd.accel_func.x)[:del_index] + t
    new_a = list(old_cmd.accel_func.y)[:del_index] + a

    return Command(new_t, new_a)