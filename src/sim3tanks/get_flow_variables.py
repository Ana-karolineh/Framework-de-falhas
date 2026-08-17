import numpy as np
import pandas as pd

def get_flow_variables(self):
    from .sim3tanks import Sim3Tanks
    columns = Sim3Tanks.LIST_OF_FLOWS
    q = self._get_internal_flow_variables()
    t = self._get_internal_simulation_time()
    if q is None or np.asarray(q).size == 0:
        return pd.DataFrame(columns=columns)
    q = np.atleast_2d(q)
    return pd.DataFrame(q, index=pd.Index(t, name='time (s)'), columns=columns)
