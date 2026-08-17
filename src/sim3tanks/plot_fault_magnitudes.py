import warnings
from funcoes_aux.get_message import Sim3TanksError, get_message

def plot_fault_magnitudes(self, fault_name: str=None):
    import matplotlib.pyplot as plt
    from .sim3tanks import Sim3Tanks
    from .get_fault_magnitudes import get_fault_magnitudes
    from .plot_utils import time_based_markevery
    LIST_OF_FAULTS = Sim3Tanks.LIST_OF_FAULTS
    df = get_fault_magnitudes(self)
    if df.empty:
        warnings.warn(get_message('WARN008'))
        return
    time = df.index.to_numpy()
    mark_idx = time_based_markevery(time)
    tag = 'Sim3Tanks'
    if fault_name is None:
        fig, axes = plt.subplots(4, 6, figsize=(18, 10))
        fig.canvas.manager.set_window_title(f'{tag}: fault magnitudes')
        axes = axes.flatten()
        for i, fid in enumerate(LIST_OF_FAULTS):
            ax = axes[i]
            ax.plot(time, df[fid].to_numpy(), 'r-o', markevery=mark_idx)
            ax.legend([fid], loc='best')
            ax.set_xlim(time[0], time[-1])
            ax.set_ylim(0, 1)
            ax.set_yticks([0, 0.5, 1])
        for j in range(len(LIST_OF_FAULTS), len(axes)):
            axes[j].axis('off')
        plt.tight_layout()
        plt.show()
    else:
        option = [f.lower() for f in LIST_OF_FAULTS]
        if fault_name.lower() not in option:
            raise Sim3TanksError('ERR003')
        fid = LIST_OF_FAULTS[option.index(fault_name.lower())]
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.canvas.manager.set_window_title(f'{tag}: {fid} magnitude')
        ax.plot(time, df[fid].to_numpy(), 'r-o', markevery=mark_idx)
        ax.legend([fid], loc='best')
        ax.set_xlabel('Time')
        ax.set_ylabel('Magnitude')
        ax.set_xlim(time[0], time[-1])
        ax.set_ylim(0, 1)
        ax.set_yticks([0, 0.5, 1])
        plt.tight_layout()
        plt.show()
