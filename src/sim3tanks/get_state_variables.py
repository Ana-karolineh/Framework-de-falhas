import numpy as np
import pandas as pd

def get_state_variables(self):
    from .sim3tanks import Sim3Tanks
    columns = Sim3Tanks.LIST_OF_STATES
    x = self._get_internal_state_variables()
    t = self._get_internal_simulation_time()
    if x is None or np.asarray(x).size == 0:
        return pd.DataFrame(columns=columns)
    x = np.atleast_2d(x)
    return pd.DataFrame(x, index=pd.Index(t, name='time (s)'), columns=columns)
