import warnings
from funcoes_aux.get_message import Sim3TanksError, get_message

def plot_levels(self, level_name: str=None):
    import matplotlib.pyplot as plt
    from .sim3tanks import Sim3Tanks
    from .get_state_variables import get_state_variables
    from .get_sensor_measurements import get_sensor_measurements
    from .plot_utils import time_based_markevery, staggered_time_markevery
    X = get_state_variables(self)
    if X.empty:
        warnings.warn(get_message('WARN008'))
        return
    Y = get_sensor_measurements(self)
    time = X.index.to_numpy()
    STATE_IDs = Sim3Tanks.LIST_OF_STATES
    tag = 'Sim3Tanks'
    if level_name is None:
        mark_idxs = staggered_time_markevery(time, n_series=3)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))
        fig.canvas.manager.set_window_title(f'{tag}: levels')
        markers = ['-o', '-s', '-^']
        for ax, df, ylabel in [(ax1, X, 'Real values'), (ax2, Y[STATE_IDs], 'Measured values')]:
            for sid, mk, mi in zip(STATE_IDs, markers, mark_idxs):
                ax.plot(time, df[sid].to_numpy(), mk, markevery=mi, label=sid)
            ax.legend(loc='upper right')
            ax.set_xlabel('Time')
            ax.set_ylabel(ylabel)
            ax.set_xlim(time[0], time[-1])
        plt.tight_layout()
        plt.show()
    else:
        option = [s.lower() for s in STATE_IDs]
        if level_name.lower() not in option:
            raise Sim3TanksError('ERR003')
        sid = STATE_IDs[option.index(level_name.lower())]
        real_value = X[sid].to_numpy()
        measured_value = Y[sid].to_numpy()
        mark_idx = time_based_markevery(time)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))
        fig.canvas.manager.set_window_title(f'{tag}: {sid}')
        ax1.plot(time, real_value, 'b-o', markevery=mark_idx, label=sid)
        ax1.legend(loc='upper right')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Real value')
        ax1.set_xlim(time[0], time[-1])
        ax2.plot(time, measured_value, 'r-o', markevery=mark_idx, label=sid)
        ax2.legend(loc='upper right')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Measured value')
        ax2.set_xlim(time[0], time[-1])
        plt.tight_layout()
        plt.show()
