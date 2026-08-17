import warnings
from funcoes_aux.get_message import Sim3TanksError, get_message

def _matlab_markevery(n0, divisor=4, start=0):
    n1 = max(round(n0 / divisor), 1)
    return list(range(start, n0, n1))

def plot_flows(self, flow_name: str=None):
    import matplotlib.pyplot as plt
    from .sim3tanks import Sim3Tanks
    from .get_flow_variables import get_flow_variables
    from .get_sensor_measurements import get_sensor_measurements
    Q = get_flow_variables(self)
    if Q.empty:
        warnings.warn(get_message('WARN008'))
        return
    Y = get_sensor_measurements(self)
    time = Q.index.to_numpy()
    FLOW_IDs = Sim3Tanks.LIST_OF_FLOWS
    tag = 'Sim3Tanks'
    if flow_name is None:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
        fig.canvas.manager.set_window_title(f'{tag}: flows')
        for fid in FLOW_IDs:
            ax1.plot(time, Q[fid].to_numpy(), label=fid)
        ax1.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Real values')
        ax1.set_xlim(time[0], time[-1])
        for fid in FLOW_IDs:
            ax2.plot(time, Y[fid].to_numpy())
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Measured values')
        ax2.set_xlim(time[0], time[-1])
        plt.tight_layout()
        plt.show()
    else:
        option = [f.lower() for f in FLOW_IDs]
        if flow_name.lower() not in option:
            raise Sim3TanksError('ERR003')
        fid = FLOW_IDs[option.index(flow_name.lower())]
        real_value = Q[fid].to_numpy()
        measured_value = Y[fid].to_numpy()
        N0 = len(time)
        from .plot_utils import time_based_markevery
        mark_idx = time_based_markevery(time)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))
        fig.canvas.manager.set_window_title(f'{tag}: {fid}')
        ax1.plot(time, real_value, 'b-o', markevery=mark_idx, label=fid)
        ax1.legend(loc='upper right')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Real value')
        ax1.set_xlim(time[0], time[-1])
        ax2.plot(time, measured_value, 'r-o', markevery=mark_idx, label=fid)
        ax2.legend(loc='upper right')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Measured value')
        ax2.set_xlim(time[0], time[-1])
        plt.tight_layout()
        plt.show()
