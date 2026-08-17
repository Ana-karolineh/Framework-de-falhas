import warnings
import numpy as np
from funcoes_aux.check_operation_mode import check_operation_mode
from funcoes_aux.get_message import Sim3TanksError, get_message
from funcoes_aux.get_rgb_triplet import get_rgb_triplet

def plot_valves(self, valve_name: str=None):
    import matplotlib.pyplot as plt
    from .get_valve_signals import get_valve_signals
    from .plot_utils import time_based_markevery
    K = get_valve_signals(self)
    if K.empty:
        warnings.warn(get_message('WARN008'))
        return
    time = K.index.to_numpy()
    op_mode, VALVE_IDs = check_operation_mode(self)
    tag = 'Sim3Tanks'
    normal = get_rgb_triplet('normal')
    fault = get_rgb_triplet('fault')
    N0 = len(time)
    mark_idx = time_based_markevery(time)

    def _draw_valve(ax, vid, opm, label_fs=8):
        flag1, flag2 = ('Open', 'Closed') if opm != 0 else ('Closed', 'Open')
        dK = np.full(N0, opm)
        ax.plot(time, dK, '--', color=normal)
        ax.plot(time, 1 - dK, '--', color=fault)
        ax.plot(time, K[vid].to_numpy(), 'k-o', markevery=mark_idx, label=vid)
        ax.legend(loc='best')
        ax.set_xlim(time[0], time[-1])
        ax.set_ylim(-0.1, 1.1)
        ax.set_yticks([0, 0.5, 1])
        ax.text(time[0], opm, flag1, fontsize=label_fs, ha='left', bbox=dict(facecolor=normal, edgecolor='none'))
        ax.text(time[0], 1 - opm, flag2, fontsize=label_fs, ha='left', bbox=dict(facecolor=fault, edgecolor='none'))
    if valve_name is None:
        fig, axes = plt.subplots(4, 3, figsize=(14, 12))
        fig.canvas.manager.set_window_title(f'{tag}: valves')
        axes = axes.flatten()
        for i, vid in enumerate(VALVE_IDs):
            _draw_valve(axes[i], vid, op_mode[i])
        for j in range(len(VALVE_IDs), len(axes)):
            axes[j].axis('off')
        plt.tight_layout()
        plt.show()
    else:
        option = [v.lower() for v in VALVE_IDs]
        if valve_name.lower() not in option:
            raise Sim3TanksError('ERR003')
        idx = option.index(valve_name.lower())
        vid = VALVE_IDs[idx]
        opm = op_mode[idx]
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.canvas.manager.set_window_title(f'{tag}: {vid}')
        _draw_valve(ax, vid, opm)
        ax.set_xlabel('Time')
        ax.set_ylabel('Opening Rate')
        plt.tight_layout()
        plt.show()
