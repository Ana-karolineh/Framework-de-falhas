import numpy as np

def sys_measurements(x, q, fault_mag, offset, m_noise):
    from src.sim3tanks.sim3tanks import Sim3Tanks
    N = len(Sim3Tanks.LIST_OF_VALVES)
    x = np.asarray(x, dtype=float)
    q = np.asarray(q, dtype=float)
    fault_mag = np.asarray(fault_mag, dtype=float)
    offset = np.asarray(offset, dtype=float)
    m_noise = np.asarray(m_noise, dtype=float)
    y = np.concatenate([x, q])
    for i in range(len(y)):
        j = N + i
        if fault_mag[j] != 1:
            y[i] = (1 - fault_mag[j]) * y[i] + offset[j] + m_noise[i]
        else:
            y[i] = 0.0
    return y
