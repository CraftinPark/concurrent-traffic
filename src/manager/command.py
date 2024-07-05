from scipy.interpolate import interp1d
import numpy as np

class Command:
    accel_func: interp1d # symoblizes a piecewise function
                                               # 0: acceleration to set to
                                               # 1: the time to set corresponding acceleration
                                               # time should be based on world clock/manager clock

    def __init__(self, t: float, a: float) -> None:
        self.accel_func = interp1d(t, a, kind='previous', bounds_error=False, fill_value=tuple((a[0], a[-1])))
    
    def eval(self, t: float) -> float:
        return self.accel_func(t)
    
    def update_cmd(self, t: float, a: float, elapsed_time: float=0) -> None:

        del_index = None
        for i in range(len(self.accel_func.x)):
            if self.accel_func.x[i] >= elapsed_time:
                del_index = i
                break
        
        if del_index is not None:
            self.accel_func.x = np.delete(self.accel_func.x, np.s_[del_index:])
            self.accel_func.y = np.delete(self.accel_func.y, np.s_[del_index:])

        self.accel_func.x = np.concatenate((self.accel_func.x, t))
        self.accel_func.y = np.concatenate((self.accel_func.y, a))