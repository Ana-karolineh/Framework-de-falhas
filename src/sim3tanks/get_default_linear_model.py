import warnings
import numpy as np
from funcoes_aux.check_physical_param import check_physical_param
from funcoes_aux.get_message import Sim3TanksError

def get_default_linear_model(self, x1op, method=None, tspan=None):
    from .sim3tanks import Struct
    Param, ID = check_physical_param(self)
    Rtank = Param[ID[0]]
    Hmax = Param[ID[1]]
    Rpipe = Param[ID[2]]
    mu = Param[ID[4]]
    g = Param[ID[5]]
    Qmax = Param[ID[7]]
    Sc = np.pi * Rtank ** 2
    S = np.pi * Rpipe ** 2
    Beta = mu * S * np.sqrt(2 * g)
    if not (np.isfinite(x1op) and np.isscalar(x1op) and (x1op > 0) and (x1op < Hmax)):
        raise Sim3TanksError('ERR003')
    x2op = x1op
    x3op = 4 / 5 * x1op
    u1op = Beta / Qmax * np.sqrt(x1op / 5)
    u2op = u1op
    X13 = x1op - x3op
    X23 = x2op - x3op
    Q13op = Beta * np.sign(X13) * np.sqrt(abs(X13))
    Q23op = Beta * np.sign(X23) * np.sqrt(abs(X23))
    Q3op = Beta * np.sqrt(x3op)
    x_op = np.array([x1op, x2op, x3op])
    u_op = np.array([u1op, u2op])
    y_op = np.array([x1op, x2op, Q13op, Q23op, Q3op])
    a11 = -(1 / np.sqrt(abs(X13))) * (X13 / abs(X13))
    a22 = -(1 / np.sqrt(abs(X23))) * (X23 / abs(X23))
    a33 = -(1 / np.sqrt(x3op)) + a11 + a22
    A = Beta / (2 * Sc) * np.array([[a11, 0, -a11], [0, a22, -a22], [-a11, -a22, a33]])
    B = 1 / Sc * np.array([[Qmax, 0], [0, Qmax], [0, 0]])
    Cx = np.array([[1, 0, 0], [0, 1, 0]])
    Cq = Beta / 2 * np.array([[-a11, 0, a11], [0, -a22, a22], [0, 0, 1 / np.sqrt(x3op)]])
    C = np.vstack([Cx, Cq])
    D = np.zeros((C.shape[0], B.shape[1]))
    OP = Struct(x=x_op, u=u_op, y=y_op)
    if method is None and tspan is None:
        try:
            import control
            SYS = control.ss(A, B, C, D)
        except ImportError:
            warnings.warn("Pacote 'control' não encontrado (pip install control); retornando (A,B,C,D) em vez de um objeto ss().")
            SYS = Struct(A=A, B=B, C=C, D=D)
        return (SYS, OP)
    if method is None or tspan is None:
        raise Sim3TanksError('ERR021')
    valid_methods = ['zoh', 'foh', 'impulse', 'tustin', 'matched', 'euler']
    if method.lower() not in valid_methods:
        raise Sim3TanksError('ERR003')
    if not (np.isfinite(tspan) and np.isscalar(tspan) and (tspan > 0)):
        raise Sim3TanksError('ERR003')
    if method.lower() == 'euler':
        nx = A.shape[1]
        Ad = np.eye(nx) + tspan * A
        Bd = tspan * B
        try:
            import control
            SYS = control.ss(Ad, Bd, C, D, tspan)
        except ImportError:
            SYS = Struct(A=Ad, B=Bd, C=C, D=D, dt=tspan)
    else:
        try:
            import control
            SYS = control.ss(A, B, C, D)
            SYS = control.c2d(SYS, tspan, method.lower())
        except ImportError:
            raise Sim3TanksError('ERR000', "Pacote 'control' necessário para métodos != 'euler'.")
    return (SYS, OP)
