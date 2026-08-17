import numpy as np
from scipy.integrate import solve_ivp
from funcoes_aux.check_enabled_faults import check_enabled_faults
from funcoes_aux.check_enabled_noises import check_enabled_noises
from funcoes_aux.check_enabled_valves import check_enabled_valves
from funcoes_aux.check_operation_mode import check_operation_mode
from funcoes_aux.check_physical_param import check_physical_param
from funcoes_aux.get_message import Sim3TanksError
from funcoes_aux.sat_signal import sat_signal
from funcoes_aux.sys_flow_rates import sys_flow_rates
from funcoes_aux.sys_measurements import sys_measurements

def simulate_model(self, Qp1=None, Qp2=None, Qp3=None, Tspan=0.1, all_steps=False):
    from .sim3tanks import Sim3Tanks
    Param, ID = check_physical_param(self)
    Rtank = Param[ID[0]]
    Hmax = Param[ID[1]]
    Rpipe = Param[ID[2]]
    h0 = Param[ID[3]]
    mu = Param[ID[4]]
    g = Param[ID[5]]
    Qmin = Param[ID[6]]
    Qmax = Param[ID[7]]
    Sc = np.pi * Rtank ** 2
    S = np.pi * Rpipe ** 2
    Beta = mu * S * np.sqrt(2 * g)
    Qp1 = Qmax if Qp1 is None else Qp1
    Qp2 = Qmax if Qp2 is None else Qp2
    Qp3 = Qmax if Qp3 is None else Qp3
    op_mode, _ = check_operation_mode(self)
    valve_id, opening_rate = check_enabled_valves(self)
    fault_id, fault_mag, offset = check_enabled_faults(self)
    K = np.zeros(len(op_mode))
    for i in range(len(op_mode)):
        OP = bool(op_mode[i])
        EC = valve_id[i] is None
        EF = fault_id[i] is None
        if not OP and EC and EF or (OP and EC and EF):
            K[i] = float(OP)
        elif not OP and EC and (not EF):
            K[i] = fault_mag[i]
        elif not OP and (not EC) and EF or (OP and (not EC) and EF):
            K[i] = opening_rate[i]
        elif not OP and (not EC) and (not EF) or (OP and (not EC) and (not EF)):
            K[i] = opening_rate[i] * (1 - fault_mag[i])
        elif OP and EC and (not EF):
            K[i] = 1 - fault_mag[i]
        else:
            raise Sim3TanksError('ERR000')
    Nx = len(Sim3Tanks.LIST_OF_STATES)
    Nq = len(Sim3Tanks.LIST_OF_FLOWS)
    Qin = np.array([K[0] * float(sat_signal(Qp1, (Qmin, Qmax))), K[1] * float(sat_signal(Qp2, (Qmin, Qmax))), K[2] * float(sat_signal(Qp3, (Qmin, Qmax)))])
    x_vec = self._get_internal_state_variables()
    if x_vec.size == 0:
        x0 = self.Model.InitialCondition
        if x0 is None or len(x0) != Nx:
            raise Sim3TanksError('ERR024')
        x0 = np.asarray(x0, dtype=float)
        Qx = sys_flow_rates(x0, K, h0, Beta)
        q = np.concatenate([Qin, Qx])
        _, m_noise = check_enabled_noises(self)
        y = sys_measurements(x0, q, fault_mag, offset, m_noise)
        self._set_internal_state_variables(x0)
        self._set_internal_flow_variables(q)
        self._set_internal_sensor_measurements(y)
        self._set_internal_valve_signals(op_mode.astype(float))
        self._set_internal_fault_magnitudes(fault_mag)
        self._set_internal_fault_offsets(offset[10:])
        self._reset_internal_simulation_time()
    else:
        x0 = x_vec[-1, :] if x_vec.ndim == 2 else x_vec
    p_noise, _ = check_enabled_noises(self)

    def model(t, x):
        from funcoes_aux.sys_dynamics import sys_dynamics
        return sys_dynamics(t, x, Qin, K, h0, Sc, Beta, p_noise)
    sol = solve_ivp(model, t_span=(0.0, Tspan), y0=x0, method='RK45', max_step=Tspan, rtol=1e-06, dense_output=False)
    if not sol.success or not np.all(np.isfinite(sol.y)):
        raise Sim3TanksError('ERR007')
    xsol_full = sol.y.T
    tsol_full = sol.t
    if all_steps:
        xsol = sat_signal(xsol_full[1:, :], (0, Hmax))
        tsol = tsol_full[1:]
    else:
        xsol = sat_signal(xsol_full[-1:, :], (0, Hmax))
        tsol = tsol_full[-1:]
    n_steps = xsol.shape[0]
    ysol = np.zeros((n_steps, Nx + Nq))
    qsol = np.zeros((n_steps, Nq))
    t0 = self._get_internal_simulation_time(-1)
    for i in range(n_steps):
        Qx = sys_flow_rates(xsol[i, :], K, h0, Beta)
        qsol[i, :] = np.concatenate([Qin, Qx])
        _, m_noise = check_enabled_noises(self)
        ysol[i, :] = sys_measurements(xsol[i, :], qsol[i, :], fault_mag, offset, m_noise)
        self._push_internal_state_variables(xsol[i, :])
        self._push_internal_flow_variables(qsol[i, :])
        self._push_internal_sensor_measurements(ysol[i, :])
        self._push_internal_valve_signals(K)
        self._push_internal_fault_magnitudes(fault_mag)
        self._push_internal_fault_offsets(offset[10:])
        self._increment_internal_simulation_time(t0 + tsol[i])
    return (ysol, xsol, qsol)
