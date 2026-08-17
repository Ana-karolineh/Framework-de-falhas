import warnings
import numpy as np
from .check_operation_mode import check_operation_mode
from .get_message import Sim3TanksError, get_message
from .sat_signal import sat_signal

def check_enabled_valves(obj):
    from src.sim3tanks.sim3tanks import Sim3Tanks
    if not isinstance(obj, Sim3Tanks):
        raise Sim3TanksError('ERR004')
    LIST_OF_VALVES = Sim3Tanks.LIST_OF_VALVES
    valves = obj.Model.ValveSettings
    op_mode, _ = check_operation_mode(obj)
    valve_id = [None] * len(LIST_OF_VALVES)
    opening_rate = np.zeros(len(LIST_OF_VALVES))
    for i, vname in enumerate(LIST_OF_VALVES):
        valve = getattr(valves, vname)
        if isinstance(valve.EnableControl, bool) and valve.EnableControl:
            if valve.OpeningRate is None:
                warnings.warn(get_message('WARN003'))
                opening_rate[i] = op_mode[i]
            elif valve.OpeningRate < 0 or valve.OpeningRate > 1:
                warnings.warn(get_message('WARN004'))
                opening_rate[i] = float(sat_signal(valve.OpeningRate, (0, 1)))
            else:
                opening_rate[i] = valve.OpeningRate
            valve_id[i] = vname
        elif isinstance(valve.EnableControl, bool):
            opening_rate[i] = op_mode[i]
            valve_id[i] = None
        else:
            raise Sim3TanksError('ERR010')
    return (valve_id, opening_rate)
