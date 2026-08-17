import numpy as np
from .sys_flow_rates import sys_flow_rates

def sys_dynamics(t, x, Qin, K, h0, Sc, Beta, w):
    Qin = np.asarray(Qin, dtype=float)
    w = np.asarray(w, dtype=float)
    Q1in, Q2in, Q3in = (Qin[0], Qin[1], Qin[2])
    Qx = sys_flow_rates(x, K, h0, Beta)
    Qa, Qb, Q13, Q23, Q1, Q2, Q3 = Qx
    dx1_dt = 1.0 / Sc * (Q1in - Qa - Q13 - Q1) + w[0]
    dx2_dt = 1.0 / Sc * (Q2in - Qb - Q23 - Q2) + w[1]
    dx3_dt = 1.0 / Sc * (Q3in + Q13 + Q23 + Qa + Qb - Q3) + w[2]
    return np.array([dx1_dt, dx2_dt, dx3_dt], dtype=float)
