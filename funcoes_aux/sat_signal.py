import numpy as np
from .get_message import Sim3TanksError

def sat_signal(x, x_range):
    if x is None or x_range is None:
        raise Sim3TanksError('ERR001')
    x = np.asarray(x, dtype=float)
    xmin, xmax = x_range
    y = np.minimum(xmax, np.maximum(xmin, x))
    return y
