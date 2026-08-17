import numpy as np
import pandas as pd

def get_fault_offsets(self):
    from .sim3tanks import Sim3Tanks
    columns = Sim3Tanks.LIST_OF_FAULTS[10:]
    f = self._get_internal_fault_offsets()
    t = self._get_internal_simulation_time()
    if f is None or np.asarray(f).size == 0:
        return pd.DataFrame(columns=columns)
    f = np.atleast_2d(f)
    return pd.DataFrame(f, index=pd.Index(t, name='time (s)'), columns=columns)
