import numpy as np
from .get_message import Sim3TanksError

def check_physical_param(obj):
    from src.sim3tanks.sim3tanks import Sim3Tanks
    if not isinstance(obj, Sim3Tanks):
        raise Sim3TanksError('ERR004')
    LIST_OF_PARAM = Sim3Tanks.LIST_OF_PARAM
    phys = obj.Model.PhysicalParam
    values = {}
    for name in LIST_OF_PARAM:
        value = getattr(phys, name)
        if value is None:
            raise Sim3TanksError('ERR008')
        elif isinstance(value, (int, float)) and np.isfinite(value):
            values[name] = value
        else:
            raise Sim3TanksError('ERR008')
    if not values[LIST_OF_PARAM[0]] > 0:
        raise Sim3TanksError('ERR012')
    elif not values[LIST_OF_PARAM[1]] > 0:
        raise Sim3TanksError('ERR013')
    elif not 0 < values[LIST_OF_PARAM[2]] < values[LIST_OF_PARAM[0]]:
        raise Sim3TanksError('ERR014')
    elif not 0 < values[LIST_OF_PARAM[3]] < values[LIST_OF_PARAM[1]]:
        raise Sim3TanksError('ERR015')
    elif not values[LIST_OF_PARAM[4]] > 0:
        raise Sim3TanksError('ERR016')
    elif not values[LIST_OF_PARAM[5]] > 0:
        raise Sim3TanksError('ERR017')
    elif not values[LIST_OF_PARAM[6]] >= 0:
        raise Sim3TanksError('ERR018')
    elif not values[LIST_OF_PARAM[7]] >= values[LIST_OF_PARAM[6]]:
        raise Sim3TanksError('ERR019')
    return (values, LIST_OF_PARAM)
