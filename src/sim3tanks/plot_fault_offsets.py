import warnings
import numpy as np
from funcoes_aux.get_message import Sim3TanksError, get_message

def _apply_offset_ylim(ax, values):
    vmin, vmax = (float(np.nanmin(values)), float(np.nanmax(values)))
    if vmin >= -1 and vmax <= 1:
        ax.set_ylim(-1, 1)
        ax.set_yticks([-1, 0, 1])
    else:
        margin = 0.1 * max(abs(vmin), abs(vmax), 1)
        ax.set_ylim(vmin - margin, vmax + margin)

def plot_fault_offsets(self, fault_name: str=None):
    import matplotlib.pyplot as plt
    from .sim3tanks import Sim3Tanks
    from .get_fault_offsets import get_fault_offsets
    from .plot_utils import time_based_markevery
    FAULT_IDs = Sim3Tanks.LIST_OF_FAULTS[10:]
    df = get_fault_offsets(self)
    if df.empty:
        warnings.warn(get_message('WARN008'))
        return
    time = df.index.to_numpy()
    mark_idx = time_based_markevery(time)
    tag = 'Sim3Tanks'
    if fault_name is None:
        fig, axes = plt.subplots(3, 5, figsize=(16, 8))
        fig.canvas.manager.set_window_title(f'{tag}: fault offsets')
        axes = axes.flatten()
        for i, fid in enumerate(FAULT_IDs):
            ax = axes[i]
            ax.plot(time, df[fid].to_numpy(), 'r-o', markevery=mark_idx)
            ax.legend([fid], loc='best')
            ax.set_xlim(time[0], time[-1])
            _apply_offset_ylim(ax, df[fid].to_numpy())
        for j in range(len(FAULT_IDs), len(axes)):
            axes[j].axis('off')
        plt.tight_layout()
        plt.show()
    else:
        option = [f.lower() for f in FAULT_IDs]
        if fault_name.lower() not in option:
            raise Sim3TanksError('ERR003')
        fid = FAULT_IDs[option.index(fault_name.lower())]
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.canvas.manager.set_window_title(f'{tag}: {fid} offset')
        ax.plot(time, df[fid].to_numpy(), 'r-o', markevery=mark_idx)
        ax.legend([fid], loc='best')
        ax.set_xlabel('Time')
        ax.set_ylabel('Offset')
        ax.set_xlim(time[0], time[-1])
        _apply_offset_ylim(ax, df[fid].to_numpy())
        plt.tight_layout()
        plt.show()
