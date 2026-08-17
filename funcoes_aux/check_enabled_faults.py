import warnings
import numpy as np
from .get_message import Sim3TanksError, get_message
from .sat_signal import sat_signal

def check_enabled_faults(obj):
    from src.sim3tanks.sim3tanks import Sim3Tanks
    if not isinstance(obj, Sim3Tanks):
        raise Sim3TanksError('ERR004')
    LIST_OF_FAULTS = Sim3Tanks.LIST_OF_FAULTS
    faults_struct = obj.Model.FaultSettings
    fault_id = [None] * len(LIST_OF_FAULTS)
    fault_mag = np.zeros(len(LIST_OF_FAULTS))
    offset = np.zeros(len(LIST_OF_FAULTS))
    for i, fname in enumerate(LIST_OF_FAULTS):
        fault = getattr(faults_struct, fname)
        if isinstance(fault.EnableSignal, bool) and fault.EnableSignal:
            if fault.Magnitude is None:
                warnings.warn(get_message('WARN001'))
                fault_mag[i] = 0.0
            elif fault.Magnitude < 0 or fault.Magnitude > 1:
                warnings.warn(get_message('WARN002'))
                fault_mag[i] = float(sat_signal(fault.Magnitude, (0, 1)))
            else:
                fault_mag[i] = fault.Magnitude
            if hasattr(fault, 'Offset'):
                if fault.Offset is None:
                    warnings.warn(get_message('WARN007'))
                    offset[i] = 0.0
                elif not np.isfinite(fault.Offset):
                    raise Sim3TanksError('ERR022')
                else:
                    offset[i] = fault.Offset
            fault_id[i] = fname
        elif isinstance(fault.EnableSignal, bool):
            fault_id[i] = None
            fault_mag[i] = 0.0
            offset[i] = 0.0
        else:
            raise Sim3TanksError('ERR011')
    return (fault_id, fault_mag, offset)
