import warnings
import numpy as np
from .get_message import Sim3TanksError, get_message

def check_enabled_noises(obj):
    from src.sim3tanks.sim3tanks import Sim3Tanks
    if not isinstance(obj, Sim3Tanks):
        raise Sim3TanksError('ERR004')
    Nx = len(Sim3Tanks.LIST_OF_STATES)
    Nq = len(Sim3Tanks.LIST_OF_FLOWS)
    pn = obj.Model.ProcessNoise
    if isinstance(pn.EnableSignal, bool) and pn.EnableSignal:
        if pn.Magnitude is None:
            warnings.warn(get_message('WARN005'))
            p_noise = np.zeros(Nx)
        elif len(pn.Magnitude) != Nx:
            raise Sim3TanksError('ERR006')
        else:
            p_noise = np.asarray(pn.Magnitude, dtype=float)
    elif isinstance(pn.EnableSignal, bool):
        p_noise = np.zeros(Nx)
    else:
        raise Sim3TanksError('ERR011')
    mn = obj.Model.MeasurementNoise
    if isinstance(mn.EnableSignal, bool) and mn.EnableSignal:
        if mn.Magnitude is None:
            warnings.warn(get_message('WARN006'))
            m_noise = np.zeros(Nx + Nq)
        elif len(mn.Magnitude) != Nx + Nq:
            raise Sim3TanksError('ERR006')
        else:
            m_noise = np.asarray(mn.Magnitude, dtype=float)
    elif isinstance(mn.EnableSignal, bool):
        m_noise = np.zeros(Nx + Nq)
    else:
        raise Sim3TanksError('ERR011')
    return (p_noise, m_noise)
