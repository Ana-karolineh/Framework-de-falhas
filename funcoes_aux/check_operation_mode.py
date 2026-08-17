import numpy as np
from .get_message import Sim3TanksError

def check_operation_mode(obj):
    from src.sim3tanks.sim3tanks import Sim3Tanks
    if not isinstance(obj, Sim3Tanks):
        raise Sim3TanksError('ERR004')
    LIST_OF_VALVES = Sim3Tanks.LIST_OF_VALVES
    valves = obj.Model.ValveSettings
    op_mode = np.zeros(len(LIST_OF_VALVES))
    valve_id = [None] * len(LIST_OF_VALVES)
    for i, vname in enumerate(LIST_OF_VALVES):
        mode = getattr(valves, vname).OperationMode
        if isinstance(mode, str) and mode.lower() == 'open':
            op_mode[i] = 1.0
        elif isinstance(mode, str) and mode.lower() == 'closed':
            op_mode[i] = 0.0
        else:
            raise Sim3TanksError('ERR009')
        valve_id[i] = vname
    return (op_mode, valve_id)
