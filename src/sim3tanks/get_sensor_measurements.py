import numpy as np
import pandas as pd

def get_sensor_measurements(self):
    from .sim3tanks import Sim3Tanks
    columns = Sim3Tanks.LIST_OF_STATES + Sim3Tanks.LIST_OF_FLOWS
    y = self._get_internal_sensor_measurements()
    t = self._get_internal_simulation_time()
    if y is None or np.asarray(y).size == 0:
        return pd.DataFrame(columns=columns)
    y = np.atleast_2d(y)
    return pd.DataFrame(y, index=pd.Index(t, name='time (s)'), columns=columns)
