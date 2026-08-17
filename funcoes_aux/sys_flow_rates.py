import numpy as np
from .get_message import Sim3TanksError

def sys_flow_rates(x, K, h0, Beta):
    x = np.asarray(x, dtype=float)
    K = np.asarray(K, dtype=float)
    h1, h2, h3 = (x[0], x[1], x[2])
    K_a, K_b, K_13, K_23, K_1, K_2, K_3 = (K[3], K[4], K[5], K[6], K[7], K[8], K[9])
    if h1 <= h0 and h2 <= h0 and (h3 <= h0):
        Qa = K_a * 0.0
        Qb = K_b * 0.0
    elif h1 <= h0 and h2 <= h0 and (h3 > h0):
        Qa = K_a * Beta * np.sign(h0 - h3) * np.sqrt(abs(h0 - h3))
        Qb = K_b * Beta * np.sign(h0 - h3) * np.sqrt(abs(h0 - h3))
    elif h1 <= h0 and h2 > h0 and (h3 <= h0):
        Qa = K_a * 0.0
        Qb = K_b * Beta * np.sign(h2 - h3) * np.sqrt(abs(h2 - h3))
    elif h1 <= h0 and h2 > h0 and (h3 > h0):
        Qa = K_a * Beta * np.sign(h0 - h3) * np.sqrt(abs(h0 - h3))
        Qb = K_b * Beta * np.sign(h2 - h3) * np.sqrt(abs(h2 - h3))
    elif h1 > h0 and h2 <= h0 and (h3 <= h0):
        Qa = K_a * Beta * np.sign(h1 - h0) * np.sqrt(abs(h1 - h0))
        Qb = K_b * 0.0
    elif h1 > h0 and h2 <= h0 and (h3 > h0):
        Qa = K_a * Beta * np.sign(h1 - h3) * np.sqrt(abs(h1 - h3))
        Qb = K_b * Beta * np.sign(h0 - h3) * np.sqrt(abs(h0 - h3))
    elif h1 > h0 and h2 > h0 and (h3 <= h0):
        Qa = K_a * Beta * np.sign(h1 - h0) * np.sqrt(abs(h1 - h0))
        Qb = K_b * Beta * np.sign(h2 - h0) * np.sqrt(abs(h2 - h0))
    elif h1 > h0 and h2 > h0 and (h3 > h0):
        Qa = K_a * Beta * np.sign(h1 - h3) * np.sqrt(abs(h1 - h3))
        Qb = K_b * Beta * np.sign(h2 - h3) * np.sqrt(abs(h2 - h3))
    else:
        raise Sim3TanksError('ERR000')
    Q13 = K_13 * Beta * np.sign(h1 - h3) * np.sqrt(abs(h1 - h3))
    Q23 = K_23 * Beta * np.sign(h2 - h3) * np.sqrt(abs(h2 - h3))
    Q1 = K_1 * Beta * np.sqrt(abs(h1))
    Q2 = K_2 * Beta * np.sqrt(abs(h2))
    Q3 = K_3 * Beta * np.sqrt(abs(h3))
    return np.array([Qa, Qb, Q13, Q23, Q1, Q2, Q3], dtype=float)
