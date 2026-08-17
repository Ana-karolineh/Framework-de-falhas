import numpy as np
import pandas as pd

def get_valve_signals(self):
    from .sim3tanks import Sim3Tanks
    columns = Sim3Tanks.LIST_OF_VALVES
    v = self._get_internal_valve_signals()
    t = self._get_internal_simulation_time()
    if v is None or np.asarray(v).size == 0:
        return pd.DataFrame(columns=columns)
    v = np.atleast_2d(v)
    return pd.DataFrame(v, index=pd.Index(t, name='time (s)'), columns=columns)
